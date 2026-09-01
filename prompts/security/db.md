# PROMPT DE AUDITORIA COMPLETA: BANCO DE DADOS, CONCORRÊNCIA, SEGURANÇA E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Banco de Dados e Especialista em AppSec. Sua missão é realizar uma varredura completa no repositório para garantir resiliência, performance, concorrência segura, proteção de dados e prevenção ativa contra vazamentos (Data Leakage), alinhando a validação aos pilares de DDD (limites de transação), ADD (atributos de qualidade) e TDD Concorrente.

Ao final da auditoria, você deve listar os achados no terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios do projeto e identifique a stack/tecnologia utilizada.
2. Leia todos os arquivos de documentação e arquitetura existentes (`README.md`, `/docs`, SDD, etc.).
3. Identifique e analise TODOS os arquivos com impacto em dados: entidades, ORMs, repositórios, SQLs nativos, scripts de migração, configurações de pool, controllers/mappers que tratam requisições/respostas do banco e arquivos de log/exceção.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA

### 1. Limites de Transação e Arquitetura (DDD / ADD)
- [ ] **Dual Write:** Identifique escritas sequenciais em múltiplos bancos/serviços (ex: SQL + Redis, SQL + Kafka) no mesmo fluxo sem padrões de resiliência (Transactional Outbox ou CDC).
- [ ] **Escopo da Transação:** Identifique transações SQL curtas vs. transações longas que abraçam chamadas externas (I/O, APIs de terceiros, envios de e-mail), retendo conexões desnecessariamente.
- [ ] **Gestão do Pool de Conexões:** Verifique ausência de timeouts, conexões não devolvidas ao pool (*Connection Leak*) e retenção indevida de threads.
- [ ] **Migrações e Schema:** Verifique se as alterações de banco usam scripts versionados (Flyway, Liquibase, Prisma Migrations) e garanta a ausência de opções perigosas ativas em produção (como `auto-ddl`, `synchronize: true` ou `drop-schema`).

### 2. Desempenho e ORM
- [ ] **N+1 Queries:** Identifique iterações sobre coleções/listas que disparam novas buscas individuais ao banco (falta de `Eager Loading`, `Fetch JOINs` ou paginação adequada).
- [ ] **Falta de Índices:** Localize consultas com cláusulas `WHERE`, `JOIN` ou `ORDER BY` em colunas que não possuem índices explicitamente mapeados nas migrações/entidades.
- [ ] **Consultas Sem Paginação:** Identifique buscas globais (`findAll()`, `SELECT *`) sem cláusulas de restrição (`LIMIT` / paginação) que possam estourar a memória RAM (*Out of Memory*).
- [ ] **Observabilidade:** Verifique se existe suporte a logs de consultas lentas (*Slow Query Log*) sem comprometer dados sensíveis.

### 3. Concorrência e Resiliência (TDD Concorrente)
- [ ] **Race Conditions:** Identifique operações de leitura-modificação-escrita em recursos compartilhados sem a devida sincronização (Lock Otimista, Lock Pessimista ou atualizações atômicas diretamente no SQL).
- [ ] **Deadlocks:** Identifique se transações simultâneas tentam alterar múltiplos registros/tabelas em ordem cruzada ou inconsistente.
- [ ] **Idempotência e Retry:** Verifique se existem mecanismos de retry com *backoff* exponencial para falhas de transação transitórias (como deadlocks aleatórios) em operações críticas.

### 4. Segurança do Banco e Prevenção de Vazamentos (Data Leakage)
- [ ] **SQL Injection:** Identifique concatenação ou interpolação manual de strings em instruções SQL (exigir rigorosamente `Prepared Statements` / queries parametrizadas).
- [ ] **Credenciais e Dados Sensíveis:** Verifique senhas ou chaves hardcoded no código, ausência de criptografia TLS/SSL na conexão com o banco e dados sensíveis (PII, segredos) salvos em texto puro nas tabelas.
- [ ] **Vazamento via Logs (PII Leakage):** Identifique se objetos completos de banco, DTOs com dados sensíveis (senhas, cartões, CPF) ou parâmetros de busca estão sendo gravados em arquivos de log em texto claro.
- [ ] **Vazamento via Serialização/APIs:** Verifique se entidades do banco/ORM são retornadas diretamente em controllers/endpoints HTTP sem o uso de DTOs, Mappers ou anotações de exclusão (ex: `@JsonIgnore`, `select: false`), expondo colunas internas na resposta JSON.
- [ ] **Vazamento em Tratamento de Exceções:** Identifique se erros SQL nativos, exceções do ORM ou *stack traces* completos são expostos diretamente no payload HTTP de erro para o cliente.
- [ ] **Mass Assignment:** Identifique se payloads de requisições de criação/atualização são injetados diretamente nas entidades do banco sem filtro explícito de campos permitidos (*whitelisting*).

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `caminho/arquivo.ext:42` | Segurança | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `caminho/outro.ext:105` | Performance | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [DDD / ADD / TDD Concorrente / Segurança e Vazamentos / Performance / Migrações]
- **Problema:** Explicação direta do risco real em produção.
- **Evidência:** Trecho do código-fonte atual.
- **Correção Recomendada:** Código devidamente corrigido.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/security-audit/relatorio-auditoria-seguranca.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Banco de Dados e Segurança — <nome do projeto>", data, escopo auditado e nota metodológica (como cada categoria foi mapeada para a stack detectada).
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria. 
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (o que está protegido, com evidência) e **Pontos Fracos** (os riscos centrais).
d) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição, com indicação/chip de severidade e tag de Quick Win.
e) **Recomendações Priorizadas** (P1, P2, P3...).
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[Segurança/Banco] <descrição curta da falha>`
   - Labels sugeridas: `security` ou `database` + severidade
   - Descrição do problema e por que é explorável / impacta a produção
   - Evidência: `arquivo:linha` com trecho de código
   - Impacto
   - Sugestão de correção
   - Critérios de aceite (checklist verificável)
   *(Nota: Agrupe achados triviais relacionados numa issue única quando fizer sentido para evitar spam).*

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Não instale pacotes globalmente no sistema. Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`, ou ferramentas equivalentes locais como `puppeteer`/HTML-to-PDF).
- Deixe o script gerador salvo no diretório `docs/security-audit/` para que o relatório possa ser regerado futuramente.
- Verifique o PDF gerado: garanta o número correto de páginas, a renderização adequada dos gráficos e a legibilidade das tabelas.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/security-audit/relatorio-auditoria-seguranca.pdf`, `docs/security-audit/generate_report.py`).