# PROMPT DE AUDITORIA COMPLETA: CONTROLE DE ACESSO & AUTORIZAÇÃO (OWASP PROACTIVE CONTROL C1), RBAC/ABAC/ReBAC, IDOR/BOLA E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Autorização (Access Control Lead / Yellow Team). Sua missão é realizar uma varredura completa no repositório aplicando o **OWASP Top 10 Proactive Controls 2024 — C1: Implement Access Control** e as diretrizes do **OWASP Cheat Sheet Series** (*Authorization, Access Control, Insecure Direct Object Reference Prevention, Transaction Authorization*), reforçadas pelos testes de código do **OWASP WSTG v4.2** (*WSTG-ATHZ*) e pela categoria **A01:2021 — Broken Access Control**.

A auditoria deve garantir negação por padrão (*deny-by-default*), centralização da decisão de autorização, verificação de titularidade de objeto em toda camada (rota, serviço, dado), isolamento multi-tenant, ausência de escalada de privilégio horizontal/vertical e proteção de funções administrativas.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique a stack e o modelo de autorização usado (RBAC por roles, ABAC por atributos/políticas, ReBAC/relacional tipo Zanzibar/OpenFGA/Oso, ACLs, *policy engine* como OPA/Casbin/Cerbos).
2. Identifique e analise TODOS os pontos de decisão de acesso: middlewares/guards de autorização, decorators (`@Roles`, `@PreAuthorize`, `permission_classes`), checagens inline (`if user.role === 'admin'`), *policy files*, *row-level security* no banco, filtros de query por `tenant_id`/`owner_id` e regras de GraphQL field-level.
3. Construa a **Matriz de Acesso** do sistema: para cada recurso/ação sensível, quais papéis/atributos deveriam ter acesso, e confronte com o que o código realmente exige.
4. Identifique os identificadores de objeto expostos ao cliente (rota, query, body, header) e verifique onde a titularidade é (ou não é) validada.
5. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.
6. **Diretriz Anti-Fadiga e Anti-Alucinação (Filtro Factual):** Só reporte vulnerabilidades categoricamente comprovadas pelo código-fonte inspecionado. É proibido levantar suposições hipotéticas sem evidência. Recomendações cosméticas sem impacto real devem ser marcadas como `[NIT]` ou descartadas, mantendo o foco no risco real e no *Blast Radius*.

---

## CHECKLIST DE AUDITORIA PRÁTICA (OWASP PROACTIVE C1 & CHEAT SHEETS)

### 1. Princípios Fundamentais (Authorization + Access Control Cheat Sheets)
- [ ] **Deny-by-Default:** Verifique se toda rota/handler/recurso nega acesso por padrão e só libera mediante regra explícita — nunca "libera se não houver regra que bloqueie". Rotas novas sem decorator de autorização devem falhar fechado.
- [ ] **Centralização da Decisão:** Verifique se a autorização passa por um componente único e testável (middleware, *policy engine*, service) em vez de checagens `if role ==` espalhadas e divergentes por controller.
- [ ] **Enforcement no Servidor:** Verifique que nenhuma decisão de acesso depende de flag vinda do cliente (campo `isAdmin` no body/JWT não verificado, parâmetro `?role=`, ocultar botão no frontend sem bloquear a rota).
- [ ] **Menor Privilégio:** Verifique se roles/scopes concedidos são os mínimos necessários; ausência de role "god"/wildcard (`*:*`) atribuída por conveniência a serviços ou usuários internos.
- [ ] **Separação de Deveres e Contexto:** Operações críticas (aprovar pagamento, alterar permissão de outro usuário) exigem papel distinto de quem originou a ação e re-autenticação/*step-up* quando aplicável (Transaction Authorization Cheat Sheet).

### 2. IDOR / BOLA — Autorização em Nível de Objeto (IDOR Prevention Cheat Sheet — WSTG-ATHZ-04)
- [ ] **Verificação de Titularidade:** Para cada endpoint com identificador na rota/query/body (`/orders/{id}`, `/users/{uuid}/cards`, `?accountId=`), verifique se o código confirma que o objeto pertence ao `user_id`/`tenant_id` autenticado **antes** de ler/alterar — não apenas `findById(id)`.
- [ ] **Referências Indiretas ou Não Adivinháveis:** Verifique uso de UUIDv4/identificadores por-usuário no lugar de inteiros sequenciais previsíveis; a ausência de IDs sequenciais não substitui a checagem de titularidade, mas reduz enumeração.
- [ ] **Escopo na Query, não no Código de Aplicação:** Prefira `WHERE id = ? AND tenant_id = ?` (ou Row-Level Security no banco) a buscar por `id` e filtrar depois em memória — filtragem pós-consulta é frágil e vaza via contagem/paginação.
- [ ] **Mass Assignment / BOPLA:** Verifique se endpoints de criação/atualização aceitam campos que controlam acesso (`role`, `owner_id`, `tenant_id`, `is_verified`) sem *allow-list* estrita de propriedades graváveis.
- [ ] **Objetos Aninhados e Batch:** Verifique autorização em cada item de operações em lote (`PATCH /items` com array de IDs), em sub-recursos (`/orders/{id}/items/{itemId}`) e em expansões GraphQL (`order { customer { ssn } }`).

### 3. Escalada Vertical e Funções Administrativas (WSTG-ATHZ-02 / BFLA)
- [ ] **Rotas Admin:** Verifique que endpoints administrativos exigem role/scope específico e não apenas "usuário autenticado"; ausência de rotas admin acessíveis por adivinhação de caminho (`/admin`, `/internal`, `/api/v1/debug`) sem checagem.
- [ ] **Bypass por Método/Verbo HTTP:** Verifique que trocar `GET` por `POST/PUT/DELETE`, usar `X-HTTP-Method-Override` ou content-type alternativo não contorna o guard de autorização.
- [ ] **Force Browsing / Falta de Checagem Pós-Navegação:** Verifique que etapas de um fluxo (wizard, checkout, aprovação) revalidam permissão em cada passo, não só no primeiro.
- [ ] **Endpoints de Gestão de Usuário:** `PATCH /users/{id}/role`, convites, reset de MFA de terceiros — verifique que só admin do mesmo tenant executa e que ninguém eleva o próprio privilégio.

### 4. Isolamento Multi-Tenant e Consistência
- [ ] **Tenant Boundary:** Verifique que todo acesso a dado carrega o `tenant_id` da sessão como filtro obrigatório e não confia em `tenant_id` enviado pelo cliente. Teste mental da **Matriz de Autorização Cruzada** (Tenant A acessando recurso do Tenant B).
- [ ] **Caches e Chaves Compartilhadas:** Verifique que chaves de cache, nomes de arquivo em storage e chaves de idempotência incluem o escopo do tenant/usuário para evitar vazamento cruzado.
- [ ] **Jobs Assíncronos e Webhooks:** Verifique que workers e handlers de eventos recarregam e revalidam o contexto de autorização em vez de confiar em payload serializado antigo.
- [ ] **Consistência entre Camadas:** Verifique que API, GraphQL, gRPC, exportações/relatórios e endpoints legados aplicam a **mesma** regra de acesso ao mesmo recurso.

### 5. Testabilidade e Observabilidade da Autorização
- [ ] **Testes Negativos de Autorização:** Verifique existência de testes automatizados que esperam `403 Forbidden` / `404` para acesso cruzado (usuário A ao recurso de B, tenant cruzado, não-admin em rota admin).
- [ ] **Log de Decisão de Acesso:** Verifique que negações de autorização são logadas com ator, recurso, ação e resultado (para detecção de abuso — ver também Proactive C9).
- [ ] **Fail Closed em Erro:** Verifique que exceção no *policy engine* ou timeout de consulta de permissão resulta em negação, nunca em liberação.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica, exiba no chat a lista detalhada de achados ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados:

| ID | Arquivo / Ponto | Módulo / Padrão | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/controllers/invoice.ts:31` | BOLA / IDOR (sem checagem de titularidade) | CRÍTICA | Baixo (30 min) | **SIM** |
| #2 | `src/routes/admin.ts:8` | Rota admin sem checagem de role | CRÍTICA | Baixo (20 min) | **SIM** |
| #3 | `src/services/report.ts:120` | Filtro de tenant só em memória | ALTA | Médio (3 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item da tabela:
- **Achado #[ID]:** [Nome do Problema]
- **Controle / Cheat Sheet:** [ex: Proactive C1 / IDOR Prevention Cheat Sheet / WSTG-ATHZ-04 / A01:2021]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Vetor de Ataque / Exploração:** Como um atacante explora a falha (ex: trocar `id` na rota, forjar `tenant_id`, force browsing de `/admin`).
- **Evidência:** Trecho do código-fonte vulnerável.
- **Prova de Conceito (PoC / Reprodução):** Requisição reproduzível (`curl` com dois tokens de usuários distintos) demonstrando o acesso indevido.
- **Correção Recomendada:** Código refatorado com checagem centralizada e escopo na query.
- **Comando de Verificação da Correção:** Como validar em 1 comando (teste negativo de autorização) que a correção funcionou.

---

## GERAÇÃO DE RELATÓRIO PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script automatizado salvo em `docs/access-control-audit/generate_report.py` para produzir:

1. **Relatório em PDF (`docs/access-control-audit/relatorio-auditoria-autorizacao.pdf`):**
   - **Capa:** Título "Relatório de Auditoria de Controle de Acesso (OWASP Proactive C1) — <nome do projeto>", data e escopo.
   - **Resumo Executivo:** Gráfico de rosca por severidade e gráfico de barras por categoria (Deny-by-Default, IDOR/BOLA, Escalada Vertical, Multi-Tenant, Testabilidade).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
   - **Matriz de Acesso Auditada:** Tabela recurso × papel com status esperado vs implementado.
   - **Tabela Detalhada de Achados** com tags de Quick Win e referências a arquivos e linhas.

2. **Seção "ISSUES PARA O GITHUB" no Relatório:**
   - Template Markdown completo pronto para copiar e colar para cada achado, com labels, passos de reprodução, impacto e critérios de aceite.

### REGRAS TÉCNICAS
- Use ambiente Python isolado (`venv` temporário com `reportlab` e `matplotlib`).
- Salve o script e os artefatos em `docs/access-control-audit/`.
- Garanta formatação A4 impecável, paginação correta e sem quebras visuais em tabelas.

---

## ENTREGÁVEIS FINAIS
Ao concluir, informe no chat:
1. A confirmação da geração do relatório PDF.
2. A lista de achados (Parte 1 e Parte 2).
3. O caminho relativo dos arquivos gerados (`docs/access-control-audit/relatorio-auditoria-autorizacao.pdf`, `docs/access-control-audit/generate_report.py`).
