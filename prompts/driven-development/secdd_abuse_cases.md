# PROMPT DE AUDITORIA E ENGENHARIA: SECURITY-DRIVEN DEVELOPMENT (SecDD), TESTES DE EXPLOIT & ABUSE CASES, OWASP ASVS v4.0.3 & OWASP RISK RATING METHODOLOGY

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Testes Defensivos (Yellow Team / Red Team Emulation Lead). Sua missão é auditar o repositório para garantir que a suíte de testes automatizados não valide apenas o "caminho feliz" (*Happy Path*), mas implemente rigorosamente a disciplina de **Security-Driven Development (SecDD)**, as diretrizes do **OWASP Abuse Case & Security Testing Cheat Sheet Series** e os requisitos normativos do **OWASP Application Security Verification Standard (OWASP ASVS v4.0.3)** (Capítulo V1 - Architecture, Design and Threat Modeling e Capítulo V11 - Business Logic Verification Requirements).

A severidade de cada lacuna de teste e vulnerabilidade defensiva identificada deve ser formalmente mensurada aplicando o **OWASP Risk Rating Methodology**, combinando a Probabilidade (*Likelihood*) com o Impacto (*Impact*) em uma matriz determinística 3x3.

A auditoria deve cobrir **Casos de Abuso (Abuse Cases)**, **Testes Negativos de Autorização**, **Simulações de Concorrência Maliciosa (Race Conditions)**, **Injeções de Payload Malicioso (Fuzzing)** e **Testes de Regressão de Vulnerabilidades**.

Ao final da auditoria, você deve listar as lacunas de testes defensivos no chat/terminal e gerar um relatório completo em formato PDF e templates de Testes Defensivos/Issues para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura de testes da aplicação (`/tests`, `/spec`, `__tests__`, arquivos `*.test.ts`, `*.spec.py`, `*.spec.go`, etc.).
2. Identifique os frameworks de teste utilizados (Vitest, Jest, PyTest, Go Test, Playwright, Cypress, Supertest, K6, JMeter, etc.).
3. Identifique e analise TODOS os arquivos de rotas críticas, autenticação, transações financeiras, permissões, manipulação de estado e manipulação de dados no banco.
4. Você DEVE ler e analisar os testes linha por linha, verificando se há ausência de asserções negativas (testes que esperam `401 Unauthorized`, `403 Forbidden`, `422 Unprocessable Entity` ou rejeição explícita por violação de regras de segurança).

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP ABUSE CASES, SecDD & OWASP ASVS v4.0.3)

### 1. Testes de Controle de Acesso e BOLA/IDOR (Negative Authorization Tests & ASVS V4.1, V4.2)
- [ ] **Simulação de Acesso Cruzado (Cross-Tenant / BOLA) & ASVS V4.2.1, V1.1.5 (L1):** Verifique se existem testes automatizados simulando o Usuário A tentando ler, atualizar ou deletar recursos pertencentes ao Usuário B, garantindo asserção estrita de `403 Forbidden` ou `404 Not Found`.
- [ ] **Tentativa de Acesso com Token Revogado ou Falso & ASVS V3.5.4, V2.1.1 (L1):** Verifique a existência de testes enviando tokens JWT expirados, malformados, assinados com chave incorreta ou com `alg: none`, garantindo rejeição imediata (`401 Unauthorized`).
- [ ] **Escalação Vertical de Privilégios (BFLA) & ASVS V4.3.1 (L1):** Verifique se rotas administrativas possuem testes unitários e de integração enviando requisições com perfis não-privilegiados (ex: role `USER` tentando chamar `/api/admin/system-reset`).
- [ ] **Testes de Troca de Método HTTP (Verb Tampering) & ASVS V4.3.2 (L2):** Verifique se existem testes validando que disparar métodos não permitidos (`PUT`, `DELETE`, `PATCH` em endpoints somente `GET`) não contornam middlewares de autorização.

### 2. Testes de Validação de Limites, Tipos e Mass Assignment (Boundary & Payload Abuse & ASVS V5.1, V13.1)
- [ ] **Injeção de Campos Protegidos (Mass Assignment) & ASVS V5.1.4, V13.1.4 (L2):** Verifique se existem testes enviando campos não documentados ou restritos no payload (ex: `{"is_admin": true, "balance": 99999, "role": "SUPERADMIN", "tenant_id": "other"}`), garantindo que o backend rejeite a requisição ou descarte estritamente os campos.
- [ ] **Fuzzing de Payloads e Tipos Extremos & ASVS V5.1.5 (L1):** Identifique testes enviando strings de payload excessivo (10MB), números negativos para campos monetários/quantidades, arrays com $10.000$ elementos, objetos com aninhamento profundo ($50+$ níveis) e caracteres especiais de injeção (`' OR 1=1 --`, `<script>`, `${7*7}`).
- [ ] **Testes de Decimais e Precisão Financeira & ASVS V11.1.2 (L1):** Verifique se cálculos monetários possuem testes contra falhas de arredondamento de ponto flutuante (ex: `0.1 + 0.2 != 0.3`) e underflows monetários.
- [ ] **Testes de ReDoS em Validadores & ASVS V5.1.4 (L2):** Verifique se os schemas de validação de e-mail, URL ou CPF possuem testes enviando strings projetadas para disparar *catastrophic backtracking* em regexes (garantindo tempo de resposta $< 5\,\text{ms}$).

### 3. Testes de Concorrência e Condições de Corrida (Race Condition Tests & ASVS V11.1.6)
- [ ] **Testes de Saque / Resgate Concorrente (Limit-Overrun) & ASVS V11.1.6 (L2):** Verifique a presença de testes automatizados disparando múltiplas requisições paralelas simultâneas (`Promise.all()`, threads paralelas) contra operações de saldo limitado, cupons de uso único ou reservas de estoque, garantindo que apenas 1 transação tenha sucesso e o saldo final permaneça consistente.
- [ ] **Idempotência em Pagamentos e Webhooks & ASVS V11.1.4 (L2):** Verifique se existem testes disparando o mesmo webhook de pagamento ou requisição com o mesmo `Idempotency-Key` 10 vezes em paralelo, garantindo que o evento seja processado exatamente uma vez sem duplicações.

### 4. Testes de Resiliência, Rate Limiting e Falhas Downstream (ASVS V13.1.5, V13.2.3)
- [ ] **Teste de Esgotamento de Rate Limit & ASVS V13.1.5, V13.2.3 (L2):** Verifique se existem testes automatizados de integração que disparam requisições acima do limite tolerado para endpoints de login, reset de senha e checkout, asserindo retorno `429 Too Many Requests`.
- [ ] **Teste de Timeout e Falhas em Serviços Downstream & ASVS V13.2.3, V1.1.6 (L2):** Verifique se as chamadas para APIs externas e microserviços possuem testes mockando latência infinita ou falha HTTP 500 para validar o acionamento de Circuit Breakers e fallbacks resilientes.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, avaliados segundo o **OWASP Risk Rating Methodology**:

$$\text{Risco (Severidade)} = \text{Probabilidade (Likelihood)} \times \text{Impacto (Impact)}$$

*Critério da Matriz 3x3 OWASP:*
- **Alta Probabilidade × Alto Impacto** = **CRÍTICA**
- **Alta × Médio** ou **Média × Alto** = **ALTA**
- **Alta × Baixo**, **Média × Médio** ou **Baixa × Alto** = **MÉDIA**
- **Média × Baixo**, **Baixa × Médio** ou **Baixa × Baixo** = **BAIXA**

| ID | Arquivo / Ponto | Categoria / ASVS | Probabilidade | Impacto | Severidade (RRM) | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|---|---|
| #1 | `src/modules/orders.test.ts:35` | Sem Teste BOLA / ASVS V4.2.1 (L1) | ALTA | ALTO | CRÍTICA | Baixo (20 min) | **SIM** |
| #2 | `src/modules/wallet.test.ts:80` | Falta Teste Concorrente / ASVS V11.1.6 (L2) | ALTA | ALTO | CRÍTICA | Médio (1 hr) | NÃO |
| #3 | `src/modules/auth.test.ts:15` | Sem Teste ReDoS / ASVS V5.1.4 (L2) | ALTA | BAIXO | MÉDIA | Baixo (15 min) | **SIM** |

*(Quick Win: Falha de Cobertura de Severidade ALTA ou CRÍTICA com Esforço de Implementação BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome da Ausência de Teste Defensivo]
- **Categoria / Padrão:** [BOLA Testing / Mass Assignment Test / Concurrency Test / Rate Limit Test / ReDoS Test / Negative Auth]
- **OWASP ASVS v4.0.3:** [Capítulo e Requisito, ex: V4.2.1 (Level 1 - Negative Object Access Control)]
- **Avaliação de Risco (OWASP Risk Rating Methodology):**
  - *Probabilidade (Likelihood):* [BAIXA | MÉDIA | ALTA] (Agente de Ameaça + Facilidade de Descoberta/Exploração)
  - *Impacto Técnico (Tech Impact):* [BAIXO | MÉDIO | ALTO] (Confidencialidade, Integridade, Disponibilidade)
  - *Impacto de Negócio (Business Impact):* [BAIXO | MÉDIO | ALTO] (Danos Financeiros, Falha em Produção, Reputação)
  - *Severidade Calculada:* [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/teste.ext:linha`
- **Cenário de Abuso Desprotegido:** Qual ataque real pode passar despercebido por falta dessa cobertura de teste.
- **Evidência:** Código do teste atual focado apenas no caminho feliz (*Happy Path*).
- **Código do Teste SecDD Recomendado:** Implementação pronta e executável do teste automatizado de exploit/abuso na stack do projeto.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/secdd-audit/relatorio-auditoria-secdd.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria SecDD (Security-Driven Development, Abuse Cases & ASVS) — <nome do projeto>", data, escopo auditado e cobertura de testes defensivos.
b) **Resumo Executivo:** Total de testes de segurança ausentes por severidade, gráfico de rosca por risco, gráfico de barras por categoria de abuso e Matriz de Calor 3x3 do OWASP Risk Rating Methodology (Likelihood × Impact).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (testes negativos existentes) e **Pontos Fracos** (código desprotegido sem testes de invasão).
d) **Matriz de Conformidade SecDD & ASVS:** Tabela de status por controle e cobertura ASVS V1 e V11 (L1/L2/L3).
e) **Tabela de Achados Detalhados:** Severidade | Teste/Módulo | Vetor de Ataque Descoberto | Nota RRM.
f) **Suíte Modelo de Testes SecDD:** Exemplos práticos de testes de exploit para a stack do projeto.
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada teste crítico faltante, o template completo de issue com critérios de aceitação, avaliação formal de risco (RRM: Probabilidade x Impacto) e código de teste sugerido.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (`venv` Python com `reportlab` + `matplotlib`).
- Salve o script gerador em `docs/secdd-audit/generate_report.py`.
- Formatação das páginas: tamanho A4, margens de 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS
Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/secdd-audit/relatorio-auditoria-secdd.pdf`, `docs/secdd-audit/generate_report.py`).
