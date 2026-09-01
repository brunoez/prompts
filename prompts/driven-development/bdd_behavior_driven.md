# PROMPT DE AUDITORIA E ENGENHARIA: BEHAVIOR-DRIVEN DEVELOPMENT (BDD), DOCUMENTAÇÃO VIVA & TESTES DE COMPORTAMENTO

## OBJETIVO
Atuar como Engenheiro Principal de Qualidade de Software e Especialista em Engenharia de Requisitos (Yellow Team). Sua missão é auditar e consolidar a prática de **Behavior-Driven Development (BDD)** no repositório, garantindo que as regras de negócio complexas, fluxos de domínio, restrições financeiras e máquinas de estado estejam documentadas em linguagem ubíqua e executável (arquivos `.feature` em sintaxe **Gherkin: Given/When/Then**), eliminando ambiguidades entre negócio, segurança e código gerado por IA (*Vibe Coding*).

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Cenários BDD/Issues para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todos os arquivos de especificação de comportamento existentes (`.feature`, `/specs`, `/e2e`, `/cucumber`, `*.steps.ts`, `steps.py`, etc.).
2. Identifique a biblioteca/framework de execução BDD suportado (Cucumber, Vitest-Cucumber, Playwright-BDD, pytest-bdd, Behave, Godog, SpecFlow).
3. Identifique e analise os arquivos de domínio central da aplicação (carrinho, checkout, assinaturas, autenticação multi-etapas, concessão de crédito, máquina de estados).
4. Você DEVE ler e analisar os cenários BDD existentes, verificando se há divergência entre a documentação viva e a implementação real no código (*Behavior Drift*).

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (BEHAVIOR-DRIVEN DEVELOPMENT)

### 1. Clareza e Estrutura dos Cenários (Sintaxe Gherkin & Regras de Negócio)
- [ ] **Aderência ao Padrão Given-When-Then:** Verifique se os cenários seguem estritamente a separação entre Contexto (*Given*), Ação disparada (*When*) e Resultado esperado (*Then*), evitando passos imperativos com detalhes excessivos de interface gráfica (ex: evitar `When I click on button with id #submit_btn_2`).
- [ ] **Linguagem Ubíqua de Negócio (Domain Language):** Verifique se os termos utilizados nos arquivos `.feature` refletem fielmente a terminologia dos especialistas de domínio (ex: "Cliente Elegível", "Saldo Bloqueado", "Pedido Concluído"), e não termos de banco de dados ou programação (`SELECT`, `DTO`, `HTTP 200`).
- [ ] **Uso Adequado de Scenario Outlines / Tabelas de Exemplos:** Verifique se fluxos com múltiplas combinações de dados e regras de cálculo utilizam `Scenario Outline` e tabelas de `Examples`, cobrindo faixas de valores válidos e inválidos.

### 2. Cobertura de Máquinas de Estado e Transições Inválidas
- [ ] **Cenários de Transição Válida de Estado:** Verifique se todos os estados permitidos do domínio possuem cenários que atestam a progressão correta (ex: `CRIADO` $\rightarrow$ `PAGO` $\rightarrow$ `ENVIADO` $\rightarrow$ `ENTREGUE`).
- [ ] **Cenários de Rejeição de Transições Proibidas:** Verifique se existem cenários explícitos testando tentativas de transições ilegais (ex: *Given* um pedido no estado "CANCELADO", *When* o webhook de pagamento tentar marcá-lo como "PAGO", *Then* a operação deve ser rejeitada com erro de inconsistência de estado).
- [ ] **Cenários de Cancelamento e Estorno:** Verifique se fluxos compensatórios (estornos parciais, cancelamento de reservas, expiração de vouchers) estão cobertos por cenários BDD completos.

### 3. Automação dos Step Definitions e Isolamento
- [ ] **Ausência de Steps Pendentes / Órfãos:** Identifique steps Gherkin declarados nos arquivos `.feature` que não possuem implementação de código correspondente (*Undefined Step Definitions*).
- [ ] **Reutilização de Step Definitions:** Verifique se steps comuns de autenticação e criação de entidades são reutilizados entre diferentes features, evitando duplicação de lógica de teste.
- [ ] **Isolamento de Dados em Execução BDD:** Garanta que cada cenário execute em um contexto isolado de dados (usando bancos de dados em memória, transações revertidas ao final ou identificadores dinâmicos `UUID`), impedindo que a execução de um cenário afete o próximo.

### 4. Sincronização entre BDD, Código e Critérios de Aceite
- [ ] **Prevenção de Behavior Drift:** Identifique se alterações recentes na lógica de negócio foram feitas no código sem a devida atualização dos arquivos `.feature`.
- [ ] **Integração com a Esteira de CI/CD:** Verifique se os testes BDD são executados automaticamente nos pull requests como critério bloqueante de qualidade.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `features/checkout.feature:14` | Transição Inválida Não Coberta | ALTA | Baixo (30 min) | **SIM** |
| #2 | `features/billing.feature` | Step Definitions Órfãos | MÉDIA | Médio (1 hr) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema de BDD]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/da/feature.feature:linha`
- **Categoria:** [Gherkin Quality / State Machine Coverage / Orphan Steps / Behavior Drift]
- **Problema:** Explicação direta da ambiguidade ou risco de regra de negócio desprotegida.
- **Evidência:** Cenário atual incompleto ou ausência de cobertura.
- **Cenário Gherkin / Step Definition Recomendado:** Implementação pronta do arquivo `.feature` e do código do step.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/bdd-audit/relatorio-auditoria-bdd.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria BDD (Behavior-Driven Development) — <nome do projeto>", data, escopo de funcionalidades auditadas e status da documentação viva.
b) **Resumo Executivo:** Total de regras de negócio sem cobertura formal BDD, gráfico de rosca de maturidade de cenários e gráfico de barras por domínio de negócio.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (cenários BDD robustos existentes) e **Pontos Fracos** (regras implícitas sem documentação viva).
d) **Tabela de Achados Detalhados:** Severidade | Domínio | Falha de Comportamento Mapeada.
e) **Especificação Viva Consolidada:** Exemplos dos principais fluxos modelados em Gherkin.
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada cenário faltante, o template completo de issue contendo os critérios de aceitação em formato Gherkin.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`).
- Deixe o script gerador salvo no diretório `docs/bdd-audit/`.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/bdd-audit/relatorio-auditoria-bdd.pdf`, `docs/bdd-audit/generate_report.py`).
