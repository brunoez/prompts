# PROMPT DE AUDITORIA E ENGENHARIA: SECURITY-DRIVEN DEVELOPMENT (SecDD), TESTES DE EXPLOIT & ABUSE CASES

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Testes Defensivos (Yellow Team / Red Team Emulation Lead). Sua missão é auditar o repositório para garantir que a suíte de testes automatizados não valide apenas o "caminho feliz" (*Happy Path*), mas implemente rigorosamente a disciplina de **Security-Driven Development (SecDD)** e as diretrizes do **OWASP Abuse Case & Security Testing Cheat Sheet Series**.

A auditoria deve cobrir **Casos de Abuso (Abuse Cases)**, **Testes Negativos de Autorização**, **Simulações de Concorrência Maliciosa (Race Conditions)**, **Injeções de Payload Malicioso (Fuzzing)** e **Testes de Regressão de Vulnerabilidades**.

Ao final da auditoria, você deve listar as lacunas de testes defensivos no chat/terminal e gerar um relatório completo em formato PDF e templates de Testes Defensivos/Issues para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura de testes da aplicação (`/tests`, `/spec`, `__tests__`, arquivos `*.test.ts`, `*.spec.py`, `*.spec.go`, etc.).
2. Identifique os frameworks de teste utilizados (Vitest, Jest, PyTest, Go Test, Playwright, Cypress, Supertest, K6, JMeter, etc.).
3. Identifique e analise TODOS os arquivos de rotas críticas, autenticação, transações financeiras, permissões, manipulação de estado e manipulação de dados no banco.
4. Você DEVE ler e analisar os testes linha por linha, verificando se há ausência de asserções negativas (testes que esperam `401 Unauthorized`, `403 Forbidden`, `422 Unprocessable Entity` ou rejeição explícita por violação de regras de segurança).

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP ABUSE CASES & SecDD)

### 1. Testes de Controle de Acesso e BOLA/IDOR (Negative Authorization Tests)
- [ ] **Simulação de Acesso Cruzado (Cross-Tenant / BOLA):** Verifique se existem testes automatizados simulando o Usuário A tentando ler, atualizar ou deletar recursos pertencentes ao Usuário B, garantindo asserção estrita de `403 Forbidden` ou `404 Not Found`.
- [ ] **Tentativa de Acesso com Token Revogado ou Falso:** Verifique a existência de testes enviando tokens JWT expirados, malformados, assinados com chave incorreta ou com `alg: none`, garantindo rejeição imediata (`401 Unauthorized`).
- [ ] **Escalação Vertical de Privilégios (BFLA):** Verifique se rotas administrativas possuem testes unitários e de integração enviando requisições com perfis não-privilegiados (ex: role `USER` tentando chamar `/api/admin/system-reset`).
- [ ] **Testes de Troca de Método HTTP (Verb Tampering):** Verifique se existem testes validando que disparar métodos não permitidos (`PUT`, `DELETE`, `PATCH` em endpoints somente `GET`) não contornam middlewares de autorização.

### 2. Testes de Validação de Limites, Tipos e Mass Assignment (Boundary & Payload Abuse)
- [ ] **Injeção de Campos Protegidos (Mass Assignment):** Verifique se existem testes enviando campos não documentados ou restritos no payload (ex: `{"is_admin": true, "balance": 99999, "role": "SUPERADMIN", "tenant_id": "other"}`), garantindo que o backend rejeite a requisição ou descarte estritamente os campos.
- [ ] **Fuzzing de Payloads e Tipos Extremos:** Identifique testes enviando strings de payload excessivo (10MB), números negativos para campos monetários/quantidades, arrays com $10.000$ elementos, objetos com aninhamento profundo ($50+$ níveis) e caracteres especiais de injeção (`' OR 1=1 --`, `<script>`, `${7*7}`).
- [ ] **Testes de Decimais e Precisão Financeira:** Verifique se cálculos monetários possuem testes contra falhas de arredondamento de ponto flutuante (ex: `0.1 + 0.2 != 0.3`) e underflows monetários.
- [ ] **Testes de ReDoS em Validadores:** Verifique se os schemas de validação de e-mail, URL ou CPF possuem testes enviando strings projetadas para disparar *catastrophic backtracking* em regexes (garantindo tempo de resposta $< 5\,\text{ms}$).

### 3. Testes de Concorrência e Condições de Corrida (Race Condition Tests)
- [ ] **Testes de Saque / Resgate Concorrente (Limit-Overrun):** Verifique a presença de testes automatizados disparando múltiplas requisições paralelas simultâneas (`Promise.all()`, threads paralelas) contra operações de saldo limitado, cupons de uso único ou reservas de estoque, garantindo que apenas 1 transação tenha sucesso e o saldo final permaneça consistente.
- [ ] **Idempotência em Pagamentos e Webhooks:** Verifique se existem testes disparando o mesmo webhook de pagamento ou requisição com o mesmo `Idempotency-Key` 10 vezes em paralelo, garantindo que o evento seja processado exatamente uma vez sem duplicações.

### 4. Testes de Resiliência, Rate Limiting e Falhas Downstream
- [ ] **Teste de Esgotamento de Rate Limit:** Verifique se existem testes automatizados de integração que disparam requisições acima do limite tolerado para endpoints de login, reset de senha e checkout, asserindo retorno `429 Too Many Requests`.
- [ ] **Teste de Timeout e Falhas em Serviços Downstream:** Verifique se as chamadas para APIs externas e microserviços possuem testes mockando latência infinita ou falha HTTP 500 para validar o acionamento de Circuit Breakers e fallbacks resilientes.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/modules/orders/orders.test.ts:35` | Ausência de Teste BOLA/IDOR | CRÍTICA | Baixo (20 min) | **SIM** |
| #2 | `src/modules/wallet/wallet.test.ts:80` | Falta de Teste Concorrente | ALTA | Médio (1 hr) | NÃO |
| #3 | `src/modules/auth/validators.test.ts:15` | Ausência de Teste ReDoS | MÉDIA | Baixo (15 min) | **SIM** |

*(Quick Win: Falha de Cobertura de Severidade ALTA ou CRÍTICA com Esforço de Implementação BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome da Ausência de Teste Defensivo]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/teste.ext:linha`
- **Categoria:** [BOLA Testing / Mass Assignment Test / Concurrency Test / Rate Limit Test / ReDoS Test / Negative Auth]
- **Cenário de Abuso Desprotegido:** Qual ataque real pode passar despercebido por falta dessa cobertura de teste.
- **Evidência:** Código do teste atual focado apenas no caminho feliz (*Happy Path*).
- **Código do Teste SecDD Recomendado:** Implementação pronta e executável do teste automatizado de exploit/abuso na stack do projeto.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/secdd-audit/relatorio-auditoria-secdd.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria SecDD (Security-Driven Development & Abuse Cases) — <nome do projeto>", data, escopo auditado e cobertura de testes defensivos.
b) **Resumo Executivo:** Total de testes de segurança ausentes por severidade, gráfico de rosca por risco e gráfico de barras por categoria de abuso.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (testes negativos existentes) e **Pontos Fracos** (código desprotegido sem testes de invasão).
d) **Tabela de Achados Detalhados:** Severidade | Teste/Módulo | Vetor de Ataque Descoberto.
e) **Suíte Modelo de Testes SecDD:** Exemplos práticos de testes de exploit para a stack do projeto.
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada teste crítico faltante, o template completo de issue com critérios de aceitação e código de teste sugerido.

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
