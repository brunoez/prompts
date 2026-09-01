# PROMPT DE AUDITORIA E ENGENHARIA: CONTRACT-DRIVEN DEVELOPMENT (CDD) & CONSUMER-DRIVEN CONTRACTS (PACT/OPENAPI)

## OBJETIVO
Atuar como Engenheiro Principal de Integração e Especialista em Arquitetura de Contratos (Yellow Team). Sua missão é auditar e implementar a disciplina de **Contract-Driven Development (CDD)** no repositório, garantindo que a comunicação entre serviços, microsserviços, frontend-backend e APIs de terceiros seja governada por contratos imutáveis, executáveis e versionados (OpenAPI, AsyncAPI, Protobuf, GraphQL e **Consumer-Driven Contracts** com Pact). O foco é prevenir quebras de contrato em produção (*Breaking Changes*) e garantir desacoplamento seguro.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Contratos/Issues para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todos os pontos de integração externa e interna da aplicação (chamadas HTTP entre serviços, Webhooks consumidos/enviados, tópicos de mensageria Kafka/RabbitMQ/SQS, chamadas gRPC, GraphQL).
2. Identifique todos os arquivos de definição de contrato (`openapi.yaml`, `swagger.json`, `asyncapi.yaml`, `schema.graphql`, `*.proto`, arquivos de pactos em `pacts/` ou Pact Broker).
3. Identifique os clientes de API gerados ou manuais e os controladores/handlers que servem essas interfaces.
4. Você DEVE ler e analisar cada contrato e implementação, verificando se há divergência entre a especificação acordada e os dados realmente transmitidos/recebidos (*Contract Drift*).

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (CONTRACT-DRIVEN DEVELOPMENT)

### 1. Governança e Validação de Contratos de API (OpenAPI / Schema-First)
- [ ] **Validação Automatizada de Conformidade (Contract Testing):** Verifique se existem testes automatizados que validam se as respostas reais da API (status code, headers, corpo JSON) estão 100% em conformidade com o schema OpenAPI/AsyncAPI declarado (ex: usando ferramentas como Dredd, Prism, ou validadores de OpenAPI em Vitest/Jest).
- [ ] **Prevenção de Quebras de Compatibilidade Retroativa (Breaking Changes):** Verifique se alterações de schema são verificadas contra ferramentas de detecção de breaking change (ex: `oasdiff`, `graphql-inspector`, `buf breaking`), impedindo a remoção de campos ou adição de campos obrigatórios sem versionamento.
- [ ] **Geração Automatizada de Clientes e Tipos:** Verifique se o frontend e serviços consumidores geram seus clientes HTTP e tipos TypeScript/Python diretamente da especificação OpenAPI (`openapi-typescript`, `orval`, `rtk-query`), eliminando tipagens manuais suscetíveis a erro humano.

### 2. Consumer-Driven Contracts (Pact Testing)
- [ ] **Existência de Testes no Lado do Consumidor (Consumer Tests):** Verifique se os serviços consumidores definem formalmente suas expectativas de requisição e resposta usando contratos Pact, gerando arquivos de pacto versionados.
- [ ] **Verificação no Lado do Provedor (Provider Verification):** Verifique se o serviço provedor executa testes que validam automaticamente todos os pactos registrados pelos seus consumidores antes de autorizar novos deploys (`can-i-deploy`).
- [ ] **Desacoplamento e Independência de Deploy:** Garanta que mudanças internas na estrutura de dados do provedor não quebrem campos consumidos por clientes legados ou aplicações móveis.

### 3. Contratos de Mensageria Assíncrona e Eventos (AsyncAPI / Event Schemas)
- [ ] **Especificação Formal de Eventos (AsyncAPI / CloudEvents):** Verifique se os eventos publicados em tópicos de mensageria (RabbitMQ, Kafka, EventBridge) possuem schemas formais versionados documentando a estrutura do payload, headers de correlação e metadados.
- [ ] **Evolução Segura de Schemas de Eventos (Schema Registry):** Verifique se os tópicos utilizam Schema Registry (Avro, Protobuf ou JSON Schema) com políticas estritas de compatibilidade (*FULL*, *BACKWARD*, *FORWARD*).
- [ ] **Validação de Consumo de Eventos Desconhecidos:** Garanta que os consumidores de mensagens tratem de forma graciosa payloads com novos campos sem falhar o processamento.

### 4. Contratos de Webhooks e Integrações de Terceiros
- [ ] **Validação Estrita de Assinatura de Webhooks:** Verifique se todos os webhooks recebidos (Stripe, Pagar.me, GitHub, etc.) possuem contratos que validam rigorosamente a assinatura criptográfica (`HMAC-SHA256`) no header antes do parsing do body.
- [ ] **Mocking Confiável Baseado em Contrato:** Verifique se os testes de integração contra APIs externas utilizam servidores de mock alimentados diretamente pelos contratos oficiais do fornecedor.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `openapi.yaml:45` | Breaking Change em Rota Pública | CRÍTICA | Baixo (20 min) | **SIM** |
| #2 | `src/events/user-created.ts` | Evento Sem Schema AsyncAPI | ALTA | Médio (1 hr) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema de Contrato]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/contrato.ext:linha`
- **Categoria:** [Contract Drift / Breaking Change / Pact Testing / Event Schema / Webhook Verification]
- **Problema:** Explicação do risco de quebra de comunicação entre sistemas em produção.
- **Evidência:** Trecho do contrato ou implementação divergente.
- **Contrato / Código Recomendado:** Definição correta do contrato OpenAPI/AsyncAPI ou teste Pact.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/cdd-audit/relatorio-auditoria-cdd.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria CDD (Contract-Driven Development) — <nome do projeto>", data, mapa de integrações e status dos contratos.
b) **Resumo Executivo:** Total de contratos divergentes por severidade, gráfico de rosca de maturidade de contratos e gráfico de barras por tipo de protocolo (REST/OpenAPI, gRPC, Eventos/AsyncAPI).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (contratos bem versionados) e **Pontos Fracos** (riscos de quebra de integração em produção).
d) **Tabela de Achados Detalhados:** Severidade | Integração | Falha de Contrato Mapeada.
e) **Diretrizes de Versionamento e Contratos:** Regras para evolução segura de contratos de API e eventos.
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada contrato quebrado ou ausente, a issue formatada para o GitHub.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`).
- Deixe o script gerador salvo no diretório `docs/cdd-audit/`.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/cdd-audit/relatorio-auditoria-cdd.pdf`, `docs/cdd-audit/generate_report.py`).
