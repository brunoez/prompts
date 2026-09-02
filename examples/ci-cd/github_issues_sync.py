#!/usr/bin/env python3
"""
==============================================================================
Sincronizador Automático de Vulnerabilidades SARIF com GitHub Issues
Modelo para uso em Pipelines de CI/CD (GitHub Actions)
==============================================================================
Lê o arquivo SARIF gerado pela auditoria de segurança (ex: docs/api-audit/results.sarif)
e cria automaticamente Issues no GitHub para achados de alta e crítica severidade,
evitando duplicações via consulta prévia à API de Issues do GitHub.
==============================================================================
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
import sys

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")  # ex: "empresa/meu-repo"
SARIF_PATH = os.getenv("SARIF_PATH", "docs/api-audit/results.sarif")
API_BASE = os.getenv("GITHUB_API_URL", "https://api.github.com")


def validate_env():
    if not GITHUB_TOKEN or not GITHUB_REPOSITORY:
        print("❌ Variáveis GITHUB_TOKEN e GITHUB_REPOSITORY são obrigatórias.")
        return False
    return True


def get_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json"
    }


def search_existing_issue(summary_prefix):
    """Consulta issues abertas no GitHub para evitar duplicatas."""
    url = f"{API_BASE}/repos/{GITHUB_REPOSITORY}/issues?state=open&per_page=100"
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as resp:
            issues = json.loads(resp.read().decode())
            for issue in issues:
                if summary_prefix.lower() in issue.get("title", "").lower():
                    return True
            return False
    except Exception as e:
        print(f"⚠️ Não foi possível verificar duplicatas no GitHub: {e}")
        return False


def create_github_issue(rule_id, message, file_path, start_line, severity):
    title = f"[AppSec] {rule_id} em {file_path}:{start_line}"
    query_prefix = f"{rule_id} em {file_path}:{start_line}"
    
    if search_existing_issue(query_prefix):
        print(f"ℹ️ Issue já aberta no GitHub para '{title}'. Pulando...")
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
{message or 'Consulte o relatório completo em PDF nos artefatos da esteira.'}
```

---

> *Card gerado automaticamente pelo pipeline de CI/CD da Suíte de Prompts de AppSec.*
"""

    payload = {
        "title": title,
        "body": body_markdown,
        "labels": ["security", "appsec", "bug", severity_label]
    }

    url = f"{API_BASE}/repos/{GITHUB_REPOSITORY}/issues"
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=get_headers())
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            issue_number = result.get("number")
            issue_url = result.get("html_url")
            print(f"✅ GitHub Issue #{issue_number} criada com sucesso: {issue_url}")
            return issue_number
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"❌ Erro HTTP ao criar issue no GitHub ({e.code}): {err_body}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao criar issue no GitHub: {e}")
        return None


def main():
    print("=================================================================")
    print("  🐙 Sincronizador de Vulnerabilidades com GitHub Issues")
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
                
                issue_num = create_github_issue(rule_id, message, file_path, start_line, level)
                if issue_num:
                    created_count += 1

    print(f"\n🎉 Sincronização concluída: {created_count} nova(s) issue(s) criada(s) no GitHub.")


if __name__ == "__main__":
    main()
