#!/usr/bin/env python3
"""
==============================================================================
Sincronizador Automático de Vulnerabilidades SARIF com GitLab Issues & Boards
Modelo para uso em Pipelines de CI/CD (GitLab CI)
==============================================================================
Lê o arquivo SARIF gerado pela auditoria de segurança (ex: docs/api-audit/results.sarif)
e cria automaticamente Issues no GitLab para achados de alta e crítica severidade,
evitando duplicações via consulta prévia à API do GitLab.
==============================================================================
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
import sys

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN") or os.getenv("CI_JOB_TOKEN")
CI_API_V4_URL = os.getenv("CI_API_V4_URL", "https://gitlab.com/api/v4")
CI_PROJECT_ID = os.getenv("CI_PROJECT_ID")  # ID numérico ou URL-encoded path do projeto
SARIF_PATH = os.getenv("SARIF_PATH", "docs/api-audit/results.sarif")


def validate_env():
    if not GITLAB_TOKEN or not CI_PROJECT_ID:
        print("❌ Variáveis GITLAB_TOKEN (ou CI_JOB_TOKEN) e CI_PROJECT_ID são obrigatórias.")
        return False
    return True


def get_headers():
    return {
        "PRIVATE-TOKEN": GITLAB_TOKEN,
        "Content-Type": "application/json"
    }


def search_existing_issue(summary_prefix):
    """Consulta issues abertas no GitLab para evitar duplicatas."""
    encoded_project = urllib.parse.quote(str(CI_PROJECT_ID), safe="")
    url = f"{CI_API_V4_URL}/projects/{encoded_project}/issues?state=opened&per_page=100"
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as resp:
            issues = json.loads(resp.read().decode())
            for issue in issues:
                if summary_prefix.lower() in issue.get("title", "").lower():
                    return True
            return False
    except Exception as e:
        print(f"⚠️ Não foi possível verificar duplicatas no GitLab: {e}")
        return False


def create_gitlab_issue(rule_id, message, file_path, start_line, severity):
    title = f"[AppSec] {rule_id} em {file_path}:{start_line}"
    query_prefix = f"{rule_id} em {file_path}:{start_line}"
    
    if search_existing_issue(query_prefix):
        print(f"ℹ️ Issue já aberta no GitLab para '{title}'. Pulando...")
        return None

    scoped_severity = "severity::critical" if severity.lower() in ["error", "critical"] else "severity::high"

    description_markdown = f"""## 🚨 Vulnerabilidade de Segurança Detectada pela Auditoria com IA

* **Módulo / Regra:** `{rule_id}`
* **Arquivo Afetado:** `{file_path}` (Linha `{start_line}`)
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
        "description": description_markdown,
        "labels": f"security,appsec,bug,{scoped_severity}"
    }

    encoded_project = urllib.parse.quote(str(CI_PROJECT_ID), safe="")
    url = f"{CI_API_V4_URL}/projects/{encoded_project}/issues"
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=get_headers())
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            issue_iid = result.get("iid")
            issue_url = result.get("web_url")
            print(f"✅ GitLab Issue #{issue_iid} criada com sucesso: {issue_url}")
            return issue_iid
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"❌ Erro HTTP ao criar issue no GitLab ({e.code}): {err_body}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao criar issue no GitLab: {e}")
        return None


def main():
    print("=================================================================")
    print("  🦊 Sincronizador de Vulnerabilidades com GitLab Issues & Boards")
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
                
                issue_iid = create_gitlab_issue(rule_id, message, file_path, start_line, level)
                if issue_iid:
                    created_count += 1

    print(f"\n🎉 Sincronização concluída: {created_count} nova(s) issue(s) criada(s) no GitLab.")


if __name__ == "__main__":
    main()
