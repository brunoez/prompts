# PROMPT DE ENGENHARIA E GERAÇÃO COMPLETA DE TESTES: PIRÂMIDE DE TESTES, AUTOMAÇÃO & COBERTURA

## OBJETIVO
Atuar como Engenheiro Principal de QA (Quality Assurance) e Especialista em Automação de Testes. Sua missão é realizar uma varredura completa no repositório, mapear todos os módulos, controllers, services, utilitários e componentes que carecem de cobertura, e **gerar, implementar e executar fisicamente uma suíte de testes automatizados de ponta a ponta**, cobrindo todas as camadas da **Pirâmide de Testes (Unitários, Integração, E2E e Carga)**.

Ao final da execução, você DEVE rodar os testes no terminal, garantir que todos passem com sucesso (100% Green), exibir o resumo de cobertura e gerar um relatório completo em formato PDF e templates de GitHub/GitLab Issues para débitos técnicos remanescentes.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique a stack de desenvolvimento e frameworks de teste disponíveis (ex: Vitest, Jest, PyTest, Go Test, Playwright, Cypress, Supertest, Testcontainers, K6).
2. Se nenhum framework de teste estiver configurado no projeto, identifique a stack e sugira/configure o framework mais moderno e leve para o ambiente (ex: Vitest para TypeScript/Node, PyTest para Python).
3. Identifique todos os arquivos de código-fonte (`src/`, `app/`, `lib/`, `controllers/`, `services/`, `utils/`) e mapeie quais possuem ou não arquivos de teste correspondentes (`*.test.ts`, `*.spec.py`, etc.).
4. Você DEVE ler e analisar cada arquivo que receberá testes linha por linha, compreendendo os fluxos felizes (*Happy Paths*), casos de borda (*Edge Cases*), exceções e chamadas assíncronas.

---

## DIRETRIZES DE IMPLEMENTAÇÃO POR CAMADA DE TESTE

### 1. Testes de Unidade (Unit Tests - Base da Pirâmide)
- [ ] **Padrão AAA (Arrange, Act, Assert):** Estruture cada teste de forma limpa, isolando a preparação de dados (*Arrange*), a chamada do método (*Act*) e a verificação estrita do retorno ou efeito colateral (*Assert*).
- [ ] **Cobertura Extensiva de Casos de Borda (Edge Cases):** Crie testes para entradas nulas (`null`/`undefined`), strings vazias, valores numéricos extremos (`0`, negativos, limites de precisão), arrays vazios e caracteres especiais.
- [ ] **Isolamento e Mocks Determinísticos:** Isole dependências externas (APIs de terceiros, relógio do sistema, filesystem) usando mocks estritos e tipados (`vi.mock()`, `unittest.mock`), evitando testes lentos ou instáveis (*Flaky Tests*).
- [ ] **Tratamento de Exceções:** Garanta que cada bloco `try/catch` e lançamento de erro personalizado (`throw new DomainError()`) possua um teste verificando a mensagem e o tipo exato da exceção.

### 2. Testes de Integração (Integration Tests - Meio da Pirâmide)
- [ ] **Testes de Controladores HTTP e Rotas:** Utilize bibliotecas como Supertest, Hono Client ou FastAPI TestClient para disparar requisições HTTP reais contra os endpoints, validando headers, status codes (`200`, `201`, `400`, `401`, `403`, `404`, `422`, `500`) e schemas do payload de resposta.
- [ ] **Testes de Repositório com Banco de Dados Isolado:** Teste queries SQL nativas, migrações e operações ORM (Prisma, Drizzle, SQLAlchemy) contra instâncias efêmeras de banco (SQLite em memória, Testcontainers Docker ou schemas de teste dedicados).
- [ ] **Testes de Middlewares e Pipeline de Autenticação:** Valide o comportamento dos middlewares de autenticação, extração de sessão, rate limit e tratamento global de erros em cadeia.

### 3. Testes Ponta a Ponta (End-to-End / E2E Tests - Topo da Pirâmide)
- [ ] **Fluxos Críticos do Usuário:** Para aplicações com interface visual ou APIs públicas, implemente testes E2E (Playwright, Cypress) para os fluxos vitais do negócio:
  - Cadastro de Usuário $\rightarrow$ Confirmação de E-mail $\rightarrow$ Login;
  - Seleção de Produto $\rightarrow$ Carrinho $\rightarrow$ Checkout $\rightarrow$ Recibo;
  - Recuperação de Senha $\rightarrow$ Troca de Senha $\rightarrow$ Novo Login.
- [ ] **Resiliência a Mudanças de UI:** Utilize seletores semânticos e orientados a acessibilidade (ex: `getByRole`, `getByLabel`, `getByTestId`) em vez de seletores frágeis de CSS/XPath.

### 4. Testes de Carga e Performance (Load & Smoke Tests - Opcional/Recomendado)
- [ ] **Scripts K6 / Artillery:** Crie scripts de teste de carga para simular requisições concorrentes em endpoints críticos (ex: 50 a 500 VUs simultâneos em login ou checkout), validando p95 de latência e taxa de erro < 1%.

---

## FLUXO DE EXECUÇÃO DO PROMPT

1. **Passo Zero — Mapeamento e Ordenação em Memória:** Antes de criar qualquer arquivo físico, mapeie internamente a hierarquia de dependências e ordene a implementação (camadas base/schemas primeiro, depois serviços de domínio, depois controllers/rotas de integração). Garanta que os comandos de teste da stack existam e sejam executáveis em uma linha.
2. **Diagnóstico Inicial:** Liste no terminal a tabela de arquivos existentes vs arquivos de teste faltantes.
3. **Geração dos Arquivos de Teste:** Escreva os arquivos de teste diretamente no repositório nos caminhos padronizados (ex: `src/services/auth.service.test.ts` ou `tests/integration/orders.test.ts`), aplicando testes determinísticos e evitando over-mocking.
4. **Execução e Prova Literal (Proof of Green):** Execute a suíte de testes no terminal do projeto e apresente a saída literal:
   ```bash
   # Exemplo Node/TypeScript:
   npm test -- --run --coverage
   # Exemplo Python:
   pytest --cov=src tests/
   ```
5. **Correção Automática e Proibição de Relaxar Asserções:** Se algum teste falhar, analise a causa raiz. Se o código de produção possuir um defeito, corrija o código de produção — nunca enfraqueça o teste nem mascare falhas com mocks artificiais para forçar aprovação. Reexecute até obter 100% de sucesso real.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a criação e execução dos testes, exiba no chat a tabela consolidada de cobertura e novos testes criados:

### PARTE 1: RESUMO DA SUÍTE DE TESTES GERADA

| Módulo / Camada | Arquivo de Teste Criado | Tipo de Teste | Qtd. Testes | Status |
|---|---|---|---|---|
| Autenticação | `tests/unit/auth.service.test.ts` | Unitário | 12 | ✅ PASS |
| Pedidos | `tests/integration/orders.api.test.ts` | Integração | 8 | ✅ PASS |
| Checkout | `tests/e2e/checkout.spec.ts` | E2E | 3 | ✅ PASS |

### PARTE 2: MÉTRICAS DE COBERTURA (COVERAGE)
Apresente os índices de cobertura obtidos após a execução:
- **Statements (Declarações):** [XX%]
- **Branches (Caminhos condicionais):** [XX%]
- **Functions (Funções):** [XX%]
- **Lines (Linhas):** [XX%]

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA EXECUÇÃO, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/tests-audit/relatorio-cobertura-testes.pdf`, contendo:

a) **Capa:** Título "Relatório de Engenharia e Cobertura de Testes — <nome do projeto>", data, stack de testes e visão geral.
b) **Resumo Executivo:** Gráfico de rosca de distribuição da Pirâmide de Testes (Unitário vs Integração vs E2E) e gráfico de barras de cobertura por módulo.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Tabela Completa de Arquivos Testados e Cenários Cobertos.**
d) **Mapeamento de Débitos Técnicos de Teste** (casos complexos que necessitam de infraestrutura externa dedicada).
e) **Seção Final "ISSUES PARA O GITHUB/GITLAB":** Templates de issues para automação de testes contínuos em CI/CD.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`).
- Deixe o script gerador salvo no diretório `docs/tests-audit/`.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de que todos os testes foram criados e estão passando (100% Green).
2. A confirmação de geração do relatório em PDF.
3. A lista de arquivos de teste gerados no projeto.
