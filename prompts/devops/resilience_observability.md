# PROMPT DE AUDITORIA COMPLETA: RESILIÊNCIA, OBSERVABILIDADE, MENSAGERIA & ESTABILIDADE (SRE & YELLOW TEAM)

## OBJETIVO
Atuar como Engenheiro Principal de Confiabilidade (SRE) e Especialista em Arquitetura Resiliente (Yellow Team). Sua missão é auditar o repositório para garantir **alta disponibilidade, resiliência contra falhas em cascata, observabilidade ponta a ponta (Logs Estruturados, Métricas e Tracing Distribuído com OpenTelemetry)** e integridade no processamento assíncrono (**Filas, Mensageria, Dead Letter Queues e Backpressure**). A auditoria também cobre **Logging de Segurança e Monitoramento de Detecção** conforme o **OWASP Top 10 Proactive Controls 2024 — C9**.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todos os mecanismos de comunicação síncrona e assíncrona da aplicação (HTTP clients, gRPC, WebSockets, RabbitMQ, Apache Kafka, AWS SQS/SNS, Redis BullMQ, Celery).
2. Identifique os middlewares de observabilidade, exporters de telemetria, configurações de logging, probes de saúde e manipuladores de sinais de sistema (`SIGTERM`, `SIGINT`).
3. Você DEVE ler e analisar cada consumidor de fila, cliente de integração externa e manipulador de eventos linha por linha.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (RESILIÊNCIA & OBSERVABILIDADE)

### 1. Mensageria Assíncrona, Filas e Tratamento de Falhas
- [ ] **Dead Letter Queues (DLQ) e Retry com Backoff:** Verifique se todas as filas e consumidores de eventos possuem Dead Letter Queues configuradas e políticas de retry com *Exponential Backoff* e *Jitter*, impedindo loops infinitos de reprocessamento (*Retry Storms*).
- [ ] **Detecção de Mensagens Venenosas (Poison Pills):** Verifique se o consumidor de mensagens é capaz de capturar exceções fatais de deserialização/schema e encaminhar a mensagem defeituosa para quarentena sem travar o worker.
- [ ] **Idempotência no Consumo de Eventos:** Verifique se os consumers registram os IDs de eventos processados em store atômica/banco para evitar processamento duplicado em cenários de reentrega (*At-least-once delivery*).
- [ ] **Controle de Vazão e Backpressure:** Verifique se os workers assíncronos limitam a quantidade de mensagens consumidas simultaneamente (`prefetch_count` / `concurrency limit`), evitando estouro de memória sob picos de carga.

### 2. Padrões de Resiliência e Prevenção de Falhas em Cascata
- [ ] **Circuit Breakers em Chamadas Downstream:** Verifique se todas as chamadas HTTP/gRPC para serviços externos ou terceiros utilizam *Circuit Breaker* (ex: Opossum, Resilience4j, Polly, Tenacity), abrindo o circuito após taxas de erro anômalas para preservar o sistema.
- [ ] **Timeouts Estritos em I/O:** Identifique clientes de rede ou operações de banco de dados sem timeouts explícitos de conexão (`connectTimeout`) e de resposta (`readTimeout`), que possam causar acúmulo infinito de threads.
- [ ] **Bulkheads (Isolamento de Recursos):** Verifique se pools de conexões e filas de execução são isoladas por domínio crítico, impedindo que a lentidão em uma funcionalidade secundária derrube toda a aplicação.

### 3. Observabilidade Moderna (Logs, Métricas e Tracing)
- [ ] **Logs Estruturados em JSON:** Verifique se a aplicação emite logs em formato JSON padronizado com metadados contextuais (`timestamp`, `level`, `service`, `environment`, `userId_hash`, `tenantId`), sem emitir texto livre desestruturado em produção.
- [ ] **Propagação de Contexto e Correlation IDs (`x-correlation-id`):** Verifique se todas as requisições geram ou propagam um Trace ID único em headers e logs, conectando chamadas do frontend até os logs assíncronos das filas.
- [ ] **Instrumentação com OpenTelemetry (OTel):** Verifique se o código possui suporte a spans e tracing distribuído para rastrear gargalos de latência entre serviços.
- [ ] **Métricas Essenciais (Golden Signals):** Verifique a existência de métricas expostas (Prometheus/StatsD) cobrindo os 4 Sinais de Ouro: Latência, Tráfego, Erros e Saturação (CPU/Memória/Pool).

### 4. Ciclo de Vida e Encerramento Gracioso (Graceful Shutdown)
- [ ] **Manipulação de Sinais de Sistema:** Verifique se a aplicação captura sinais `SIGTERM` e `SIGINT` para drenar requisições em andamento antes de desligar, rejeitando novas conexões com `HTTP 503` durante a drenagem.
- [ ] **Fechamento Seguro de Conexões:** Garanta que no shutdown o sistema feche conexões de banco de dados, pools do Redis, canais de mensageria e finalize jobs em andamento sem perda de dados.

### 5. Logging de Segurança e Monitoramento de Detecção (OWASP Proactive Control C9)

Aplique o **OWASP Cheat Sheet Series** (*Logging, Application Logging Vocabulary, Logging Cheat Sheet*) e **A09:2021 — Security Logging and Monitoring Failures**.

- [ ] **Eventos de Segurança Auditados:** Verifique se são logados com contexto suficiente (ator, IP, recurso, ação, resultado, timestamp UTC, correlation ID): sucesso e falha de login, logout, troca de senha/e-mail/MFA, falha de autorização (`403`), criação/alteração de permissão e role, acesso a dado sensível/exportação em massa, invalidação de sessão, uso de token de reset, e eventos administrativos.
- [ ] **Redação de Dados Sensíveis no Log (Anti-Leak):** Verifique que senhas, tokens, chaves, cookies de sessão, PAN/cartão, PII e o corpo bruto de requisições sensíveis **nunca** são gravados em log; existência de um filtro/serializer central de redação aplicado a todos os appenders (inclusive logs de exceção e de acesso).
- [ ] **Integridade e Retenção dos Logs:** Verifique envio dos logs para um destino centralizado append-only fora do host da aplicação (SIEM/coletor), com retenção definida e proteção contra adulteração/expurgo pelo processo da aplicação; relógio sincronizado (NTP) e timestamps em UTC/ISO-8601.
- [ ] **Prevenção de Log Injection:** Verifique neutralização de CR/LF e caracteres de controle em valores vindos do usuário antes de concatenar em mensagens de log (evita forja de linhas de log e quebra de parsers).
- [ ] **Vocabulário e Nível Consistentes:** Verifique uso de um vocabulário de eventos padronizado (ex: `authn_login_success`, `authz_fail`, `authn_token_reuse`) e níveis coerentes (evento de segurança não afogado em `DEBUG`).
- [ ] **Alertas e Casos de Detecção Acionáveis:** Verifique existência de regras de alerta sobre picos de `403`/falha de login, reuso de refresh token, criação de conta admin, desativação de MFA, acesso fora de horário/geografia atípica, e volume anômalo de exportação — com destino de notificação definido (on-call/canal), não apenas dashboard.
- [ ] **Monitoramento de Disponibilidade do Pipeline de Log:** Verifique alerta para "parou de receber logs" (falha silenciosa do coletor) e para descarte de logs por backpressure.
- [ ] **Sem Dependência de Log do Cliente:** Verifique que decisões de detecção/forense não dependem de logs gerados no navegador/app móvel (não confiáveis).

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/queue/email-worker.ts:32` | Ausência de DLQ / Retry Infinito | CRÍTICA | Baixo (20 min) | **SIM** |
| #2 | `src/clients/payment-gateway.ts` | Falta de Circuit Breaker | ALTA | Médio (1 hr) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome da Fragilidade de Resiliência / Observabilidade]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [DLQ & Retry / Circuit Breaker / Structured Logs / Tracing OTel / Graceful Shutdown]
- **Problema:** Explicação direta de como a ausência desse padrão causa instabilidade, indisponibilidade ou cegueira operacional em produção.
- **Evidência:** Trecho de código atual sem o padrão de resiliência.
- **Correção Recomendada:** Código devidamente instrumentado ou com padrão de resiliência aplicado.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/resilience-audit/relatorio-auditoria-resiliencia.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Resiliência, Observabilidade e Confiabilidade — <nome do projeto>", data, mapa de mensageria e postura de SRE.
b) **Resumo Executivo:** Total de riscos por severidade, gráfico de rosca de estabilidade e gráfico de barras por categoria de resiliência.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (logging estruturado, tracing existente) e **Pontos Fracos** (riscos de gargalo, filas sem DLQ).
d) **Tabela de Achados Detalhados:** Severidade | Componente | Fragilidade Identificada | Solução.
e) **Guia de Implementação de Golden Signals e Resiliência.**
f) **Seção Final "ISSUES PARA O GITHUB":** Templates completos de issues para cada ponto de falha mapeado.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`).
- Deixe o script gerador salvo no diretório `docs/resilience-audit/`.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/resilience-audit/relatorio-auditoria-resiliencia.pdf`, `docs/resilience-audit/generate_report.py`).
