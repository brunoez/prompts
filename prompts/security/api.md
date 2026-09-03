# PROMPT DE AUDITORIA COMPLETA: APIS, OWASP API TOP 10 (ASTF), WSTG v4.2 E GERAÇÃO DE RELATÓRIO PDF / SARIF

## OBJETIVO
Atuar como Engenheiro Principal de APIs e Especialista em AppSec (Yellow/Red Team). Sua missão é realizar uma varredura completa no repositório aplicando a metodologia do **OWASP API Security Testing Framework (ASTF)**, a especificação oficial do **OWASP API Security Top 10 2023** e os testes essenciais de código do **OWASP Web Security Testing Guide (WSTG v4.2)**.

A auditoria deve garantir resiliência, performance, concorrência segura, proteção rigorosa de contratos (OpenAPI/GraphQL/gRPC/WebSockets), prevenção de uploads maliciosos, injeções em templates/arquivos e validação de autorização multi-tenant.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF, arquivo SARIF para o GitHub Security e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique a stack/tecnologia utilizada (Node.js/Nest/Express, Python/FastAPI/Django, Go/Gin, Java/Spring, Rust, etc.).
2. **Auditoria de Contrato e Inventário:** Leia arquivos de especificação (`openapi.yaml`, `swagger.json`, schemas `.graphql`, arquivos `.proto`, `postman_collection.json`). Compare as rotas declaradas com as rotas reais implementadas nos controllers para identificar **Shadow/Zombie APIs (ASTF-API9)**.
3. Identifique e analise TODOS os arquivos da camada de interface e rotas: controllers, handlers, resolvers GraphQL, serviços gRPC, handlers de WebSocket, middlewares de autenticação/autorização, DTOs/schemas de validação (Zod, Joi, Pydantic, class-validator), manipuladores de upload/arquivos, interceptores e clientes HTTP/Webhooks downstream.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.
5. **Diretriz Anti-Fadiga e Anti-Alucinação (Filtro Factual):** Só reporte vulnerabilidades que possam ser categoricamente comprovadas pelo código-fonte inspecionado. É proibido levantar suposições hipotéticas sem evidência no repositório. Recomendações puramente cosméticas ou de estilo sem impacto real de segurança devem ser marcadas como `[NIT]` ou descartadas, mantendo o foco estrito no risco real e no raio de impacto (*Blast Radius*).

---

## CHECKLIST DE AUDITORIA PRÁTICA (OWASP ASTF & WSTG v4.2)

### 1. Autorização, Autenticação e Sessão (ASTF Core & WSTG)
- [ ] **ASTF-API1 (BOLA / IDOR):** Identifique endpoints com identificadores de recursos na rota/query (`/api/orders/{id}`, `/users/{uuid}/profile`) que não validam se o `tenant_id` ou `user_id` autenticado na sessão possui a titularidade do objeto. Execute mentalmente o teste de **Matriz de Autorização Cruzada** (Usuário A tentando acessar o recurso do Usuário B).
- [ ] **ASTF-API2 (Broken Authentication) & WSTG-SESS-03 / IDNT-04:** Verifique ausência de autenticação em rotas sensíveis, JWTs com validação fraca de assinatura/algoritmo (`alg: none`, chaves simétricas fracas), falta de revogação/blacklist de tokens, regeneração ausente de Session ID após login (*Session Fixation*) e mensagens/tempos heterogêneos em login/recuperação que permitam enumeração de contas (*Account Harvesting*).
- [ ] **ASTF-API3 (BOPLA - Broken Object Property Level Authorization):**
  - **Mass Assignment:** Endpoints de criação/atualização que aceitam DTOs sem filtro estrito (`whitelist`), permitindo injetar campos sensíveis (ex: `role`, `is_admin`, `verified`, `balance`, `tenant_id`).
  - **Excessive Data Exposure:** Entidades do ORM retornadas cruas sem serialização/DTO de saída, vazando campos como `password_hash`, dados PII, segredos internos ou flags de auditoria.
- [ ] **ASTF-API5 (BFLA) & WSTG-ATHZ-01 (Path / Directory Traversal):** Rotas administrativas que checam apenas se o usuário está logado sem validação de roles (`RBAC/ABAC`), bypass via troca de método HTTP (`DELETE/PUT` em rota `GET`) e funções de leitura/download de arquivos locais (`fs.readFile`, `res.sendFile`, `open()`) que recebem caminhos do usuário sem normalização (`path.resolve`) e sem confinamento ao diretório raiz seguro.

### 2. Consumo de Recursos, Injeções, Uploads e Lógica de Negócio
- [ ] **ASTF-API4 (Unrestricted Resource Consumption):** Ausência de Rate Limiting por IP/Token em rotas pesadas; falta de timeout em operações síncronas; falta de paginação obrigatória com limite máximo (`limit/size` padrão e teto); ausência de limite no tamanho do corpo da requisição (*Request Payload Body Limit*).
- [ ] **ASTF-API6 (Business Flows) & WSTG-BUSL-08/09 (File Upload Vulnerabilities):** Endpoints de upload de arquivos que não validam os **Magic Bytes** reais do buffer (confiando apenas na extensão ou `Content-Type`), arquivos gravados com nomes controlados pelo cliente (permitindo sobrescrita e Path Traversal), ou ausência de isolamento do storage (falta de URLs pré-assinadas S3/GCS ou execução de scripts liberada).
- [ ] **ASTF-API7 (Server-Side Request Forgery - SSRF):** Endpoints que aceitam URLs fornecidas pelo cliente (webhooks, importação de imagens, fetch de links, integrações) sem validação de whitelist estrita, permitindo acesso à rede interna (`localhost`, `10.0.0.0/8`, `192.168.0.0/16`) ou metadata cloud (`169.254.169.254`).
- [ ] **ASTF-INJECTION & WSTG-INPV-18 (SSTI / Template Injection):** Concatenação direta de parâmetros em queries SQL/NoSQL, injeção de comandos em subprocessos e interpolação de strings não sanitizadas no corpo de templates de e-mail ou páginas SSR (`Handlebars.compile`, `jinja2.Template`, `ejs.render`) gerando RCE.
- [ ] **ASTF-REDOS (Regular Expression Denial of Service):** Uso de expressões regulares vulneráveis a *catastrophic backtracking* em middlewares de rota, sanitizadores ou schemas de validação.

### 3. Configuração, Inventário e Consumo de Terceiros
- [ ] **ASTF-API8 (Security Misconfiguration) & WSTG-CLNT-07 (CORS Regex Bypass):** CORS excessivamente permissivo (`Origin: *` com `Credentials: true`); middlewares de CORS com expressões regulares dinâmicas mal formatadas (pontos não escapados aceitando domínios de atacantes); ausência de headers de segurança (`HSTS`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy`); vazamento de stack traces em erros 500.
- [ ] **ASTF-API9 (Improper Inventory Management):** Presença de rotas legadas não documentadas (`/api/v1/` coexistindo sem patches com `/v2/`), endpoints internos/debug expostos publicamente e discrepâncias entre o Swagger/OpenAPI e a implementação real (*Contract Drift*).
- [ ] **ASTF-API10 (Unsafe Consumption of APIs):** Consumo ingênuo de APIs externas ou webhooks sem validação rigorosa de schema e assinatura criptográfica; confiança cega em dados retornados por serviços terceiros downstream.

### 4. Protocolos Modernos e Vetores Avançados (ASTF Extensions & WSTG)
- [ ] **ASTF-GRAPHQL:** Introspecção (`__schema`) habilitada em produção; ausência de limitação de profundidade de query (*Query Depth Limiting*) permitindo DoS por recursão circular; ausência de análise de custo/complexidade (*Query Cost Analysis*); batching attacks desprotegidos.
- [ ] **ASTF-GRPC:** Server Reflection ativado em ambiente produtivo; ausência de interceptores de autenticação/autorização em chamadas RPC; falta de validação de tamanho de stream.
- [ ] **WSTG-CLNT-10 (WebSocket Security & CSWSH):** Servidores WebSocket que aceitam conexões sem validação estrita do cabeçalho `Origin` no handshake HTTP inicial, permitindo Cross-Site WebSocket Hijacking em conexões autenticadas via cookies.
- [ ] **ASTF-LLM (AI/GenAI Endpoints):** Endpoints de API que recebem entrada do usuário para compor prompts de LLM sem sanitização contra *Indirect Prompt Injection*, falta de restrição de permissões em chamadas de ferramentas (*Tool/Function Calling*) e ausência de guardrails na resposta da API.
- [ ] **ASTF-MTLS & Transport:** Falta de enforcement de TLS 1.3/mTLS para comunicação entre microsserviços sensíveis ou integrações B2B bancárias/financeiras.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica, exiba no chat a lista detalhada de achados ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados:

| ID | Arquivo / Ponto | Módulo / Padrão | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/controllers/upload.ts:32` | WSTG File Upload (No Magic Bytes) | CRÍTICA | Baixo (20 min) | **SIM** |
| #2 | `src/controllers/order.ts:54` | ASTF-API1 (BOLA) | CRÍTICA | Baixo (20 min) | **SIM** |
| #3 | `src/routes/webhook.ts:88` | ASTF-API7 (SSRF) | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item da tabela:
- **Achado #[ID]:** [Nome do Problema]
- **Módulo ASTF / WSTG:** [ex: ASTF-API1-2023 (BOLA) / WSTG-BUSL-08 (File Upload) / WSTG-INPV-18 (SSTI)]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Vetor de Ataque / Exploração:** Como um atacante explora essa falha (ex: payload de exemplo, bypass de extensão, chamada com segundo token ou WebSocket hijacking).
- **Evidência:** Trecho do código-fonte vulnerável.
- **Prova de Conceito (PoC / Reprodução):** Exemplo de requisição reproduzível (`curl`, script ou payload HTTP) para demonstrar a falha no contexto do projeto.
- **Correção Recomendada:** Código devidamente refatorado e seguro.
- **Comando de Verificação da Correção:** Como o desenvolvedor valida em 1 comando (teste automatizado ou chamada de verificação) que a correção funcionou sem quebrar o contrato da API.

---

## GERAÇÃO DE RELATÓRIO PDF, SARIF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script automatizado salvo em `docs/api-audit/generate_report.py` para produzir:

1. **Relatório em PDF (`docs/api-audit/relatorio-auditoria-api.pdf`):**
   - **Capa:** Título "Relatório de Auditoria de APIs e Segurança (OWASP ASTF & WSTG) — <nome do projeto>", data, escopo e conformidade com OWASP API Top 10 2023.
   - **Resumo Executivo:** Gráfico de rosca por severidade e gráfico de barras com a distribuição dos módulos detectados.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
   - **Matriz de Conformidade ASTF & WSTG:** Tabela indicando status para cada um dos módulos.
   - **Tabela Detalhada de Achados** com tags de Quick Win e referências a arquivos e linhas.

2. **Arquivo SARIF (`docs/api-audit/results.sarif`):**
   - Gere o relatório no padrão **SARIF v2.1.0** para que possa ser importado diretamente na aba *Security / Code Scanning* do GitHub Actions.

3. **Seção "ISSUES PARA O GITHUB" no Relatório:**
   - Template Markdown completo pronto para copiar e colar para cada achado relevante, com labels, passos de reprodução, impacto e critérios de aceite.

### REGRAS TÉCNICAS
- Use ambiente Python isolado (`venv` temporário com `reportlab` e `matplotlib`).
- Salve o script e os artefatos em `docs/api-audit/`.
- Garanta formatação A4 impecável, paginação correta e sem quebras visuais em tabelas.

---

## ENTREGÁVEIS FINAIS
Ao concluir, informe no chat:
1. A confirmação da geração do relatório PDF e do arquivo SARIF.
2. A lista de achados (Parte 1 e Parte 2).
3. O caminho relativo dos arquivos gerados (`docs/api-audit/relatorio-auditoria-api.pdf`, `docs/api-audit/results.sarif`, `docs/api-audit/generate_report.py`).