# SDD & BDD IMPLEMENTATION PLAN: INTEGRAÇÃO OWASP ASVS v4.0.3 & OWASP RISK RATING METHODOLOGY (RRM)

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrar formalmente os padrões **OWASP ASVS v4.0.3** (requisitos e níveis L1/L2/L3) e o **OWASP Risk Rating Methodology** (cálculo de risco Likelihood × Impact) em todos os 13 prompts de segurança e no prompt de SecDD/Abuse Cases, **sem substituir nenhum programa, framework ou controle OWASP existente** (preservação aditiva estrita de 100% do acervo atual).

**Architecture:** Abordagem de enriquecimento estritamente aditivo (*Strictly Additive Enrichment*). Nenhum padrão existente (OWASP API Top 10 2023, ASTF, WSTG v4.2, Proactive Controls 2024, Cheat Sheets, LLM Top 10) será removido ou substituído. O ASVS e o Risk Rating coexistem e fortalecem os controles atuais: cada checklist mantém seus códigos originais e recebe o mapeamento ASVS correspondente, a matriz de priorização recebe colunas de Probabilidade e Impacto, e o detalhamento do achado ganha o score formal de risco e os códigos normativos do ASVS.

**Tech Stack:** Markdown (Prompts), Python 3.10+ (Integrity Tests & Report Generator), Gherkin / BDD, ReportLab, Matplotlib, SARIF v2.1.0.

**Spec:** Este documento consolida a especificação de engenharia de software (SDD) e os cenários de comportamento (BDD) descritos abaixo.

---

## ⚠️ DIRETRIZ INEGOCIÁVEL: PRINCÍPIO DA NÃO-SUBSTITUIÇÃO (ENRIQUECIMENTO ADITIVO)

> [!IMPORTANT]
> **NENHUM PROGRAMA OU PADRÃO OWASP EXISTENTE PODE SER REMOVIDO OU SUBSTITUÍDO.**
> - Em [`prompts/security/api.md`](file:///home/bruno/Projetos/prompts/prompts/security/api.md), o **OWASP API Security Top 10 2023**, o **OWASP ASTF** e o **OWASP WSTG v4.2** NÃO serão substituídos. Eles continuam exatamente onde estão, sendo enriquecidos com os requisitos do **OWASP ASVS v4.0.3 (V13, V1, V14)** e a avaliação de risco do **OWASP Risk Rating Methodology**.
> - Em [`prompts/security/authn_identity.md`](file:///home/bruno/Projetos/prompts/prompts/security/authn_identity.md), o **OWASP Proactive Controls C7**, as **OWASP Cheat Sheets** e o **WSTG** continuam intactos, somando-se ao **ASVS V2 e V3**.
> - Em [`prompts/security/db.md`](file:///home/bruno/Projetos/prompts/prompts/security/db.md), o **OWASP Database Security Cheat Sheet Series** continua intacto, somando-se ao **ASVS V5, V8 e V6**.
> - Esta regra de **coexistência e soma** aplica-se rigorosamente a TODOS os 14 arquivos da suíte.

---

## 1. ESPECIFICAÇÃO DE SOFTWARE (SDD - SPEC-DRIVEN DEVELOPMENT)

### 1.1 Metas (Goals)
1. **Adição Normativa do OWASP ASVS v4.0.3 (Coexistência):** Associar a cada um dos 13 prompts de `prompts/security/` e a `prompts/driven-development/secdd_abuse_cases.md` os seus respectivos capítulos do ASVS (V1 a V14) e Níveis de Verificação (**L1, L2, L3**), posicionando os requisitos ASVS lado a lado com os padrões já existentes (ex: `ASTF-API1 & ASVS V13.1.1 (L2)`).
2. **Adição do OWASP Risk Rating Methodology (RRM):** Incorporar o cálculo formal de risco da OWASP:
   $$\text{Risco Geral} = \text{Probabilidade (Likelihood)} \times \text{Impacto (Impact)}$$
   mantendo a compatibilidade com a priorização de Quick Wins preexistente.
3. **Preservação Integral do Conteúdo Existente:** Nenhuma linha, checklist, código WSTG, código ASTF, recomendação de Cheat Sheet, regra anti-alucinação ou instrução de entrega atual poderá ser deletada ou substituída.
4. **Enriquecimento dos Entregáveis Automatizados:**
   - **PDF:** Especificação de inclusão do Heatmap 3x3 de Risco OWASP e da Matriz de Conformidade ASVS mantendo os gráficos existentes.
   - **SARIF v2.1.0:** Inclusão de tags `ASVS-V*.` e propriedades de score de risco sem romper a estrutura v2.1.0 existente.
   - **GitHub Issues:** Inclusão de campos estruturados de justificativa de Probabilidade e Impacto mantendo os templates existentes.
5. **Garantia de Qualidade Contínua (CI Gate):** Adicionar verificação automatizada no script `tests/test_integrity.py` assegurando que tanto os padrões originais quanto os novos (ASVS e RRM) estão presentes em 100% dos prompts de segurança.

### 1.2 Não-Metas (Non-Goals)
1. **PROIBIDO:** Substituir ou suprimir o OWASP API Top 10 2023, ASTF, WSTG v4.2, Proactive Controls, Cheat Sheets ou OWASP Top 10 for LLM.
2. Não alterar prompts de Driven-Development ou DevOps não focados em segurança defensiva (ex: `bdd_behavior_driven.md`, `tdd_test_driven.md`).
3. Não alterar a sintaxe ou nomes das seções obrigatórias (`## OBJETIVO`, `## ESCOPO`, `## SAÍDA`, `## ENTREGÁVEIS`).

### 1.3 Mapeamento de Coexistência: Padrões Atuais + OWASP ASVS v4.0.3

| Arquivo do Prompt | Padrões Atuais (MANTIDOS 100%) | Novo Padrão Adicionado: OWASP ASVS v4.0.3 |
| :--- | :--- | :--- |
| `security/api.md` | OWASP API Top 10 2023, ASTF, WSTG v4.2 | **ASVS V13** (API & Web Service), **V1** (Architecture), **V14** (Config) |
| `security/authn_identity.md` | OWASP Proactive C7, WSTG, Cheat Sheets | **ASVS V2** (Authentication), **V3** (Session Management) |
| `security/access_control.md` | OWASP Proactive C6, BOLA/BFLA, WSTG | **ASVS V4** (Access Control Verification) |
| `security/input_validation.md`| OWASP Proactive C4/C5, XSS/SSTI Cheat Sheets | **ASVS V5** (Validation, Sanitization and Encoding) |
| `security/db.md` | OWASP Database Security Cheat Sheets, SQLi | **ASVS V5** (SQLi), **V8** (Data Protection), **V6** (Crypto) |
| `security/frontend.md` | OWASP Proactive C3/C4, DOM XSS, CSP | **ASVS V5** (Output Encoding/XSS), **V3** (Client Session), **V14** |
| `security/business.md` | OWASP WSTG-BUSL, Anti-Fraud Guidelines | **ASVS V11** (Business Logic Verification) |
| `security/secrets.md` | OWASP Proactive C8, Cryptographic Storage | **ASVS V6** (Stored Cryptography), **V8** (Data Protection) |
| `security/secure_config.md` | OWASP Proactive C1/C2, Secure Headers, Logging | **ASVS V7** (Logging/Errors), **V9** (Communications/TLS), **V14** |
| `security/ssrf.md` | OWASP SSRF Prevention Cheat Sheet, WSTG | **ASVS V12** (File & Resources - SSRF Protection), **V5** |
| `security/supply_chain.md` | OWASP Software Component Verification (SCVS), SCA | **ASVS V10** (Malicious Code), **V14** (Third-Party Components) |
| `security/threat_modeling.md`| STRIDE, DFD, Threat Modeling Guide | **ASVS V1** (Architecture, Design and Threat Modeling) |
| `security/ai_appsec.md` | OWASP Top 10 for LLM Applications 2025 | **ASVS V1** (Modelagem), **V5** (Validação), **V10** (Código Malicioso) |
| `driven-development/secdd_abuse_cases.md` | OWASP Abuse Case Cheat Sheet | **ASVS V1** (Architecture) e **V11** (Business Logic Testing) |

---

## 2. ESPECIFICAÇÃO DE COMPORTAMENTO (BDD - BEHAVIOR-DRIVEN DEVELOPMENT)

### Feature 1: Preservação de Padrões Existentes e Coexistência com ASVS e RRM
```gherkin
Feature: Coexistência e Preservação Estrita dos Padrões OWASP Existentes
  Como Engenheiro de AppSec e Mantenedor da Base de Prompts
  Quero garantir que nenhum programa OWASP existente seja substituído
  Para que a auditoria se torne mais rica sem perder referências históricas e específicas

  Scenario: Preservação integral do OWASP API Top 10 e ASTF no prompt de API
    Given o prompt "prompts/security/api.md"
    When o arquivo for atualizado
    Then os códigos "ASTF-API1" até "ASTF-API10" devem permanecer integralmente preservados
    And as referências ao "OWASP API Security Top 10 2023" e "WSTG v4.2" devem permanecer ativas
    And o padrão "OWASP ASVS" (Capítulos V13, V1 e V14) deve ser adicionado em coexistência
    And a metodologia "OWASP Risk Rating Methodology" deve ser adicionada para o cálculo de severidade

  Scenario Outline: Preservação de padrões originais e adição de ASVS em todos os prompts
    Given o prompt "<prompt_path>"
    When o conteúdo for analisado após a atualização
    Then todos os checklists originais devem continuar presentes
    And o capítulo correspondente "<asvs_chapter>" do OWASP ASVS deve estar presente
    And o cálculo do OWASP Risk Rating Methodology deve estar documentado

    Examples:
      | prompt_path | asvs_chapter |
      | prompts/security/api.md | ASVS V13 |
      | prompts/security/authn_identity.md | ASVS V2 |
      | prompts/security/access_control.md | ASVS V4 |
      | prompts/security/input_validation.md | ASVS V5 |
      | prompts/security/db.md | ASVS V5 |
      | prompts/security/frontend.md | ASVS V5 |
      | prompts/security/business.md | ASVS V11 |
      | prompts/security/secrets.md | ASVS V6 |
      | prompts/security/secure_config.md | ASVS V14 |
      | prompts/security/ssrf.md | ASVS V12 |
      | prompts/security/supply_chain.md | ASVS V14 |
      | prompts/security/threat_modeling.md | ASVS V1 |
      | prompts/security/ai_appsec.md | ASVS V5 |
      | prompts/driven-development/secdd_abuse_cases.md | ASVS V11 |
```

### Feature 2: Matriz de Risco do OWASP Risk Rating Methodology (RRM)
```gherkin
Feature: Cálculo Formal de Severidade com Matriz 3x3 do OWASP Risk Rating
  Como Especialista em AppSec
  Quero que cada achado reporte Probabilidade (Likelihood) e Impacto (Impact)
  Para que a severidade seja calculada deterministicamente pela matriz oficial OWASP

  Scenario Outline: Cálculo de Severidade na Matriz de Risco 3x3
    Given uma vulnerabilidade com probabilidade "<probabilidade>"
    And com impacto combinado "<impacto>"
    When a severidade é calculada pela matriz OWASP Risk Rating
    Then a severidade deve ser "<severidade>"

    Examples:
      | probabilidade | impacto | severidade |
      | ALTA          | ALTO    | CRÍTICA    |
      | ALTA          | MÉDIO   | ALTA       |
      | ALTA          | BAIXO   | MÉDIA      |
      | MÉDIA         | ALTO    | ALTA       |
      | MÉDIA         | MÉDIO   | MÉDIA      |
      | MÉDIA         | BAIXO   | BAIXA      |
      | BAIXA         | ALTO    | MÉDIA      |
      | BAIXA         | MÉDIO   | BAIXA      |
      | BAIXA         | BAIXO   | BAIXA      |
```

### Feature 3: Automação Contínua e Integridade (CI Gate)
```gherkin
Feature: Validação Automatizada de Integridade dos Padrões
  Como Desenvolvedor de CI/CD
  Quero que o script "tests/test_integrity.py" valide os padrões existentes e os novos
  Para evitar regressões ou esquecimento de normas

  Scenario: Suíte de Integridade Executa com Sucesso
    Given que todos os 14 prompts receberam ASVS e RRM sem perda de conteúdo anterior
    When o script "python3 tests/test_integrity.py" for executado
    Then todas as checagens devem retornar sucesso (código de saída 0)
    And o teste de conformidade de padrões de segurança deve certificar os 14 prompts
```

---

## 3. PLANO DE TAREFAS DETALHADO (BITE-SIZED IMPLEMENTATION TASKS)

### Task 1: Expandir `tests/test_integrity.py` com Validador de Padrões Existentes + ASVS + Risk Rating
**Files:**
- Modify: `tests/test_integrity.py`
**Interfaces:**
- Produces: Teste `test_security_prompts_standards()` que checa nos 14 prompts:
  1. Presença dos padrões originais (ex: ASTF em `api.md`, Proactive C7 em `authn_identity.md`, etc.).
  2. Presença de `OWASP ASVS`.
  3. Presença de `OWASP Risk Rating Methodology`.
- [x] **Step 1: Implementar o teste em `tests/test_integrity.py`.**
- [x] **Step 2: Executar para confirmar falha esperada (Red) antes das adições.**

### Task 2: Atualização do Prompt Central de API (`prompts/security/api.md`)
**Files:**
- Modify: `prompts/security/api.md`
**Interfaces:**
- Mantém: 100% de ASTF-API1 a API10, WSTG v4.2, regras anti-alucinação.
- Adiciona: ASVS V13/V1/V14, colunas de Probabilidade e Impacto na tabela, bloco de risco RRM nos achados e relatórios (PDF com heatmap de risco, SARIF com tags ASVS, Issues com score).
- [x] **Step 1: Adicionar ASVS v4.0.3 e OWASP Risk Rating ao objetivo e escopo mantendo integralmente o ASTF e WSTG.**
- [x] **Step 2: Adicionar requisitos ASVS correspondentes em cada item do checklist de API (ex: `ASTF-API1 & ASVS V13.1.1 (L2)`).**
- [x] **Step 3: Expandir a tabela de priorização com Probabilidade e Impacto (RRM) e enriquecer o modelo de achados.**
- [x] **Step 4: Atualizar instruções de PDF, SARIF e Issues para incluir o Heatmap de Risco e tags ASVS.**

### Task 3: Atualização dos Prompts de Autenticação e Autorização (`authn_identity.md` e `access_control.md`)
**Files:**
- Modify: `prompts/security/authn_identity.md` (Mantém Proactive C7 + Cheat Sheets + WSTG; Adiciona ASVS V2/V3 + RRM)
- Modify: `prompts/security/access_control.md` (Mantém Proactive C6 + BOLA/BFLA; Adiciona ASVS V4 + RRM)
- [x] **Step 1: Enriquecer `authn_identity.md` sem remover controles existentes.**
- [x] **Step 2: Enriquecer `access_control.md` sem remover controles existentes.**

### Task 4: Atualização dos Prompts de Dados, Validação e Segredos (`db.md`, `input_validation.md`, `secrets.md`)
**Files:**
- Modify: `prompts/security/db.md` (Mantém Database Security Cheat Sheets + Concorrência; Adiciona ASVS V5/V8/V6 + RRM)
- Modify: `prompts/security/input_validation.md` (Mantém Proactive C4/C5 + Schemas; Adiciona ASVS V5 + RRM)
- Modify: `prompts/security/secrets.md` (Mantém Proactive C8 + Crypto; Adiciona ASVS V6/V8 + RRM)
- [x] **Step 1: Enriquecer `db.md`.**
- [x] **Step 2: Enriquecer `input_validation.md`.**
- [x] **Step 3: Enriquecer `secrets.md`.**

### Task 5: Atualização dos Prompts de Rede, Configuração e Frontend (`ssrf.md`, `secure_config.md`, `frontend.md`)
**Files:**
- Modify: `prompts/security/ssrf.md` (Mantém SSRF Cheat Sheet + WSTG; Adiciona ASVS V12/V5 + RRM)
- Modify: `prompts/security/secure_config.md` (Mantém Proactive C1/C2 + Hardening; Adiciona ASVS V7/V9/V14 + RRM)
- Modify: `prompts/security/frontend.md` (Mantém Proactive C3/C4 + DOM XSS + CSP; Adiciona ASVS V5/V3/V14 + RRM)
- [x] **Step 1: Enriquecer `ssrf.md`.**
- [x] **Step 2: Enriquecer `secure_config.md`.**
- [x] **Step 3: Enriquecer `frontend.md`.**

### Task 6: Atualização dos Prompts de Negócio, Supply Chain, Modelagem, IA e SecDD
**Files:**
- Modify: `prompts/security/business.md` (Mantém WSTG-BUSL; Adiciona ASVS V11 + RRM)
- Modify: `prompts/security/supply_chain.md` (Mantém SCVS + SCA; Adiciona ASVS V10/V14 + RRM)
- Modify: `prompts/security/threat_modeling.md` (Mantém STRIDE + DFD; Adiciona ASVS V1 + RRM)
- Modify: `prompts/security/ai_appsec.md` (Mantém OWASP Top 10 for LLM 2025; Adiciona ASVS V1/V5/V10 + RRM)
- Modify: `prompts/driven-development/secdd_abuse_cases.md` (Mantém Abuse Cases + SecDD; Adiciona ASVS V1/V11 + RRM)
- [x] **Step 1: Enriquecer `business.md` e `supply_chain.md`.**
- [x] **Step 2: Enriquecer `threat_modeling.md` e `ai_appsec.md`.**
- [x] **Step 3: Enriquecer `secdd_abuse_cases.md`.**

### Task 7: Execução da Bateria Completa de Testes de Integridade (Green)
- [x] **Step 1: Executar `python3 tests/test_integrity.py` e certificar 100% de aprovação em todos os testes.**
- [x] **Step 2: Verificar que todos os instaladores (`install.sh`), documentações e links permanecem íntegros.**
