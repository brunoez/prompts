#!/usr/bin/env python3
"""
==============================================================================
Sincronizador Automático de Vulnerabilidades SARIF com GitLab Issues & Boards
Modelo para uso em Pipelines de CI/CD (GitLab CI)
==============================================================================
Lê o arquivo SARIF gerado pela auditoria de segurança (ex: docs/api-audit/results.sarif)
e cria automaticamente Issues no GitLab para achados de alta e crítica severidade,
evitando duplicações via consulta prévia à API do GitLab e cache em memória.
==============================================================================
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Set

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN") or os.getenv("CI_JOB_TOKEN", "")
CI_API_V4_URL = os.getenv("CI_API_V4_URL", "https://gitlab.com/api/v4").rstrip("/")
CI_PROJECT_ID = os.getenv("CI_PROJECT_ID", "")
SARIF_PATH = os.getenv("SARIF_PATH", "docs/api-audit/results.sarif")
HTTP_TIMEOUT_SECONDS = 30

# Cache em memória para evitar duplicatas dentro da mesma execução
PROCESSED_KEYS: Set[str] = set()


def validate_env() -> bool:
    """Valida as variáveis de ambiente necessárias para o GitLab CI."""
    if not GITLAB_TOKEN or not CI_PROJECT_ID:
        print("❌ Variáveis GITLAB_TOKEN (ou CI_JOB_TOKEN) e CI_PROJECT_ID são obrigatórias.")
        return False
    return True


def get_headers() -> Dict[str, str]:
    """Retorna cabeçalhos padrão para a API REST v4 do GitLab."""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "AppSec-Prompts-CI/1.4.0",
    }
    # Suporte tanto a Personal Access Token / Project Token quanto a CI_JOB_TOKEN
    if os.getenv("GITLAB_TOKEN"):
        headers["PRIVATE-TOKEN"] = GITLAB_TOKEN
    else:
        headers["JOB-TOKEN"] = GITLAB_TOKEN
    return headers


def search_existing_issue(rule_id: str, file_path: str) -> bool:
    """Consulta issues abertas no GitLab para verificar se a vulnerabilidade já existe."""
    encoded_project = urllib.parse.quote(str(CI_PROJECT_ID), safe="")
    search_query = f"{rule_id} em {file_path}"
    encoded_search = urllib.parse.quote(search_query)
    url = f"{CI_API_V4_URL}/projects/{encoded_project}/issues?state=opened&search={encoded_search}&per_page=10"

    req = urllib.request.Request(url, headers=get_headers(), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
            issues: List[Dict[str, Any]] = json.loads(resp.read().decode("utf-8"))
            for issue in issues:
                title = issue.get("title", "")
                if rule_id.lower() in title.lower() and file_path.lower() in title.lower():
                    return True
            return False
    except Exception as e:
        print(f"⚠️ Não foi possível verificar duplicatas no GitLab: {e}")
        return False


def create_gitlab_issue(rule_id: str, message: str, file_path: str, start_line: int, severity: str) -> Optional[int]:
    """Cria uma issue no GitLab caso não exista duplicata."""
    finding_fingerprint = f"{rule_id}:{file_path}:{start_line}"
    title = f"[AppSec] {rule_id} em {file_path}:{start_line}"

    # 1. Validação em cache local da execução
    if finding_fingerprint in PROCESSED_KEYS:
        print(f"ℹ️ Item já processado nesta execução ({finding_fingerprint}). Pulando...")
        return None

    # 2. Validação remota no GitLab
    if search_existing_issue(rule_id, file_path):
        print(f"ℹ️ Issue já aberta no GitLab para '{title}'. Pulando...")
        PROCESSED_KEYS.add(finding_fingerprint)
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
{message or 'Consulte o relatório completo em PDF nos artefatos da esteira de build.'}
```

---

> *Card gerado automaticamente pelo pipeline de CI/CD da Suíte de Prompts de AppSec.*
"""

    payload: Dict[str, Any] = {
        "title": title,
        "description": description_markdown,
        "labels": f"security,appsec,bug,{scoped_severity}"
    }

    encoded_project = urllib.parse.quote(str(CI_PROJECT_ID), safe="")
    url = f"{CI_API_V4_URL}/projects/{encoded_project}/issues"
    payload_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=payload_bytes, headers=get_headers(), method="POST")

    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            issue_iid = result.get("iid")
            issue_url = result.get("web_url")
            print(f"✅ GitLab Issue #{issue_iid} criada com sucesso: {issue_url}")
            PROCESSED_KEYS.add(finding_fingerprint)
            return issue_iid
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"❌ Erro HTTP ao criar issue no GitLab ({e.code}): {err_body}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao criar issue no GitLab: {e}")
        return None


def main() -> None:
    print("=================================================================")
    print("  🦊 Sincronizador de Vulnerabilidades com GitLab Issues & Boards")
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

                issue_iid = create_gitlab_issue(rule_id, message, file_path, start_line, level)
                if issue_iid:
                    created_count += 1

    print(f"\n🎉 Sincronização concluída: {created_count} nova(s) issue(s) criada(s) no GitLab.")


if __name__ == "__main__":
    main()
