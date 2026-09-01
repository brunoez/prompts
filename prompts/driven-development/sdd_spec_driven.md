# PROMPT DE AUDITORIA E ENGENHARIA: SPEC-DRIVEN & SCHEMA-DRIVEN DEVELOPMENT (SDD), ARQUITETURA E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Arquitetura de Software e Especialista em AppSec (Yellow Team). Sua missão é auditar ou estabelecer a disciplina de **Spec-Driven Development (SDD)** e **Schema-Driven Development (SDD)** no repositório. O objetivo é garantir que nenhuma linha de código seja gerada ou alterada no modo *Vibe Coding* sem uma especificação formal prévia (*Software Design Document - SDD / RFC*), contratos de dados estritos (*Schema-First*) e mapeamento rigoroso de fronteiras de confiança, casos de borda e invariantes de sistema.

Ao final da auditoria/planejamento, você deve listar os achados e lacunas arquiteturais no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues/RFCs em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique os domínios do sistema, linguagens, frameworks e camadas da aplicação.
2. Identifique todos os documentos de especificação existentes (`/docs`, RFCs, `README.md`, ADRs - *Architecture Decision Records*, diagramas C4).
3. Identifique e analise TODOS os arquivos de Schema e Contrato:
   - **Schemas de Validação:** Schemas Zod, Joi, Yup, TypeBox, Pydantic, Marshmallow, etc.
   - **Schemas de Banco de Dados:** Migrações, schemas Prisma, Drizzle, SQLAlchemy, TypeORM, DDLs SQL.
   - **Contratos de Interface:** Especificações OpenAPI/Swagger, AsyncAPI, esquemas GraphQL, arquivos `.proto` (gRPC).
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Verifique se o código em produção diverge das especificações e schemas mapeados (*Spec Drift*).

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (SPEC-DRIVEN & SCHEMA-DRIVEN DEVELOPMENT)

### 1. Governança e Integridade de Especificação (Spec-Driven / RFCs)
- [ ] **Existência de Software Design Documents (SDD):** Verifique se funcionalidades complexas ou fluxos críticos (auth, pagamentos, billing, processamento assíncrono) possuem documentos de design técnico contendo: Metas (*Goals*), Não-Metas (*Non-Goals*), Arquitetura, Modelo de Dados, Riscos e Estratégia de Rollback.
- [ ] **Prevenção de "Vibe Coding Desgovernado":** Identifique código implementado diretamente sem especificação formal de requisitos, gerando arquivos desestruturados, duplicação de lógicas de negócio ou arquiteturas circulares.
- [ ] **Mapeamento Explícito de Casos de Borda (*Edge Cases*):** Verifique se o design do sistema documenta o comportamento para timeouts, perda de conectividade com banco/serviços externos, duplicidade de requisições e concorrência simultânea.
- [ ] **Architecture Decision Records (ADRs):** Verifique se as decisões técnicas estruturais (escolha de banco, padrões de mensageria, bibliotecas de criptografia) estão documentadas com contexto, alternativas avaliadas e consequências.

### 2. Fonte Única da Verdade e Tipagem (Schema-Driven / Single Source of Truth)
- [ ] **Validação Estrita na Borda (Schema Parsing):** Verifique se TODAS as entradas de dados (HTTP Body, Query Params, Headers, Mensagens de Filas, Webhooks) são parseadas e validadas por schemas formais antes de atingirem a lógica de negócio (`schema.parse()` / `schema.safeParse()`).
- [ ] **Type-Safety End-to-End (Inferência de Tipos):** Verifique se os tipos de domínio e DTOs são estritamente derivados dos Schemas (ex: `z.infer<typeof UserSchema>`), eliminando tipagens manuais duplicadas (`interface User`) que possam divergir do validador.
- [ ] **Rejeição de Propriedades Desconhecidas (Anti-Mass Assignment):** Garanta que os schemas de entrada operam em modo estrito (ex: `z.object({...}).strict()`), rejeitando ou eliminando explicitamente campos extras injetados pelo cliente.
- [ ] **Compartilhamento de Schemas (Fullstack Consistency):** Em aplicações fullstack (Node/React, Next.js, etc.), verifique se o frontend e o backend compartilham os mesmos schemas de validação, evitando divergência de regras entre cliente e servidor.

### 3. Sincronização entre Schema de Banco e Schema de Aplicação (ORM/DB Sync)
- [ ] **Detecção de Schema Drift:** Verifique se as entidades do ORM / schemas de validação de aplicação estão 100% alinhados com o estado real das tabelas no banco de dados (tipos primitivos, nulabilidade, constraints de unicidade e chaves estrangeiras).
- [ ] **Tratamento de Enums e Constantes no Schema:** Verifique se estados finitos (ex: `PENDING`, `APPROVED`, `REJECTED`) são declarados como Enums tipados tanto no banco de dados quanto nos schemas de aplicação, impedindo strings arbitrárias.
- [ ] **Transformações e Sanitizações no Schema:** Verifique se o schema realiza transformações e coerções seguras (ex: `.trim()`, `.toLowerCase()`, conversão de datas ISO para objetos `Date`) logo no momento da validação inicial.

### 4. Gestão de Mudanças e Versionamento de Contratos
- [ ] **Prevenção de Breaking Changes em Schemas:** Identifique alterações em campos obrigatórios de schemas públicos que quebram retrocompatibilidade sem versionamento explícito (`/v1/`, `/v2/`).
- [ ] **Depreciação Controlada:** Verifique se campos em desuso são marcados formalmente como obsoletos (`@deprecated` no OpenAPI/GraphQL) antes de sua remoção física.
- [ ] **Geração Automatizada de Artefatos:** Verifique se a documentação de API (`openapi.json`), clientes SDK e mocks de teste são gerados automaticamente a partir dos Schemas centrais.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/modules/billing/schema.ts:18` | Schema / Mass Assignment | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `docs/architecture/` | Falta de SDD / Spec Drift | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [Spec Governance / Schema-First / Type-Safety / Schema Drift / Versionamento]
- **Problema:** Explicação direta do risco arquitetural ou de segurança causado pela ausência de spec ou fragilidade do schema.
- **Evidência:** Trecho do código-fonte ou documentação atual.
- **Correção Recomendada:** Código com o Schema Zod/OpenAPI ou template de SDD estruturado.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/sdd-audit/relatorio-auditoria-sdd.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria e Governança SDD (Spec & Schema-Driven) — <nome do projeto>", data, escopo auditado e metodologia de validação de schemas e especificações.
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria de falha de schema/spec.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (schemas bem modelados, tipagem end-to-end) e **Pontos Fracos** (riscos de spec drift, falta de validação estrita).
d) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição, com chip de severidade e tag de Quick Win.
e) **Template Oficial de Software Design Document (SDD):** Modelo padrão em Markdown para guiar o time em novas funcionalidades.
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[SDD/Arquitetura] <descrição curta da falha>`
   - Labels sugeridas: `architecture` + `schema` ou `spec-drift` + severidade
   - Descrição do problema e impacto no ciclo de desenvolvimento e segurança
   - Evidência: `arquivo:linha` com trecho de código
   - Impacto na confiabilidade e manutenção
   - Sugestão de correção com schema tipado
   - Critérios de aceite (checklist verificável)

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Não instale pacotes globalmente no sistema. Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`).
- Deixe o script gerador salvo no diretório `docs/sdd-audit/` para que o relatório possa ser regerado futuramente.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/sdd-audit/relatorio-auditoria-sdd.pdf`, `docs/sdd-audit/generate_report.py`).
