# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico (SemVer)](https://semver.org/lang/pt-BR/).

## [1.7.0] - 2026-09-03

### Adicionado & Aprimorado (Suporte Nativo ao Claude Code & Multi-IDE Sync)
- **Suporte Oficial a `.claude/prompts/` (Padrão Nativo Anthropic):**
  - O instalador `install.sh` agora adota `.claude/prompts/` como diretório oficial padrão para o Claude Code.
  - O comando rápido `curl -sSL ... | bash` instala diretamente na árvore nativa `.claude/`.
- **Matriz de Instalação Modular por IDE (`install.sh`):**
  - Modo `claude` (padrão oficial): `.claude/prompts/`
  - Modo `vscode` / `agent`: `.agent/prompts/`
  - Modo `cursor`: `.cursor/rules/`
  - Modo `windsurf`: `.windsurf/rules/`
  - Modo `all`: sincronização simultânea nas 4 árvores de diretórios (`.claude`, `.agent`, `.cursor`, `.windsurf`).
- **Documentação e Exemplos de Invocação (`README.md`):**
  - Atualização dos 19 comandos de invocação rápida para a sintaxe nativa `@[.claude/prompts/...]`.
  - Instruções de uso claras diferenciando Claude Code, VSCode e Cursor.
- **Validação Automatizada de Multi-IDE (`tests/test_integrity.py`):**
  - Expansão do teste `test_installer_execution` para validar a presença física dos 19 prompts nas 4 pastas suportadas.

## [1.6.0] - 2026-09-03

### Aprimorado (Alinhamento com AI-Native Playbook & Priorização de Ferramentas)
- **Priorização de Ferramentas (Claude Code ➔ VSCode ➔ Cursor):**
  - Reestruturação de documentação, `README.md`, `project_context.md` e `install.sh` definindo **Claude Code** como ferramenta principal, seguido de **VSCode** e **Cursor**.
  - Menções isoladas ao Windsurf unificadas junto aos outros editores suportados.
- **Diretriz Anti-Fadiga e Anti-Alucinação (Filtro Factual):**
  - Inserida cláusula estrita em prompts de auditoria (`api.md`, `db.md`) proibindo achados hipotéticos sem evidência factual e separando recomendações cosméticas (`[NIT]`).
- **Prova de Conceito (PoC) & Comando de Verificação nos Achados:**
  - Cada achado de segurança agora inclui obrigatoriamente um comando de reprodução (`curl`, script, query) e um comando de verificação para validar a correção em 1 linha.
- **Regra Inviolável do Teste Travado (*Failing-Test-First*):**
  - Inserida em `tdd_test_driven.md` e `test_suite_generator.md` regra que proíbe expressamente que a IA enfraqueça asserções ou ignore testes para fazê-los passar; a correção deve ser 100% no código de produção.
- **Mapeamento em Memória (Passo Zero):**
  - Adicionada orientação de ordenação mental de dependências antes da escrita física de testes ou código.
- **Modernização do `CLAUDE.md` em `project_context.md`:**
  - Modelo atualizado com diretrizes modernas da Anthropic: regra de sub-1-página, bloco "Como Verificar seu Trabalho (Proof of Done)" com saídas literais esperadas e bloco "Erros Recorrentes (Regra do Erro Repetido)".

## [1.5.0] - 2026-09-02

### Adicionado (Suíte de Testes Unitários com Mocks para Sincronizadores)
- **Bateria de Testes Unitários (`tests/test_sync_scripts.py`):**
  - 12 testes automatizados usando `unittest` e `unittest.mock` da biblioteca padrão.
  - Validação de parsing do padrão OASIS SARIF v2.1.0, checagem de variáveis de ambiente obrigatórias, construção de payloads ricos em Atlassian Document Format (ADF) e Markdown.
  - Testes de algoritmos de deduplicação remota e cache em memória para Jira, GitHub Issues e GitLab Boards.
- **Integração na Bateria Central (`tests/test_integrity.py`):**
  - Adicionado o passo `[6/6]` executando a suíte unitária em CI/CD e localmente.

## [1.4.0] - 2026-09-02

### Adicionado (Sincronização Nativa com GitHub Issues e GitLab Boards)
- **Sincronizador com GitHub Issues (`examples/ci-cd/github_issues_sync.py`):**
  - Script autônomo em Python que consome o arquivo `results.sarif` e cria automaticamente Issues no GitHub para vulnerabilidades Críticas e Altas com zero duplicatas.
  - Formatação rica em GitHub Markdown contendo arquivo, linha, regra OWASP, evidência e labels escopadas (`severity:critical`, `appsec`, `bug`).
- **Sincronizador com GitLab Issues & Boards (`examples/ci-cd/gitlab_issues_sync.py`):**
  - Script autônomo em Python para integração com a API v4 do GitLab, criando issues com scoped labels (`severity::critical`) prontas para os Issue Boards da organização.
- **Workflows Atualizados (`github-actions-audit.yml` & `gitlab-ci-audit.yml`):**
  - Pipelines de clientes configurados com suporte completo a tickets em GitHub Issues, GitLab Boards e Jira.

## [1.3.0] - 2026-09-02

### Adicionado (Integração com Jira REST API v3 para CI/CD)
- **Sincronizador Automático com Jira (`examples/ci-cd/jira_sync.py`):**
  - Script autônomo em Python que consome o arquivo `results.sarif` e cria automaticamente cards no Jira para vulnerabilidades Críticas e Altas com prevenção de duplicatas via JQL.
- **Guia de Configuração (`examples/ci-cd/README.md`):**
  - Documentação completa para geração de tokens no Atlassian e configuração de Secrets de CI/CD.

## [1.2.0] - 2026-09-02

### Adicionado & Aprimorado (Pronto para CI/CD & Modelos para Clientes)
- **Modelos de CI/CD para Clientes (`examples/ci-cd/`):**
  - Adicionado template de **GitHub Actions** (`examples/ci-cd/github-actions-audit.yml`) para execução automática de auditoria de segurança com IA em Pull Requests, publicação de vulnerabilidades no **GitHub Code Scanning via SARIF** e upload do relatório em PDF como artefato de build.
  - Adicionado template de **GitLab CI** (`examples/ci-cd/gitlab-ci-audit.yml`) com integração nativa ao GitLab SAST reports.
- **Esteira de CI/CD do Repositório (`.github/workflows/ci.yml` & `.gitlab-ci.yml`):**
  - Implementado pipeline do GitHub Actions com validação de ShellCheck, bateria de testes de integridade e scanner de segredos (Gitleaks).
  - Corrigido e aprimorado o pipeline do GitLab CI.
- **Bateria de Testes Automatizados de Integridade (`tests/test_integrity.py`):**
  - Script autônomo em Python validando a existência física dos 19 prompts, contrato estrutural de seções obrigatórias, integridade do `install.sh`, referências no `README.md` e testes funcionais de instalação.
- **Inclusões Cirúrgicas do OWASP WSTG v4.2:**
  - Validação de Magic Bytes e anti-path traversal em uploads (`api.md` e `business.md`).
  - Directory / Path Traversal em leitura de arquivos (`api.md`).
  - Server-Side Template Injection / SSTI em SSR (`api.md` e `frontend.md`).
  - Segurança de WebSockets e prevenção de CSWSH (`api.md` e `frontend.md`).
  - Fixação de sessão e mitigação de enumeração de contas (`secrets.md` e `api.md`).

## [1.1.0] - 2026-09-02

### Adicionado & Aprimorado (Alinhamento OWASP ASTF 2023 & OWASP Cheat Sheet Series)
- **Segurança de APIs (`api.md`):** Alinhamento a 16 módulos ASTF 2023, GraphQL, gRPC, LLM APIs e exportação SARIF.
- **Banco de Dados (`db.md`):** Menor privilégio no DB, TLS obrigatório, criptografia de campos sensíveis (KMS) e NoSQL injection.
- **Gestão de Segredos (`secrets.md`):** Padrão ouro Argon2id, Salt+Pepper com KMS, Timing Attacks e Zeroization.
- **Lógica de Negócio (`business.md`):** Chaves de idempotência (`Idempotency-Key`), TOCTOU, HPP e trilhas de auditoria.
- **Modelagem de Ameaças (`threat_modeling.md`):** Manifesto de Threat Modeling e decomposição STRIDE-per-Element.
- **SecDD (`secdd_abuse_cases.md`):** Testes automatizados de invasão, BOLA cross-tenant e concorrência maliciosa.
- **Frontend (`frontend.md`):** Trusted Types API, segurança de `postMessage`, cookies seguros e CSP estrito.
- **Supply Chain (`supply_chain.md`):** OWASP SCVS, geração de SBOM (CycloneDX/SPDX) e anti-slopsquatting.
- **Segurança em CI/CD (`cicd_pipeline.md`):** Hardening de esteiras, OIDC e pinning SHA-256.

## [1.0.0] - 2026-09-01

### Adicionado
- Versão inicial com os 19 prompts estruturados nas categorias Driven Development, Security e DevOps.
