#!/usr/bin/env python3
"""
==============================================================================
Sincronizador Automático de Vulnerabilidades SARIF com Jira REST API v3
Modelo para uso em Pipelines de CI/CD (GitHub Actions / GitLab CI)
==============================================================================
Lê o arquivo SARIF gerado pela auditoria de segurança (ex: docs/api-audit/results.sarif)
e cria automaticamente cards/bugs no Jira para achados de alta e crítica severidade,
evitando duplicações via consulta prévia JQL.
==============================================================================
"""

import os
import json
import base64
import urllib.request
import urllib.parse
import urllib.error
import sys

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")          # ex: "https://empresa.atlassian.net"
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL")      # ex: "devsecops@empresa.com"
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")        # Token de API do Atlassian
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")    # ex: "SEC" ou "PROJ"
SARIF_PATH = os.getenv("SARIF_PATH", "docs/api-audit/results.sarif")
PDF_PATH = os.getenv("PDF_PATH", "docs/api-audit/relatorio-auditoria-api.pdf")


def validate_env():
    missing = []
    for var in ["JIRA_BASE_URL", "JIRA_USER_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY"]:
        if not os.getenv(var):
            missing.append(var)
    if missing:
        print(f"❌ Variáveis de ambiente obrigatórias não configuradas: {missing}")
        print("💡 Configure estas variáveis nos Secrets do seu repositório CI/CD.")
        return False
    return True


def get_auth_header():
    credentials = f"{JIRA_USER_EMAIL}:{JIRA_API_TOKEN}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def search_existing_issue(summary_query):
    """Consulta o Jira para evitar abrir tickets duplicados."""
    base_url = JIRA_BASE_URL.rstrip("/")
    jql = f'project = "{JIRA_PROJECT_KEY}" AND statusCategory != Done AND summary ~ "{summary_query}"'
    url = f"{base_url}/rest/api/3/search?jql={urllib.parse.quote(jql)}"
    req = urllib.request.Request(url, headers=get_auth_header())
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("total", 0) > 0
    except Exception as e:
        print(f"⚠️ Não foi possível verificar duplicatas no Jira: {e}")
        return False


def create_jira_issue(rule_id, message, file_path, start_line, severity):
    base_url = JIRA_BASE_URL.rstrip("/")
    summary = f"[AppSec] {rule_id} em {file_path}:{start_line}"
    
    # Query de busca simplificada para prevenção de duplicatas
    query_title = f"{rule_id} {file_path}"
    if search_existing_issue(query_title):
        print(f"ℹ️ Ticket já existe no Jira para '{summary}'. Pulando...")
        return None

    priority_map = {
        "error": "Highest",
        "critical": "Highest",
        "warning": "High",
        "high": "High",
        "note": "Medium"
    }
    jira_priority = priority_map.get(severity.lower(), "High")

    # Formato Atlassian Document Format (ADF) para o Jira v3
    description_adf = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "🚨 Vulnerabilidade detectada em auditoria automatizada de segurança:", "marks": [{"type": "strong"}]}
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": f"Regra / Módulo: {rule_id}"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": f"Arquivo Afetado: {file_path} (Linha {start_line})"}]}]},
                    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": f"Severidade: {severity.upper()}"}]}]}
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Detalhes da Vulnerabilidade e Correção:", "marks": [{"type": "strong"}]}
                ]
            },
            {
                "type": "codeBlock",
                "attrs": {"language": "text"},
                "content": [{"type": "text", "text": message or "Consulte o código e o relatório completo."}]
            }
        ]
    }

    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": description_adf,
            "issuetype": {"name": "Bug"},
            "priority": {"name": jira_priority},
            "labels": ["appsec", "security-scan", "owasp-astf"]
        }
    }

    url = f"{base_url}/rest/api/3/issue"
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=get_auth_header())
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            issue_key = result.get("key")
            print(f"✅ Card criado no Jira com sucesso: {issue_key} ({summary})")
            return issue_key
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"❌ Erro HTTP ao criar issue no Jira ({e.code}): {err_body}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao criar issue no Jira: {e}")
        return None


def main():
    print("=================================================================")
    print("  📌 Sincronizador de Vulnerabilidades de Segurança com o Jira")
    print("=================================================================")

    if not validate_env():
        sys.exit(0)

    if not os.path.isfile(SARIF_PATH):
        print(f"ℹ️ Nenhum arquivo SARIF encontrado em {SARIF_PATH}. Nada a sincronizar.")
        sys.exit(0)

    try:
        with open(SARIF_PATH, "r", encoding="utf-8") as f:
            sarif = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo SARIF: {e}")
        sys.exit(1)

    created_count = 0
    for run in sarif.get("runs", []):
        for result in run.get("results", []):
            level = result.get("level", "warning")
            # Sincroniza apenas achados de erro/críticos e warnings
            if level in ["error", "warning", "critical", "high"]:
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
