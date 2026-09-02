#!/usr/bin/env python3
"""
==============================================================================
Sincronizador Automático de Vulnerabilidades SARIF com GitHub Issues
Modelo para uso em Pipelines de CI/CD (GitHub Actions)
==============================================================================
Lê o arquivo SARIF gerado pela auditoria de segurança (ex: docs/api-audit/results.sarif)
e cria automaticamente Issues no GitHub para achados de alta e crítica severidade,
evitando duplicações via paginação, busca na API do GitHub e cache em memória.
==============================================================================
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Set

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "")  # ex: "empresa/meu-repo"
SARIF_PATH = os.getenv("SARIF_PATH", "docs/api-audit/results.sarif")
API_BASE = os.getenv("GITHUB_API_URL", "https://api.github.com").rstrip("/")
HTTP_TIMEOUT_SECONDS = 30

# Cache em memória para evitar duplicatas dentro da mesma execução
PROCESSED_KEYS: Set[str] = set()
OPEN_ISSUE_TITLES_CACHE: Optional[Set[str]] = None


def validate_env() -> bool:
    """Valida as variáveis de ambiente necessárias para o GitHub Actions."""
    if not GITHUB_TOKEN or not GITHUB_REPOSITORY:
        print("❌ Variáveis GITHUB_TOKEN e GITHUB_REPOSITORY são obrigatórias.")
        return False
    return True


def get_headers() -> Dict[str, str]:
    """Retorna cabeçalhos padrão para a API REST do GitHub."""
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "AppSec-Prompts-CI/1.4.0",
    }


def load_all_open_issues() -> Set[str]:
    """Carrega todos os títulos de issues abertas com suporte a paginação para evitar duplicações."""
    global OPEN_ISSUE_TITLES_CACHE
    if OPEN_ISSUE_TITLES_CACHE is not None:
        return OPEN_ISSUE_TITLES_CACHE

    titles: Set[str] = set()
    page = 1
    per_page = 100

    while True:
        url = f"{API_BASE}/repos/{GITHUB_REPOSITORY}/issues?state=open&per_page={per_page}&page={page}"
        req = urllib.request.Request(url, headers=get_headers(), method="GET")
        try:
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
                issues: List[Dict[str, Any]] = json.loads(resp.read().decode("utf-8"))
                if not issues:
                    break
                for issue in issues:
                    title = issue.get("title", "")
                    if title:
                        titles.add(title.strip().lower())
                if len(issues) < per_page:
                    break
                page += 1
        except Exception as e:
            print(f"⚠️ Erro ao listar issues abertas no GitHub: {e}")
            break

    OPEN_ISSUE_TITLES_CACHE = titles
    return OPEN_ISSUE_TITLES_CACHE


def is_issue_already_open(title: str) -> bool:
    """Verifica se já existe issue aberta com o mesmo título."""
    open_titles = load_all_open_issues()
    normalized = title.strip().lower()
    return normalized in open_titles


def create_github_issue(rule_id: str, message: str, file_path: str, start_line: int, severity: str) -> Optional[int]:
    """Cria uma issue no GitHub se não for duplicata."""
    finding_fingerprint = f"{rule_id}:{file_path}:{start_line}"
    title = f"[AppSec] {rule_id} em {file_path}:{start_line}"

    # 1. Validação em cache local da execução
    if finding_fingerprint in PROCESSED_KEYS:
        print(f"ℹ️ Item já processado nesta execução ({finding_fingerprint}). Pulando...")
        return None

    # 2. Validação remota contra todas as issues abertas
    if is_issue_already_open(title):
        print(f"ℹ️ Issue já aberta no GitHub para '{title}'. Pulando...")
        PROCESSED_KEYS.add(finding_fingerprint)
        return None

    severity_label = "severity:critical" if severity.lower() in ["error", "critical"] else "severity:high"

    body_markdown = f"""## 🚨 Vulnerabilidade de Segurança Detectada pela Auditoria com IA

* **Módulo / Regra:** `{rule_id}`
* **Arquivo Afetado:** [`{file_path}#L{start_line}`](file:///{file_path}#L{start_line})
* **Severidade:** **{severity.upper()}**
* **Origem da Auditoria:** OWASP ASTF 2023 / WSTG v4.2

---

### 📝 Descrição do Problema & Remediação

```text
{message or 'Consulte o relatório completo em PDF nos artefatos da esteira de build.'}
```

---

> *Card gerado automaticamente pelo pipeline de CI/CD da Suíte de Prompts de AppSec.*
"""

    payload: Dict[str, Any] = {
        "title": title,
        "body": body_markdown,
        "labels": ["security", "appsec", "bug", severity_label]
    }

    url = f"{API_BASE}/repos/{GITHUB_REPOSITORY}/issues"
    payload_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=payload_bytes, headers=get_headers(), method="POST")

    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            issue_number = result.get("number")
            issue_url = result.get("html_url")
            print(f"✅ GitHub Issue #{issue_number} criada com sucesso: {issue_url}")
            PROCESSED_KEYS.add(finding_fingerprint)
            if OPEN_ISSUE_TITLES_CACHE is not None:
                OPEN_ISSUE_TITLES_CACHE.add(title.strip().lower())
            return issue_number
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"❌ Erro HTTP ao criar issue no GitHub ({e.code}): {err_body}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao criar issue no GitHub: {e}")
        return None


def main() -> None:
    print("=================================================================")
    print("  🐙 Sincronizador de Vulnerabilidades com GitHub Issues")
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

                issue_num = create_github_issue(rule_id, message, file_path, start_line, level)
                if issue_num:
                    created_count += 1

    print(f"\n🎉 Sincronização concluída: {created_count} nova(s) issue(s) criada(s) no GitHub.")


if __name__ == "__main__":
    main()
