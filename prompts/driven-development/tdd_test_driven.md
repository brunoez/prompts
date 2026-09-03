# PROMPT DE AUDITORIA E ENGENHARIA: TEST-DRIVEN DEVELOPMENT (TDD), COBERTURA RIGOROSA E PREVENÇÃO DE ALUCINAÇÃO

## OBJETIVO
Atuar como Engenheiro Principal de Software e Especialista em Testes Automatizados (Yellow Team). Sua missão é auditar e aplicar a disciplina de **Test-Driven Development (TDD)** no repositório, garantindo que o ciclo **Red $\rightarrow$ Green $\rightarrow$ Refactor** seja rigorosamente aplicado em todo o desenvolvimento acelerado (*Vibe Coding*). O foco é blindar a aplicação contra alucinações de código, regressões silenciosas, mock drifts e falta de tratamento de casos de borda (*Edge Cases*).

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Testes Unitários/Issues para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todos os arquivos de teste da aplicação e os arquivos de código-fonte correspondentes (`src/` vs `tests/`).
2. Identifique os relatórios de cobertura de código existentes (`coverage/`, `lcov.info`, cobertura de branches e statements).
3. Identifique e analise a estratégia de dublês de teste (Mocks, Stubs, Spies, Fakes, In-Memory DBs).
4. Você DEVE ler e analisar cada arquivo de teste e função crítica, verificando se os testes validam o comportamento real da unidade ou apenas "enganam" a métrica de cobertura.
5. **Regra Inviolável do Bugfix (Failing-Test-First & Teste Travado):** Para cada bug reportado ou nova regra: (1) Escreva primeiro o teste de regressão que reproduz o problema e execute-o comprovando que ele falha (RED); (2) O teste está formalmente travado — é estritamente proibido alterar o arquivo de teste, enfraquecer asserções (`expect`), pular (`it.skip`) ou injetar mocks vazios para fazê-lo passar; (3) A correção deve ser implementada exclusivamente no código de produção até que a suíte passe integralmente (GREEN).

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (TEST-DRIVEN DEVELOPMENT)

### 1. Rigor do Ciclo Red-Green-Refactor & Testes de Unidade
- [ ] **Testes Isolados e Determinísticos:** Verifique se os testes unitários são totalmente independentes de rede, banco externo ou ordem de execução, rodando de forma ultrarrápida em memória.
- [ ] **Cobertura Efetiva de Casos de Borda (Edge Cases):** Identifique se as funções matemáticas, conversores, formatadores e parsers possuem testes para valores nulos (`null`/`undefined`), strings vazias, caracteres Unicode especiais, limites numéricos (`MAX_SAFE_INTEGER`, `-Infinity`, `NaN`) e arrays vazios.
- [ ] **Padrão AAA (Arrange, Act, Assert):** Verifique se os testes estão estruturados de forma legível e modular dividindo claramente a preparação de dados (*Arrange*), a execução da função (*Act*) e as validações estritas (*Assert*).
- [ ] **Um Conceito Lógico por Teste:** Identifique testes inflados que testam múltiplos comportamentos não correlacionados no mesmo bloco `it()` / `test()`.

### 2. Qualidade dos Dublês de Teste e Prevenção de Mock Drift
- [ ] **Ausência de Over-Mocking:** Identifique testes que mockam tantas dependências internas que acabam testando apenas o mock e não o código real, permitindo que bugs em produção passem despercebidos.
- [ ] **Prevenção de Mock Drift:** Verifique se os mocks de interfaces e clientes de terceiros implementam rigorosamente as mesmas tipagens/interfaces TypeScript/Python que o cliente real, detectando quebras de contrato em tempo de build.
- [ ] **Limpeza de Estado entre Testes:** Verifique se ganchos de limpeza (`afterEach(() => vi.clearAllMocks())` ou `jest.restoreAllMocks()`) estão configurados para impedir vazamento de estado entre testes.

### 3. Testes de Integração e Camadas de Infraestrutura
- [ ] **Testes de Repositório com Banco Real/Isolado:** Verifique se as consultas de banco de dados (SQL nativo ou ORM) são validadas com instâncias de banco efêmeras (Testcontainers, SQLite em memória ou esquemas de teste isolados), garantindo que constraints e tipos reais do banco sejam testados.
- [ ] **Testes de Integração de Middlewares e Pipeline HTTP:** Verifique se interceptadores, middlewares de autenticação, log e tratamento global de erros são testados de ponta a ponta via Supertest ou clientes HTTP locais.

### 4. Cobertura de Branches e Prevenção de Regressões
- [ ] **Cobertura de Branches (Caminhos de Decisão):** Identifique blocos condicionais (`if/else`, `switch/case`, `try/catch`) com baixa cobertura, onde apenas o fluxo principal foi testado e o tratamento de erro foi ignorado.
- [ ] **Testes de Regressão Automatizados:** Verifique se cada bug reportado no passado possui um teste automatizado correspondente que reproduz o problema e garante que ele nunca volte a ocorrer.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/utils/calc.ts:22` | Edge Case Não Testado (Divisão por zero) | ALTA | Baixo (10 min) | **SIM** |
| #2 | `src/services/auth.test.ts:45` | Over-Mocking em Autenticação | MÉDIA | Médio (45 min) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema de TDD / Teste Frágil]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [Edge Cases / Over-Mocking / Branch Coverage / Flaky Test / AAA Pattern]
- **Problema:** Explicação direta da fragilidade do teste e o risco de falha em produção.
- **Evidência:** Código do teste atual ou função não coberta.
- **Código do Teste TDD Recomendado:** Implementação completa do teste unitário/integração.
- **Comando de Verificação (Proof of Green):** Comando literal (`npm test ...` ou `pytest ...`) para executar exclusivamente este teste, garantindo que ele execute de forma determinística e com 100% de sucesso.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/tdd-audit/relatorio-auditoria-tdd.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria TDD e Qualidade de Testes — <nome do projeto>", data, métricas gerais de cobertura e escopo auditado.
b) **Resumo Executivo:** Total de lacunas de teste por severidade, gráfico de rosca de cobertura de branches e gráfico de barras por módulo.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (módulos bem testados e determinísticos) e **Pontos Fracos** (código frágil ou dependente de over-mocking).
d) **Tabela de Achados Detalhados:** Severidade | Arquivo/Função | Risco de Regressão Mapeado.
e) **Diretrizes de TDD para o Time:** Guia prático para guiar a IA e desenvolvedores no ciclo Red-Green-Refactor.
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada lacuna de teste crítica, a issue formatada para o GitHub com o código de teste sugerido.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`).
- Deixe o script gerador salvo no diretório `docs/tdd-audit/`.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/tdd-audit/relatorio-auditoria-tdd.pdf`, `docs/tdd-audit/generate_report.py`).
