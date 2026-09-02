# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico (SemVer)](https://semver.org/lang/pt-BR/).

## [1.1.1] - 2026-09-02

### Adicionado (Inclusões Cirúrgicas do OWASP WSTG v4.2)
- **Validação de Uploads Seguros de Arquivos (`api.md` & `business.md` - WSTG-BUSL-08/09):**
  - Inclusão de checagem obrigatória de Magic Bytes reais, sanitização de nome com UUID contra Path Traversal (`../../`) e isolamento de storage.
- **Directory / Path Traversal em I/O (`api.md` - WSTG-ATHZ-01):**
  - Checagem de confinamento de diretório raiz em leituras locais de arquivo (`fs.readFile`, `res.sendFile`, `open()`).
- **Server-Side Template Injection / SSTI (`api.md` & `frontend.md` - WSTG-INPV-18):**
  - Detecção de interpolação de strings não sanitizadas no corpo de templates de e-mail e renderização no servidor (SSR).
- **Segurança de WebSockets & CSWSH (`api.md` & `frontend.md` - WSTG-CLNT-10):**
  - Validação de cabeçalho `Origin` no handshake de WebSocket para mitigar Cross-Site WebSocket Hijacking.
- **Session Fixation & Account Enumeration (`secrets.md` & `api.md` - WSTG-SESS-03 / IDNT-04):**
  - Regeneração obrigatória de Session ID após login e tempos/mensagens homogêneas em endpoints de autenticação.
- **CORS Dynamic Regex Hardening (`api.md` - WSTG-CLNT-07):**
  - Prevenção de bypass de CORS por regexes com pontos não escapados em validações dinâmicas de origem.

## [1.1.0] - 2026-09-02

### Adicionado & Aprimorado (Alinhamento OWASP ASTF 2023 & OWASP Cheat Sheet Series)
- **Segurança de APIs (`api.md`):**
  - Alinhamento 100% à suíte de 16 módulos do **OWASP API Security Testing Framework (ASTF)** e **OWASP API Security Top 10 2023**.
  - Auditoria especializada para **GraphQL** (Introspecção, Query Depth/Complexity, Batching), **gRPC** (Reflection, Auth Interceptors), **LLM/AI Endpoints** (Prompt Injection, Unbounded Tool Calling) e **ReDoS**.
  - Matriz de testes de autorização cruzada com dois tokens para eliminação de falsos negativos em BOLA e BFLA.
  - Detecção de *OpenAPI Drift* e *Shadow/Zombie APIs* (ASTF-API9).
  - Suporte à geração de relatórios no padrão **SARIF v2.1.0** para integração nativa com o GitHub Code Scanning.
- **Banco de Dados & Concorrência (`db.md`):**
  - Incorporação do *OWASP Database Security*, *SQLi Prevention*, *NoSQL Injection* e *Database Access Control Cheat Sheets*.
  - Princípio do Menor Privilégio no DB (detecção de conexões com superusuários vs roles DML segregadas).
  - Enforcement obrigatório de TLS (`sslmode=verify-full`), criptografia de campos sensíveis em repouso (Field-Level Encryption / KMS) e auditoria de procedures dinâmicas.
- **Gestão de Segredos & Criptografia (`secrets.md`):**
  - Incorporação do *OWASP Password Storage* e *Secrets Management Cheat Sheets*.
  - Padrão ouro para hashing de senhas: `Argon2id` ($\ge 64\,\text{MB}$, 3 iterações, 4 threads), `scrypt`, `bcrypt` ($\ge 12$) ou `PBKDF2` ($\ge 600.000$ iterações), com banimento de `MD5`/`SHA-1`/`SHA-256` cru.
  - Arquitetura de Salt CSPRNG + Pepper gerenciado em cofre KMS e prevenção contra *Timing Attacks* (`crypto.timingSafeEqual`).
- **Lógica de Negócio & Integridade (`business.md`):**
  - Incorporação do *OWASP Business Logic Security* e *Transaction Authorization Cheat Sheets*.
  - Chaves de idempotência (`Idempotency-Key`) e locks distribuídos contra *double charges*.
  - Proteção contra manipulação de preços/quantidades, poluição de parâmetros HTTP (HPP), ataques de repetição temporal e ausência de trilhas de auditoria imutáveis.
- **Modelagem de Ameaças (`threat_modeling.md`):**
  - Incorporação do *OWASP Threat Modeling Cheat Sheet* e do Manifesto de Threat Modeling (As 4 Perguntas Fundamentais).
  - Decomposição formal **STRIDE-per-Element** (Processo, Armazenamento, Fluxo e Entidade Externa), mapeamento de *Trust Boundaries* e scoring CVSS/DREAD.
- **Security-Driven Development & Abuse Cases (`secdd_abuse_cases.md`):**
  - Incorporação do *OWASP Abuse Case Cheat Sheet* e testes defensivos automatizados.
  - Testes negativos de autorização cruzada (Cross-Tenant BOLA), simulações de concorrência maliciosa (*Limit-Overrun*) e testes de ReDoS em validadores.
- **Frontend & SPAs (`frontend.md`):**
  - Incorporação do *OWASP Client-Side Security*, *DOM-based XSS*, *CSP* e *Clickjacking Cheat Sheets*.
  - Suporte à **Trusted Types API** (`require-trusted-types-for 'script'`), validação de `window.postMessage`, prefixos de cookies seguros (`__Host-` e `__Secure-`) e mitigação de *Client-Side Prototype Pollution*.
- **Supply Chain & Dependências (`supply_chain.md`):**
  - Incorporação do **OWASP SCVS** (*Software Component Verification Standard*) e *Vulnerable Dependency Management*.
  - Geração e conformidade de SBOM (**CycloneDX** e **SPDX**), prevenção de *Dependency Confusion*, detecção de alucinação de pacotes (*Slopsquatting*) e builds determinísticos com `--ignore-scripts`.
- **Segurança em CI/CD (`cicd_pipeline.md`):**
  - Incorporação do *OWASP CI/CD Security Cheat Sheet*.
  - Prevenção de script injection via contextos de workflow, autenticação via **OIDC**, pinning imutável de Actions por **Full Commit SHA-256** e isolamento de runners.

## [1.0.0] - 2026-09-01

### Adicionado
- **Driven Development Prompts:**
  - `project_context.md` (Contexto, Dicionário do Projeto & Regras para IAs: CONTEXT.md, CLAUDE.md, Cursor).
  - `sdd_spec_driven.md` (Spec-Driven & Schema-Driven Development).
  - `technical_documentation.md` (Documentação Técnica Completa, Docs-as-Code, C4 Model & DER).
  - `test_suite_generator.md` (Engenharia e Geração Completa da Pirâmide de Testes).
  - `secdd_abuse_cases.md` (Security-Driven Development & Abuse Cases).
  - `bdd_behavior_driven.md` (Behavior-Driven Development & Gherkin).
  - `tdd_test_driven.md` (Test-Driven Development & Red-Green-Refactor).
  - `cdd_contract_driven.md` (Contract-Driven Development & Pact/OpenAPI).
- **Security & AppSec Prompts:**
  - `api.md` (OWASP API Security Top 10).
  - `business.md` (Business Logic Flaws & TOCTOU).
  - `db.md` (Banco de Dados, Concorrência & Limites DDD).
  - `frontend.md` (Client-Side Security & SPAs).
  - `secrets.md` (Gestão de Segredos & TruffleHog3 Scanner).
  - `supply_chain.md` (Software Supply Chain Security & Anti-Slopsquatting).
  - `threat_modeling.md` (Threat Modeling & STRIDE Framework).
  - `ai_appsec.md` (OWASP Top 10 for LLMs / GenAI Security).
- **DevOps & Resiliência:**
  - `cicd_pipeline.md` (Pipeline Security & DevSecOps Hardening).
  - `iac_docker_k8s.md` (IaC, Containers & Kubernetes Hardening).
  - `resilience_observability.md` (SRE, OpenTelemetry & Mensageria).
- **Governança & Open Source:**
  - Padrão GitLab CI (`.gitlab-ci.yml`), templates de issue e merge request (`.gitlab/`).
  - Padrão GitHub (`.github/`), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE` (MIT).
  - Instalador automatizado `install.sh` via curl ou clone local.
