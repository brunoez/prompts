# PROMPT DE AUDITORIA COMPLETA: APIS, SEGURANÇA (OWASP API TOP 10), PERFORMANCE E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de APIs e Especialista em AppSec. Sua missão é realizar uma varredura completa no repositório para garantir resiliência, performance, concorrência segura, proteção de endpoints e prevenção ativa contra falhas de contrato e vazamentos (Data Leakage) em APIs, alinhando a validação aos padrões do OWASP API Security Top 10 e melhores práticas de design de APIs.

Ao final da auditoria, você deve listar os achados no terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios do projeto e identifique a stack/tecnologia utilizada (Node.js, Python, Go, Java, etc.).
2. Leia todos os arquivos de documentação de API e arquitetura existentes (`OpenAPI/Swagger`, `postman_collection`, `README.md`, `/docs`, etc.).
3. Identifique e analise TODOS os arquivos da camada de interface e rotas: controllers, handlers, middlewares de autenticação/autorização, DTOs/schemas de validação, tratamento global de exceções, rotas gRPC/GraphQL e clientes HTTP.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP API TOP 10 & DESIGN)

### 1. Autenticação, Autorização e Controle de Acesso
- [ ] **BOLA (Broken Object Level Authorization / IDOR):** Identifique endpoints que recebem IDs de recursos na URL (ex: `/api/orders/{id}`) sem validar se o usuário autenticado é o dono real daquele recurso.
- [ ] **BFA (Broken Function Level Authorization):** Verifique se rotas administrativas ou de escrita apenas checam se o usuário está logado, sem validar permissões específicas/roles (`RBAC`/`ABAC`).
- [ ] **Gestão Deficiente de Tokens/Sessões:** Verifique o uso de JWTs sem validação de assinatura, algoritmos fracos (ex: `alg: none`), expiração excessivamente longa ou ausência de revogação.

### 2. Validação de Entrada, Exposição e Vazamentos
- [ ] **BOPM (Broken Object Property Level Authorization / Mass Assignment):** Identifique endpoints de criação/atualização que aceitam DTOs genéricos, permitindo que o cliente altere propriedades protegidas (ex: `is_admin`, `tenant_id`, `balance`).
- [ ] **Exposição Excessiva de Dados:** Verifique se entidades do banco ou objetos internos são retornados diretamente na resposta JSON sem filtragem por DTOs ou Mappers de resposta.
- [ ] **Falta de Sanitização e Injeções:** Identifique entradas de usuários em rotas que não passam por validação estrita de schema (ex: Zod, Joi, class-validator) abrindo brechas para SQLi, Command Injection ou NoSQLi.

### 3. Resiliência, Performance e Rate Limiting
- [ ] **Consumo Desenfreado de Recursos (Rate Limit):** Identifique ausência de limites de requisições (`Rate Limiting` / `Throttling`) por IP ou Token em endpoints sensíveis (login, reset de senha, envio de SMS/e-mail, buscas pesadas).
- [ ] **Timeouts e Resiliência em Chamadas Downstream:** Verifique se chamadas para APIs de terceiros ou microserviços possuem timeouts configurados, estratégias de retry e padrão *Circuit Breaker*.
- [ ] **Paginação e Payload Size Limit:** Localize rotas de listagem sem limitação de tamanho de página e verifique a ausência de limite máximo no tamanho do corpo da requisição (*Request Body Size Limit*).

### 4. Tratamento de Erros, Logs e Observabilidade
- [ ] **Vazamento de Stack Traces e Erros Internos:** Identifique exceções não tratadas que retornam mensagens nativas do sistema/banco ou *stack traces* no payload HTTP de erro.
- [ ] **Vazamento via Logs (PII Leakage em APIs):** Identifique se headers de autorização (`Authorization: Bearer`), senhas, tokens ou dados PII são gravados em logs de requisição/resposta em texto claro.
- [ ] **CORS e Headers de Segurança:** Verifique se a política de CORS está configurada de forma permissiva demais (`Access-Control-Allow-Origin: *` com credenciais) e se headers como `HSTS`, `X-Content-Type-Options` estão ausentes.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/controllers/user.ts:42` | Autorização (BOLA) | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `src/routes/api.ts:105` | Resiliência (Rate Limit) | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [OWASP API / Autenticação e Autorização / Performance e Resiliência / Vazamento e Logs / Sanitização]
- **Problema:** Explicação direta do risco real em produção e qual vulnerabilidade de API está sendo exposta.
- **Evidência:** Trecho do código-fonte atual.
- **Correção Recomendada:** Código devidamente corrigido.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/api-audit/relatorio-auditoria-api.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de APIs e Segurança — <nome do projeto>", data, escopo auditado e nota metodológica (como cada categoria foi mapeada para a stack detectada).
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria. 
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (o que está protegido, com evidência) e **Pontos Fracos** (os riscos centrais da API).
d) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição, com indicação/chip de severidade e tag de Quick Win.
e) **Recomendações Priorizadas** (P1, P2, P3...).
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[API/Segurança] <descrição curta da falha>`
   - Labels sugeridas: `api` + `security` ou `performance` + severidade
   - Descrição do problema e por que é explorável / impacta a produção
   - Evidência: `arquivo:linha` com trecho de código
   - Impacto
   - Sugestão de correção
   - Critérios de aceite (checklist verificável)
   *(Nota: Agrupe achados triviais relacionados numa issue única quando fizer sentido para evitar spam).*

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Não instale pacotes globalmente no sistema. Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`, ou ferramentas equivalentes locais como `puppeteer`/HTML-to-PDF).
- Deixe o script gerador salvo no diretório `docs/api-audit/` para que o relatório possa ser regerado futuramente.
- Verifique o PDF gerado: garanta o número correto de páginas, a renderização adequada dos gráficos e a legibilidade das tabelas.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/api-audit/relatorio-auditoria-api.pdf`, `docs/api-audit/generate_report.py`).