# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico (SemVer)](https://semver.org/lang/pt-BR/).

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
