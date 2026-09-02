# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico (SemVer)](https://semver.org/lang/pt-BR/).

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
