# PROMPT DE AUDITORIA COMPLETA: BANCO DE DADOS, CONCORRÊNCIA, OWASP DATABASE SECURITY E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Banco de Dados e Especialista em AppSec (Database Security & Data Protection Lead). Sua missão é realizar uma varredura completa no repositório para garantir resiliência, performance, concorrência segura, controle de acesso de menor privilégio, proteção criptográfica em repouso e prevenção ativa contra injeções e vazamentos (Data Leakage), alinhando a auditoria às diretrizes do **OWASP Database Security Cheat Sheet Series** (*Database Security, SQLi Prevention, Query Parameterization, NoSQL Injection, Database Access Control e Cryptographic Storage*), além dos pilares de DDD (limites de transação), ADD (atributos de qualidade) e TDD Concorrente.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios do projeto e identifique a stack/tecnologia utilizada (PostgreSQL, MySQL, MongoDB, Redis, Oracle, DynamoDB, SQL Server, ORMs como Prisma, TypeORM, Hibernate, SQLAlchemy, EF Core, Dapper, etc.).
2. Leia todos os arquivos de documentação e arquitetura existentes (`README.md`, `/docs`, SDD, diagramas ERD, scripts de migração).
3. Identifique e analise TODOS os arquivos com impacto em dados: entidades, ORMs, repositórios, SQLs nativos, procedures/triggers, scripts de migração, configurações de pool e conexão (`DATABASE_URL`), controllers/mappers que tratam requisições/respostas do banco e arquivos de log/exceção.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.
5. **Diretriz Anti-Fadiga e Anti-Alucinação (Filtro Factual):** Só reporte vulnerabilidades que possam ser categoricamente comprovadas pelo código-fonte ou configurações inspecionadas. É proibido levantar suposições hipotéticas sem evidência no repositório. Recomendações puramente cosméticas ou de estilo sem impacto real de segurança devem ser marcadas como `[NIT]` ou descartadas, mantendo o foco estrito no risco real e no raio de impacto (*Blast Radius*).

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP DATABASE SECURITY & ARQUITETURA)

### 1. Segurança de Acesso, Privilégios e Conexão (OWASP Database Access Control & Security)
- [ ] **Princípio do Menor Privilégio no Banco:** Verifique se a aplicação conecta no banco utilizando superusuários (`root`, `postgres`, `sa`, `admin`) ou roles com permissões DDL amplas (`DROP`, `ALTER`, `GRANT`, `SUPERUSER`), em vez de roles com privilégios estritamente necessários (ex: role DML `app_user` apenas com `SELECT`, `INSERT`, `UPDATE`, `DELETE`).
- [ ] **Transporte Seguro (TLS/SSL Enforced):** Verifique se as strings de conexão e drivers exigem criptografia em trânsito com validação de certificados (ex: `sslmode=verify-full` ou `sslmode=verify-ca` no Postgres, `ssl-mode=VERIFY_IDENTITY` no MySQL), impedindo conexões em texto puro ou vulneráveis a MitM.
- [ ] **Gestão de Conexões e Pool:** Identifique ausência de timeouts de conexão (`connectionTimeout`, `idleTimeout`), conexões não devolvidas ao pool (*Connection Leak*) e retenção indevida de conexões abertas durante operações lentas de I/O externo.
- [ ] **Migrações e Schema:** Verifique se as alterações de banco usam scripts versionados (Flyway, Liquibase, Prisma Migrations) e garanta a ausência de opções perigosas ativas em produção (como `auto-ddl`, `synchronize: true` ou `drop-schema`).

### 2. Prevenção de Injeções e Manipulação de Consultas (OWASP SQLi & NoSQL Prevention)
- [ ] **SQL Injection Direto:** Identifique concatenação, interpolação de strings (`${...}`, `f"..."`, `+`) ou montagem manual de queries SQL dinâmicas (exigir rigorosamente `Prepared Statements` e queries parametrizadas com bind variables).
- [ ] **Injeção em Stored Procedures e Dynamic SQL:** Localize procedures, triggers e funções PL/SQL / PL/pgSQL que utilizam comandos de execução dinâmica (`EXECUTE`, `EXECUTE IMMEDIATE`, `sp_executesql`) sem sanitização ou bind parameters adequados.
- [ ] **NoSQL Operator Injection:** Para bancos NoSQL (MongoDB, DocumentDB), identifique endpoints que passam objetos JSON da requisição diretamente para métodos de busca (ex: `find({ user: req.body.user })`), permitindo injeção de operadores como `{"$gt": ""}`, `{"$ne": null}` ou `{"$regex": "..."}`.
- [ ] **Injeção em Comandos Redis e Eval:** Identifique execução de comandos arbitrários no Redis via interpolação de chaves não sanitizadas ou uso de `EVAL` com scripts Lua contendo entrada de usuário.
- [ ] **Segurança de ORMs e Raw Queries:** Identifique métodos de escape em ORMs (ex: `prisma.$queryRawUnsafe`, `sequelize.literal`, `EntityManager.createNativeQuery`, `typeorm.query`) recebendo dados não parametrizados.

### 3. Proteção Criptográfica e Prevenção de Vazamentos (OWASP Cryptographic Storage)
- [ ] **Criptografia de Colunas Sensíveis em Repouso (Field-Level Encryption):** Verifique se dados altamente confidenciais (PII, números de cartão, dados de saúde, chaves privadas, segredos) estão salvos em texto puro no banco em vez de utilizarem criptografia autenticada (ex: AES-256-GCM / ChaCha20-Poly1305) com chaves gerenciadas em cofre seguro (KMS).
- [ ] **Vazamento via Logs de Banco e Queries:** Identifique se queries SQL completas contendo parâmetros sensíveis ou dados PII são impressas em arquivos de log sem mascaramento (*Data Masking / Redaction*).
- [ ] **Vazamento via Serialização/APIs (Excessive Exposure):** Verifique se entidades do banco/ORM são retornadas diretamente em controllers/endpoints HTTP sem o uso de DTOs, Mappers ou anotações de exclusão (ex: `@JsonIgnore`, `select: false`), expondo colunas internas na resposta JSON.
- [ ] **Vazamento em Tratamento de Exceções:** Identifique se erros SQL nativos, violações de integridade referencial ou *stack traces* de banco são expostos diretamente no payload HTTP de erro para o cliente.

### 4. Limites de Transação, Concorrência e Performance (DDD / ADD / TDD Concorrente)
- [ ] **Dual Write & Consistência:** Identifique escritas sequenciais em múltiplos bancos/serviços (ex: SQL + Redis, SQL + Kafka) no mesmo fluxo sem padrões de resiliência (Transactional Outbox ou CDC).
- [ ] **Escopo e Duração de Transações:** Identifique transações SQL que abraçam chamadas lentas de rede (APIs de terceiros, envios de e-mail, microserviços), retendo locks e conexões desnecessariamente.
- [ ] **Race Conditions & Concorrência:** Identifique operações de leitura-modificação-escrita em recursos compartilhados (saldo, estoque, contadores) sem controle concorrente explícito (Lock Otimista via `@Version`/coluna de versão, Lock Pessimista `SELECT ... FOR UPDATE` ou updates atômicos no SQL).
- [ ] **Deadlocks e Ordem de Acesso:** Verifique se transações simultâneas alteram múltiplos registros/tabelas em ordem cruzada ou inconsistente.
- [ ] **N+1 Queries e Consultas Sem Paginação:** Identifique buscas N+1 em laços de repetição (falta de `Fetch JOINs` / `include`) e consultas globais (`findAll()`, `SELECT *`) sem restrição de paginação com teto máximo (`LIMIT`).

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/repositories/userRepo.ts:42` | OWASP SQLi | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `config/database.ts:18` | Acesso (Superuser / No TLS) | ALTA | Baixo (20 min) | **SIM** |
| #3 | `src/services/walletService.ts:105` | Concorrência (Race Condition) | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [OWASP SQLi / NoSQL Injection / Database Access Control / Cryptographic Storage / Concorrência & Locks / Performance & N+1]
- **Vetor de Exploração / Risco:** Explicação direta de como essa vulnerabilidade pode ser explorada ou causar indisponibilidade/vazamento em produção.
- **Evidência:** Trecho do código-fonte atual identificado no repositório.
- **Prova de Conceito (PoC / Reprodução):** Query, script ou payload reproduzível demonstrando a injeção, falha de lock/concorrência ou violação de menor privilégio.
- **Correção Recomendada:** Código devidamente refatorado aplicando as melhores práticas do OWASP Database Security.
- **Comando de Verificação da Correção:** Como o desenvolvedor valida em 1 comando (teste automatizado ou query segura) que a correção funcionou sem quebrar as operações do banco.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/database-audit/relatorio-auditoria-banco.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Banco de Dados e Segurança (OWASP DB Security) — <nome do projeto>", data, escopo auditado e nota metodológica.
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria OWASP. 
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (o que está protegido no banco, com evidência) e **Pontos Fracos** (os riscos centrais).
d) **Matriz de Conformidade OWASP DB:** Tabela indicando status para cada pilar do OWASP Database Security Cheat Sheet.
e) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição, com indicação/chip de severidade e tag de Quick Win.
f) **Recomendações Priorizadas** (P1, P2, P3...).
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[Database/Segurança] <descrição curta da falha>`
   - Labels sugeridas: `database`, `security`, `performance` + severidade
   - Descrição do problema e cenário de exploração
   - Evidência: `arquivo:linha` com trecho de código
   - Impacto (ex: injeção de dados, exfiltração de dados confidenciais, deadlock em produção)
   - Sugestão de correção com código seguro
   - Critérios de aceite (checklist verificável)

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use ambiente Python isolado (`venv` com `reportlab` + `matplotlib`).
- Salve o script gerador em `docs/database-audit/generate_report.py`.
- Formatação das páginas: tamanho A4, margens de 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS
Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/database-audit/relatorio-auditoria-banco.pdf`, `docs/database-audit/generate_report.py`).