# 🚀 Modelos de CI/CD & Integração com Jira para Clientes

Esta pasta contém modelos prontos para empresas e desenvolvedores implementarem **auditoria contínua de segurança com IA** em suas esteiras de CI/CD privadas, com envio automático de alertas para o **GitHub Security (SARIF)** e criação de cards no **Jira**.

---

## 📁 Arquivos Disponíveis

1. **[`github-actions-audit.yml`](github-actions-audit.yml):** Workflow completo do GitHub Actions para auditoria em Pull Requests.
2. **[`gitlab-ci-audit.yml`](gitlab-ci-audit.yml):** Pipeline para GitLab CI com relatórios SAST e PDF.
3. **[`jira_sync.py`](jira_sync.py):** Script autônomo em Python para sincronizar achados do arquivo `results.sarif` com a API REST v3 do Jira.

---

## 📌 Configuração da Integração com o Jira

O script [`jira_sync.py`](jira_sync.py) consome o arquivo SARIF gerado pela IA e cria cards de **Bug / Vulnerabilidade** no Jira com prevenção automática de duplicatas.

### 1. Obter o Token de API do Jira (Atlassian)
1. Acesse [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
2. Clique em **Criar token de API**, dê um nome (ex: `CI/CD AppSec Token`) e copie o valor.

### 2. Configurar os Secrets no GitHub / GitLab

Adicione as seguintes variáveis secretas no seu repositório (**Settings > Secrets and variables > Actions**):

| Secret / Variável | Exemplo | Descrição |
| :--- | :--- | :--- |
| `JIRA_BASE_URL` | `https://sua-empresa.atlassian.net` | URL base do seu workspace Jira |
| `JIRA_USER_EMAIL` | `devsecops@suaempresa.com` | E-mail do usuário Atlassian |
| `JIRA_API_TOKEN` | `ATATT3xFfGF0...` | Token gerado no passo anterior |
| `JIRA_PROJECT_KEY` | `SEC` ou `PROJ` | Chave do projeto no Jira onde os cards serão abertos |

---

## 🤖 Como Funciona a Execução no Pull Request

1. O desenvolvedor abre um Pull Request no repositório.
2. A esteira executa o agente de IA utilizando os prompts instalados (ex: `.agent/prompts/security/api.md`).
3. O agente analisa o código e produz:
   - O relatório executivo em PDF (`docs/api-audit/relatorio-auditoria-api.pdf`).
   - O arquivo de vulnerabilidades padronizado (`docs/api-audit/results.sarif`).
4. A Action importa o SARIF para a aba **Security > Code Scanning** do GitHub.
5. O script `jira_sync.py` cria cards automáticos no Jira para os problemas **Críticos e Altos**.
6. Um comentário com o resumo é publicado automaticamente no Pull Request.
