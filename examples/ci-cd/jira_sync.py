#!/usr/bin/env python3
"""
==============================================================================
Sincronizador Automático de Vulnerabilidades SARIF com Jira REST API v3
Modelo para uso em Pipelines de CI/CD (GitHub Actions / GitLab CI)
==============================================================================
Lê o arquivo SARIF gerado pela auditoria de segurança (ex: docs/api-audit/results.sarif)
e cria automaticamente cards/bugs no Jira para achados de alta e crítica severidade,
evitando duplicações via consulta prévia JQL e cache em memória.
==============================================================================
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Set

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "").rstrip("/")
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "")
SARIF_PATH = os.getenv("SARIF_PATH", "docs/api-audit/results.sarif")
HTTP_TIMEOUT_SECONDS = 30

# Cache em memória para evitar criar duplicatas no mesmo scan
PROCESSED_KEYS: Set[str] = set()


def validate_env() -> bool:
    """Valida se as variáveis de ambiente necessárias e seguras foram fornecidas."""
    missing = []
    if not JIRA_BASE_URL:
        missing.append("JIRA_BASE_URL")
    if not JIRA_USER_EMAIL:
        missing.append("JIRA_USER_EMAIL")
    if not JIRA_API_TOKEN:
        missing.append("JIRA_API_TOKEN")
    if not JIRA_PROJECT_KEY:
        missing.append("JIRA_PROJECT_KEY")

    if missing:
        print(f"❌ Variáveis de ambiente obrigatórias não configuradas: {missing}")
        print("💡 Configure estas variáveis nos Secrets do seu repositório de CI/CD.")
        return False

    if not JIRA_BASE_URL.startswith("https://") and not JIRA_BASE_URL.startswith("http://"):
        print(f"❌ JIRA_BASE_URL inválida (deve iniciar com https://): {JIRA_BASE_URL}")
        return False

    return True


def get_auth_headers() -> Dict[str, str]:
    """Gera cabeçalhos de autenticação HTTP Basic para o Jira REST API v3."""
    credentials = f"{JIRA_USER_EMAIL}:{JIRA_API_TOKEN}"
    encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "AppSec-Prompts-CI/1.4.0",
    }


def sanitize_jql_text(text: str) -> str:
    """Sanitiza strings de busca para evitar erros de sintaxe ou injeção em JQL."""
    # Mantém apenas caracteres alfanuméricos, barras, pontos e underscores
    return re.sub(r'[^a-zA-Z0-9_\-\.\/ ]', ' ', text).strip()


def search_existing_issue(rule_id: str, file_path: str, start_line: int) -> bool:
    """Consulta o Jira para verificar se já existe issue aberta para a vulnerabilidade."""
    sanitized_query = sanitize_jql_text(f"{rule_id} {file_path}")
    jql = f'project = "{JIRA_PROJECT_KEY}" AND statusCategory != Done AND summary ~ "{sanitized_query}"'
    url = f"{JIRA_BASE_URL}/rest/api/3/search?jql={urllib.parse.quote(jql)}&maxResults=5"

    req = urllib.request.Request(url, headers=get_auth_headers(), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as response:
            data: Dict[str, Any] = json.loads(response.read().decode("utf-8"))
            issues = data.get("issues", [])
            for issue in issues:
                summary = issue.get("fields", {}).get("summary", "")
                if rule_id.lower() in summary.lower() and file_path.lower() in summary.lower():
                    return True
            return False
    except urllib.error.HTTPError as e:
        print(f"⚠️ Erro ao consultar Jira ({e.code}): {e.reason}")
        return False
    except Exception as e:
        print(f"⚠️ Falha de comunicação ao verificar duplicatas no Jira: {e}")
        return False


def build_adf_description(rule_id: str, message: str, file_path: str, start_line: int, severity: str) -> Dict[str, Any]:
    """Constrói a descrição estruturada no formato Atlassian Document Format (ADF)."""
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "🚨 Vulnerabilidade detectada em auditoria automatizada de segurança (AppSec):", "marks": [{"type": "strong"}]}
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": f"Regra / Módulo: {rule_id}"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": f"Arquivo Afetado: {file_path} (Linha {start_line})"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": f"Severidade: {severity.upper()}"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Framework Metodológico: OWASP ASTF 2023 / WSTG v4.2"}]}]}
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Detalhes da Vulnerabilidade e Código de Remediação:", "marks": [{"type": "strong"}]}
                ]
            },
            {
                "type": "codeBlock",
                "attrs": {"language": "text"},
                "content": [{"type": "text", "text": message or "Consulte o código-fonte e o relatório em PDF nos artefatos de build."}]
            }
        ]
    }


def create_jira_issue(rule_id: str, message: str, file_path: str, start_line: int, severity: str) -> Optional[str]:
    """Cria um card de Bug no Jira caso não exista duplicata."""
    finding_fingerprint = f"{rule_id}:{file_path}:{start_line}"
    summary = f"[AppSec] {rule_id} em {file_path}:{start_line}"

    # 1. Validação em cache local da execução
    if finding_fingerprint in PROCESSED_KEYS:
        print(f"ℹ️ Item já processado nesta execução ({finding_fingerprint}). Pulando...")
        return None

    # 2. Validação remota no Jira
    if search_existing_issue(rule_id, file_path, start_line):
        print(f"ℹ️ Ticket já existente no Jira para '{summary}'. Pulando...")
        PROCESSED_KEYS.add(finding_fingerprint)
        return None

    priority_map = {
        "error": "Highest",
        "critical": "Highest",
        "warning": "High",
        "high": "High",
        "note": "Medium",
    }
    jira_priority = priority_map.get(severity.lower(), "High")
    description_adf = build_adf_description(rule_id, message, file_path, start_line, severity)

    payload: Dict[str, Any] = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": description_adf,
            "issuetype": {"name": "Bug"},
            "priority": {"name": jira_priority},
            "labels": ["appsec", "security-scan", "owasp-astf"]
        }
    }

    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    payload_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=payload_bytes, headers=get_auth_headers(), method="POST")

    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            issue_key = result.get("key")
            print(f"✅ Card criado no Jira com sucesso: {issue_key} ({summary})")
            PROCESSED_KEYS.add(finding_fingerprint)
            return issue_key
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"❌ Erro HTTP ao criar issue no Jira ({e.code}): {err_body}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao criar issue no Jira: {e}")
        return None


def main() -> None:
    print("=================================================================")
    print("  📌 Sincronizador de Vulnerabilidades de Segurança com o Jira")
    print("=================================================================")

    if not validate_env():
        sys.exit(0)

    if not os.path.isfile(SARIF_PATH):
        print(f"ℹ️ Nenhum arquivo SARIF encontrado em '{SARIF_PATH}'. Nada a sincronizar.")
        sys.exit(0)

    try:
        with open(SARIF_PATH, "r", encoding="utf-8") as f:
            sarif = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON do arquivo SARIF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo SARIF: {e}")
        sys.exit(1)

    created_count = 0
    for run in sarif.get("runs", []):
        for result in run.get("results", []):
            level = result.get("level", "warning")
            if level.lower() in ["error", "warning", "critical", "high"]:
                rule_id = result.get("ruleId", "AppSec-Finding")
                message = result.get("message", {}).get("text", "")
                locations = result.get("locations", [])

                file_path = "src/api"
                start_line = 1
                if locations:
                    phys = locations[0].get("physicalLocation", {})
                    file_path = phys.get("artifactLocation", {}).get("uri", "src/api")
                    start_line = phys.get("region", {}).get("startLine", 1)

                issue_key = create_jira_issue(rule_id, message, file_path, start_line, level)
                if issue_key:
                    created_count += 1

    print(f"\n🎉 Sincronização concluída: {created_count} novo(s) card(s) criado(s) no Jira.")


if __name__ == "__main__":
    main()
