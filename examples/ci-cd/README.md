# 🚀 Modelos de CI/CD & Automação de Tickets (GitHub Issues, GitLab & Jira)

Esta pasta contém modelos prontos para empresas e desenvolvedores implementarem **auditoria contínua de segurança com IA** em suas esteiras de CI/CD privadas, com envio automático de alertas para **GitHub Security (SARIF)** e abertura automática de cards em **GitHub Issues**, **GitLab Issues & Boards** ou **Jira**.

---

## 📁 Arquivos Disponíveis

1. **[`github-actions-audit.yml`](github-actions-audit.yml):** Workflow completo do GitHub Actions para auditoria em Pull Requests com publicação de SARIF, PDF e sincronização com GitHub Issues e Jira.
2. **[`gitlab-ci-audit.yml`](gitlab-ci-audit.yml):** Pipeline para GitLab CI com relatórios SAST, PDFs e sincronização com GitLab Issues.
3. **[`github_issues_sync.py`](github_issues_sync.py):** Sincronizador de vulnerabilidades SARIF com o **GitHub Issues**.
4. **[`gitlab_issues_sync.py`](gitlab_issues_sync.py):** Sincronizador de vulnerabilidades SARIF com o **GitLab Issues & Issue Boards**.
5. **[`jira_sync.py`](jira_sync.py):** Sincronizador de vulnerabilidades SARIF com a API REST v3 do **Jira (Atlassian)**.

---

## 🐙 1. Integração com GitHub Issues (`github_issues_sync.py`)

A criação de Issues no GitHub funciona de forma **nativa e sem configuração extra**:
* O GitHub Actions já fornece a variável `${{ secrets.GITHUB_TOKEN }}` automaticamente.
* O script verifica issues abertas no repositório antes de criar, garantindo **zero duplicatas**.
* Cada vulnerabilidade gera uma Issue com labels `security`, `appsec`, `bug` e severidade (`severity:critical` / `severity:high`).

---

## 🦊 2. Integração com GitLab Issues & Boards (`gitlab_issues_sync.py`)

* Utiliza o token padrão do pipeline (`$CI_JOB_TOKEN` ou `$GITLAB_TOKEN`) e o ID do projeto (`$CI_PROJECT_ID`).
* As issues são criadas com labels escopadas para fácil filtragem nos **GitLab Issue Boards** (ex: `severity::critical`, `security`).

---

## 📌 3. Integração com Jira Cloud / Data Center (`jira_sync.py`)

Cria cards de **Bug / Vulnerabilidade** no Jira da organização com formatação rica em Atlassian Document Format (ADF).

### Como Configurar nos Secrets do Repositório:
1. Gere um Token de API em [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
2. Configure os seguintes Secrets no repositório:
   - `JIRA_BASE_URL`: `https://sua-empresa.atlassian.net`
   - `JIRA_USER_EMAIL`: `devsecops@suaempresa.com`
   - `JIRA_API_TOKEN`: `ATATT3xFfGF0...`
   - `JIRA_PROJECT_KEY`: `SEC` ou `PROJ`

---

## 🤖 Como Funciona o Ciclo de Vida no Pull Request / Merge Request

1. O desenvolvedor abre um PR / MR no repositório.
2. A esteira executa o agente de IA utilizando os prompts de AppSec instalados (ex: `.agent/prompts/security/api.md`).
3. O agente analisa o código e produz:
   - O relatório executivo em PDF (`docs/api-audit/relatorio-auditoria-api.pdf`).
   - O arquivo de vulnerabilidades padronizado (`docs/api-audit/results.sarif`).
4. Os scripts de sincronização criam os cards/issues correspondentes automaticamente para problemas **Críticos e Altos**.
5. A esteira salva o PDF como artefato de build retido por 30 dias.
