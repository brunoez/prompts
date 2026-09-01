# 🛡️ Suíte de Prompts de Engenharia de Software, AppSec & Yellow Team

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Release](https://img.shields.io/github/v/release/brunoez/prompts?color=blue)](https://github.com/brunoez/prompts/releases/latest)
[![GitHub Stars](https://img.shields.io/github/stars/brunoez/prompts?style=social)](https://github.com/brunoez/prompts)
[![GitLab CI](https://img.shields.io/badge/GitLab%20CI-Passing-22c55e?logo=gitlab)](.gitlab-ci.yml)
[![Language](https://img.shields.io/badge/Language-pt--BR-009c3b.svg)](README.md)

**A biblioteca definitiva de prompts estruturados de auditoria profunda, arquitetura defensiva e metodologias *Driven Development* para desenvolvedores, arquitetos e agentes de Inteligência Artificial.**

[Instalação Rápida](#-instalação-rápida) • [O Ciclo Yellow Team](#-o-ciclo-de-desenvolvimento-seguro-yellow-team-pipeline) • [Qual Prompt Usar?](#-qual-prompt-usar-guia-de-ação-rápida-com-exemplos) • [Catálogo Completo](#-catálogo-completo-de-prompts) • [Contribuição](CONTRIBUTING.md)

</div>

---

## 🇧🇷 Sobre o Projeto

Criado com foco na comunidade brasileira de desenvolvimento e AppSec, este repositório aberto reúne **prompts técnicos de alto nível** projetados para serem executados por Engenheiros Principais ou Agentes de IA (Antigravity, Cursor, Windsurf, Claude Code, GitHub Copilot).

O objetivo é transformar a velocidade do **Vibe Coding** em software de **nível corporativo**: seguro contra vulnerabilidades (OWASP), arquiteturalmente consistente (DDD/SDD), resiliente em produção (SRE) e 100% testado (TDD, BDD, SecDD).

---

## ⚡ Instalação Rápida

Instale a suíte de prompts no seu projeto com um único comando:

```bash
curl -sSL https://raw.githubusercontent.com/brunoez/prompts/main/install.sh | bash
```

> **Dica de IDE:** Por padrão, os prompts são instalados em `.agent/prompts/`. Se você usa **Cursor** ou **Windsurf**:
> ```bash
> # Para Cursor (.cursor/rules):
> curl -sSL https://raw.githubusercontent.com/brunoez/prompts/main/install.sh | bash -s -- . cursor
> 
> # Para Windsurf (.windsurf/rules):
> curl -sSL https://raw.githubusercontent.com/brunoez/prompts/main/install.sh | bash -s -- . windsurf
> 
> # Para todas as ferramentas simultaneamente:
> curl -sSL https://raw.githubusercontent.com/brunoez/prompts/main/install.sh | bash -s -- . all
> ```

---

### 📁 Estrutura de Diretórios Gerada no Projeto

```plaintext
seu-projeto/
├── .agent/prompts/
│   ├── driven-development/
│   │   ├── bdd_behavior_driven.md
│   │   ├── cdd_contract_driven.md
│   │   ├── project_context.md
│   │   ├── sdd_spec_driven.md
│   │   ├── secdd_abuse_cases.md
│   │   ├── tdd_test_driven.md
│   │   ├── test_suite_generator.md
│   │   └── technical_documentation.md
│   ├── security/
│   │   ├── ai_appsec.md
│   │   ├── api.md
│   │   ├── business.md
│   │   ├── db.md
│   │   ├── frontend.md
│   │   ├── secrets.md
│   │   ├── supply_chain.md
│   │   └── threat_modeling.md
│   └── devops/
│       ├── cicd_pipeline.md
│       ├── iac_docker_k8s.md
│       └── resilience_observability.md
├── src/
├── tests/
├── docs/
├── CONTEXT.md
└── CLAUDE.md / .cursorrules
```

---

## 🧭 O Ciclo de Desenvolvimento Seguro (Yellow Team Pipeline)

```mermaid
graph TD
    subgraph F1["1. Arquitetura & Contexto"]
        A["Demanda / Ideia"] --> B0["project_context.md"]
        B0 --> B["sdd_spec_driven.md"]
        B --> C["threat_modeling.md"]
        B --> D["cdd_contract_driven.md"]
        B --> D2["technical_documentation.md"]
    end

    subgraph F2["2. Comportamento & Testes"]
        D2 --> E["bdd_behavior_driven.md"]
        E --> F["secdd_abuse_cases.md"]
        F --> G["tdd_test_driven.md"]
        G --> G2["test_suite_generator.md"]
    end

    subgraph F3["3. Implementação Guiada"]
        G2 --> H["Vibe Coding Guiado"]
        H --> I["supply_chain.md"]
    end

    subgraph F4["4. Auditorias Especializadas"]
        I --> J1["api.md"]
        I --> J2["business.md"]
        I --> J3["db.md"]
        I --> J4["frontend.md"]
        I --> J5["secrets.md"]
        I --> J6["ai_appsec.md"]
    end

    subgraph F5["5. Deploy & Resiliência"]
        J1 --> K1["cicd_pipeline.md"]
        J2 --> K1
        J3 --> K1
        J4 --> K1
        J5 --> K1
        J6 --> K1
        K1 --> K2["iac_docker_k8s.md"]
        K2 --> K3["resilience_observability.md"]
    end
```

---

## 💡 Qual Prompt Usar? (Guia de Ação Rápida com Exemplos)

### 🛡️ 1. Segurança & AppSec

* **Para saber a segurança da API da aplicação (OWASP API Top 10):**
  * **Use:** [`prompts/security/api.md`](prompts/security/api.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/security/api.md]
    Execute a auditoria de APIs neste repositório e gere o relatório em PDF.
    ```

* **Para encontrar fraudes, falhas em regras de negócio e pulo de etapas (checkout/MFA):**
  * **Use:** [`prompts/security/business.md`](prompts/security/business.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/security/business.md]
    Audite as regras de negócio contra fraudes e race conditions (TOCTOU).
    ```

* **Para checar vazamento de senhas, chaves de API e segredos no Git ou `.env`:**
  * **Use:** [`prompts/security/secrets.md`](prompts/security/secrets.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/security/secrets.md]
    Configure o venv, execute o TruffleHog3 e faça a triagem de segredos.
    ```

* **Para auditar a segurança do frontend, SPAs e proteção contra XSS/CSRF:**
  * **Use:** [`prompts/security/frontend.md`](prompts/security/frontend.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/security/frontend.md]
    Audite os componentes frontend contra XSS, vazamento de tokens e CWV.
    ```

* **Para auditar a segurança do banco de dados, concorrência e injeções SQL:**
  * **Use:** [`prompts/security/db.md`](prompts/security/db.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/security/db.md]
    Audite as queries e migrações contra SQLi, N+1 queries e deadlocks.
    ```

* **Para identificar alucinações de pacotes por IA (*Slopsquatting*) e CVEs:**
  * **Use:** [`prompts/security/supply_chain.md`](prompts/security/supply_chain.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/security/supply_chain.md]
    Audite as dependências contra pacotes alucinados e vulnerabilidades SCA.
    ```

* **Para mapear ameaças (STRIDE) e fronteiras de confiança antes de codificar:**
  * **Use:** [`prompts/security/threat_modeling.md`](prompts/security/threat_modeling.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/security/threat_modeling.md]
    Faça a modelagem de ameaças STRIDE para a arquitetura desta aplicação.
    ```

* **Para auditar aplicações que usam IA (LLMs, RAG e Agentes) contra injeção de prompt:**
  * **Use:** [`prompts/security/ai_appsec.md`](prompts/security/ai_appsec.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/security/ai_appsec.md]
    Audite as integrações de IA contra Prompt Injection e Insecure Output.
    ```

---

### 🎯 2. Arquitetura, Contexto & Testes (Driven Developments)

* **Para ensinar o vocabulário do seu negócio à IA e gerar `CONTEXT.md`, `CLAUDE.md` e `.cursorrules`:**
  * **Use:** [`prompts/driven-development/project_context.md`](prompts/driven-development/project_context.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/driven-development/project_context.md]
    Crie o CONTEXT.md com o dicionário do projeto e os arquivos de regras de IA.
    ```

* **Para gerar a documentação técnica completa da aplicação (Stack, C4 Model, DER do Banco e APIs):**
  * **Use:** [`prompts/driven-development/technical_documentation.md`](prompts/driven-development/technical_documentation.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/driven-development/technical_documentation.md]
    Mapeie o projeto e gere o docs/architecture/ARCHITECTURE.md completo.
    ```

* **Para gerar, escrever e rodar a suíte completa de testes (Unitários, Integração e E2E):**
  * **Use:** [`prompts/driven-development/test_suite_generator.md`](prompts/driven-development/test_suite_generator.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/driven-development/test_suite_generator.md]
    Crie os testes que faltam neste projeto e execute até ficarem 100% verdes.
    ```

* **Para planejar uma nova funcionalidade com especificação técnica (SDD) e Schemas Zod:**
  * **Use:** [`prompts/driven-development/sdd_spec_driven.md`](prompts/driven-development/sdd_spec_driven.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/driven-development/sdd_spec_driven.md]
    Crie o Software Design Document e os Schemas Zod para a nova feature.
    ```

* **Para criar testes automáticos de invasão, BOLA/IDOR, Mass Assignment e concorrência:**
  * **Use:** [`prompts/driven-development/secdd_abuse_cases.md`](prompts/driven-development/secdd_abuse_cases.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/driven-development/secdd_abuse_cases.md]
    Escreva testes de abuso simulando invasões e concorrência maliciosa.
    ```

* **Para documentar o comportamento do sistema em Gherkin (`Given/When/Then`):**
  * **Use:** [`prompts/driven-development/bdd_behavior_driven.md`](prompts/driven-development/bdd_behavior_driven.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/driven-development/bdd_behavior_driven.md]
    Modele os fluxos de negócio em arquivos .feature com sintaxe Gherkin.
    ```

* **Para aplicar o ciclo TDD (Red-Green-Refactor) e cobrir casos de borda:**
  * **Use:** [`prompts/driven-development/tdd_test_driven.md`](prompts/driven-development/tdd_test_driven.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/driven-development/tdd_test_driven.md]
    Aplique TDD para criar os testes unitários antes de codificar a lógica.
    ```

* **Para garantir contratos de API entre serviços e frontend sem quebras:**
  * **Use:** [`prompts/driven-development/cdd_contract_driven.md`](prompts/driven-development/cdd_contract_driven.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/driven-development/cdd_contract_driven.md]
    Valide as rotas com a spec OpenAPI e configure testes de contrato Pact.
    ```

---

### ⚙️ 3. DevOps, Infraestrutura & Resiliência

* **Para auditar e proteger a esteira de CI/CD (GitHub Actions / GitLab CI):**
  * **Use:** [`prompts/devops/cicd_pipeline.md`](prompts/devops/cicd_pipeline.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/devops/cicd_pipeline.md]
    Audite os workflows contra script injection e permissões excessivas.
    ```

* **Para checar a segurança do Docker (rootless/multi-stage) e manifestos Kubernetes:**
  * **Use:** [`prompts/devops/iac_docker_k8s.md`](prompts/devops/iac_docker_k8s.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/devops/iac_docker_k8s.md]
    Audite Dockerfiles e K8s garantindo securityContext restrito e limites.
    ```

* **Para auditar filas, mensageria (DLQ), observabilidade (OTel) e estabilidade SRE:**
  * **Use:** [`prompts/devops/resilience_observability.md`](prompts/devops/resilience_observability.md)
  * **Comando:**
    ```markdown
    @[.agent/prompts/devops/resilience_observability.md]
    Audite os workers de fila, configure retry com DLQ e graceful shutdown.
    ```

---

## 📚 Catálogo Completo de Prompts

### 🎯 1. Driven Developments, Contexto & Testes (Guardrails contra Alucinação)

| Prompt | Especialidade | Descrição & Escopo |
| :--- | :--- | :--- |
| [`project_context.md`](prompts/driven-development/project_context.md) | **Engenheiro de Contexto & Onboarding de IA** | Mapeia o vocabulário e regras do projeto e gera os arquivos de contexto para IAs: **`CONTEXT.md`** (glossário de negócio e invariantes), **`CLAUDE.md`**, **`.cursorrules`** e **`.github/copilot-instructions.md`**. |
| [`technical_documentation.md`](prompts/driven-development/technical_documentation.md) | **Arquiteto de Software (Docs-as-Code)** | Mapeia e gera a documentação técnica completa: **Stack & Versões, Diagramas C4 Model, Diagrama ERD do Banco de Dados, Catálogo de Endpoints/Entrypoints, Mensageria, Guia de Onboarding/Setup Local e Deploy/Observabilidade**. |
| [`test_suite_generator.md`](prompts/driven-development/test_suite_generator.md) | **Engenheiro de QA & Test Automation** | Varre a aplicação, identifica código sem testes e **gera, implementa e executa fisicamente** a Pirâmide de Testes completa (Unitários, Integração com Supertest/Testcontainers, E2E com Playwright e carga com K6). |
| [`sdd_spec_driven.md`](prompts/driven-development/sdd_spec_driven.md) | **Spec & Schema-Driven** | Especificação técnica formal prévia (SDD/RFC), Schemas Zod/TypeBox como fonte única da verdade, inferência estrita de tipos e prevenção de *Spec Drift*. |
| [`secdd_abuse_cases.md`](prompts/driven-development/secdd_abuse_cases.md) | **Security-Driven (SecDD)** | Criação de testes automatizados de *Abuse Cases*, simulações de BOLA/IDOR, injeção de Mass Assignment, testes de concorrência em saldo e exaustão de Rate Limit. |
| [`bdd_behavior_driven.md`](prompts/driven-development/bdd_behavior_driven.md) | **Behavior-Driven (BDD)** | Documentação viva em linguagem Gherkin (`.feature`), validação de transições ilegais em máquinas de estado e critérios de aceite executáveis. |
| [`tdd_test_driven.md`](prompts/driven-development/tdd_test_driven.md) | **Test-Driven (TDD)** | Ciclo Red-Green-Refactor, cobertura rigorosa de *Edge Cases*, eliminação de over-mocking e testes determinísticos ultrarrápidos. |
| [`cdd_contract_driven.md`](prompts/driven-development/cdd_contract_driven.md) | **Contract-Driven (CDD)** | OpenAPI, AsyncAPI, validação com Pact (Consumer-Driven Contracts), prevenção de *Breaking Changes* e schema registry de eventos. |

---

### 🛡️ 2. Segurança, Modelagem & AppSec

| Prompt | Especialidade | Descrição & Escopo |
| :--- | :--- | :--- |
| [`threat_modeling.md`](prompts/security/threat_modeling.md) | **Modelagem de Ameaças (STRIDE)** | Mapeamento de fronteiras de confiança (*Trust Boundaries*), diagramas DFD e matriz de contramedidas arquiteturais antes do código. |
| [`supply_chain.md`](prompts/security/supply_chain.md) | **Supply Chain & SCA** | Prevenção contra **alucinação de pacotes por IA (*Slopsquatting*)**, scripts maliciosos de `postinstall`, integridade de lockfiles e CVEs. |
| [`api.md`](prompts/security/api.md) | **OWASP API Security Top 10** | BOLA/IDOR, BFA, Mass Assignment, Rate Limiting, Timeouts, Circuit Breakers e vazamento de dados em APIs. |
| [`business.md`](prompts/security/business.md) | **Business Logic Flaws** | Manipulação de preço/quantidade, pulo de etapas no checkout (*skip-step*), inconsistência de estados e race conditions (TOCTOU). |
| [`db.md`](prompts/security/db.md) | **Banco de Dados & Concorrência** | Limites DDD, prevenção de Dual Write, N+1 queries, índices, locks pessimistas/otimistas, deadlocks e SQLi. |
| [`frontend.md`](prompts/security/frontend.md) | **Frontend & SPAs** | XSS, CSRF, Open Redirect, armazenamento inseguro de sessão, vazamento no bundle, CSP, SRI e Core Web Vitals. |
| [`secrets.md`](prompts/security/secrets.md) | **Gestão de Segredos & TruffleHog3** | Scanner automatizado com `trufflehog3` em venv isolado, triagem de falsos positivos e auditoria de `.env` e histórico git. |
| [`ai_appsec.md`](prompts/security/ai_appsec.md) | **Aplicações de IA (OWASP LLM)** | Injeção direta/indireta de prompt, Insecure Output Handling, Excessive Agency e isolamento de tenants em RAG/vetores. |

---

### ⚙️ 3. DevOps, Infraestrutura & Confiabilidade (SRE)

| Prompt | Especialidade | Descrição & Escopo |
| :--- | :--- | :--- |
| [`cicd_pipeline.md`](prompts/devops/cicd_pipeline.md) | **Hardening de CI/CD (DevSecOps)** | Prevenção de script injection em GitHub Actions/GitLab CI, autenticação OIDC com nuvem e pinning de actions por SHA256. |
| [`iac_docker_k8s.md`](prompts/devops/iac_docker_k8s.md) | **IaC, Containers & K8s** | Terraform IAM least privilege, Docker rootless e multi-stage, K8s securityContext, NetworkPolicies e Probes. |
| [`resilience_observability.md`](prompts/devops/resilience_observability.md) | **Resiliência & Observabilidade** | Mensageria assíncrona, Dead Letter Queues (DLQ), Circuit Breakers, tracing distribuído com OpenTelemetry e Graceful Shutdown. |

---

## 📊 Entregáveis Padrão Gerados pelos Prompts

Todos os prompts são padronizados para entregar:
1. **Matriz de Priorização no Terminal:** Tabela com ordenação por Severidade x Esforço e chips de **Quick Wins**.
2. **Detalhamento Completo dos Achados:** Arquivo/linha, evidência, impacto real e código corrigido pronto.
3. **Relatório em PDF com Gráficos:** Salvo na pasta `docs/<modulo>-audit/`, com design profissional (paleta `#B91C1C` Crítica, `#EA580C` Alta, `#D97706` Média, `#2563EB` Baixa, `#059669` Pontos Fortes).
4. **Issues Formatadas para GitHub/GitLab:** Blocos em Markdown prontos para copiar com critérios de aceite verificáveis.

---

## 🤝 Como Contribuir

Contribuições da comunidade brasileira e internacional são muito bem-vindas!
* Leia nosso [Guia de Contribuição (CONTRIBUTING.md)](CONTRIBUTING.md) para entender o padrão de criação de novos prompts.
* Consulte o [Código de Conduta](CODE_OF_CONDUCT.md).
* Reporte vulnerabilidades de acordo com a [Política de Segurança (SECURITY.md)](SECURITY.md).

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja [`LICENSE`](LICENSE) para mais informações.

<div align="center">
Desenvolvido com 💚 para a comunidade de tecnologia brasileira por <a href="https://github.com/brunoez">@brunoez</a>
</div>
