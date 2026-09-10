# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico (SemVer)](https://semver.org/lang/pt-BR/).

## [1.8.0] - 2026-09-10

### Adicionado & Aprimorado (Cobertura Completa do OWASP Top 10 Proactive Controls 2024)

Fechamento das lacunas da suíte frente aos [OWASP Top 10 Proactive Controls (2024)](https://top10proactive.owasp.org/) e à [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/).

- **Novos prompts de auditoria em `prompts/security/`:**
  - **`authn_identity.md` (C7 – Secure Digital Identities):** hashing de senha (`Argon2id`), comparação em tempo constante, anti-enumeração, regeneração de sessão (*Session Fixation*), atributos de cookie, MFA/2FA + backup codes, JWT (rejeição de `alg:none`, validação de `iss`/`aud`/`exp`, rotação e revogação de refresh token), OAuth2/OIDC com Authorization Code + PKCE, `state`/`nonce` e allow-list de `redirect_uri`, e fluxos de reset/verificação de conta sem *Account Takeover*.
  - **`access_control.md` (C1 – Implement Access Control / A01:2021):** *deny-by-default*, centralização da decisão de autorização, *enforcement* server-side, IDOR/BOLA com checagem de titularidade e escopo na query (RLS), escalada vertical/BFLA, bypass por verbo HTTP, isolamento multi-tenant, testes negativos de autorização e *fail closed*.
  - **`ssrf.md` (C10 – Stop SSRF / A10:2021):** mapa de *sinks* de saída (webhooks, HTML→PDF, proxies de imagem, `$ref` remoto, XXE), *allow-list* de destino, validação pós-resolução DNS + *pinning* (anti DNS rebinding), bloqueio de faixas privadas/link-local, proteção do endpoint de metadata de nuvem (`169.254.169.254`, IMDSv2), *egress filtering* e tratamento de resposta anti-exfiltração.
  - **`secure_config.md` (C5 – Secure by Default / A05:2021):** estado default seguro, debug/stack traces desligados em produção, ausência de credenciais padrão, headers defensivos (`HSTS`, `CSP`, `X-Content-Type-Options`, `frame-ancestors`, `Referrer-Policy`, `Permissions-Policy`), CORS com *allow-list* estrita, atributos de cookie + CSRF, TLS 1.2+/1.3 obrigatório e *hardening* de container.
  - **`input_validation.md` (C3 – Validate Input & Handle Exceptions):** validação positiva (*allow-list*) em toda fronteira de confiança (incluindo consumidores de fila e webhooks), canonicalização Unicode antes da validação, schema estrito anti *Mass Assignment*, deserialização segura (XXE, *zip slip*, *zip bomb*, *formula injection*), parametrização de *sinks* e tratamento centralizado de exceções sem vazamento de stack trace.
- **Estendido — `devops/resilience_observability.md` (C9 – Security Logging & Monitoring):**
  - Nova seção **"Logging de Segurança e Monitoramento de Detecção"**: eventos de segurança auditados com contexto, redação obrigatória de segredos/PII em todos os *appenders*, integridade e retenção de logs *append-only*, prevenção de *Log Injection* (CR/LF), vocabulário de eventos padronizado, regras de alerta acionáveis e monitoramento da disponibilidade do próprio *pipeline* de logs.
- **Documentação (`README.md`):**
  - Nova seção **"🧭 Cobertura vs OWASP Top 10 Proactive Controls (2024)"** com matriz C1–C10 → prompt(s) responsável(is) → Cheat Sheets aplicados.
  - Catálogo de Segurança e árvore de diretórios atualizados com os 5 novos prompts.
- **Validação Automatizada (`tests/test_integrity.py` & `install.sh`):**
  - Registro dos 5 novos prompts em `EXPECTED_PROMPTS` e `PROMPT_FILES` (catálogo total: **24 prompts**).
  - Contagem de prompts na bateria de testes passou a ser dinâmica (`len(EXPECTED_PROMPTS)`), eliminando *drift* de números fixos.

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
