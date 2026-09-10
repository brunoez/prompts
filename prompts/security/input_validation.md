# PROMPT DE AUDITORIA COMPLETA: VALIDAÇÃO DE ENTRADA & TRATAMENTO DE EXCEÇÕES (OWASP PROACTIVE CONTROL C3) E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Design Defensivo (Yellow Team). Sua missão é realizar uma varredura completa no repositório aplicando o **OWASP Top 10 Proactive Controls 2024 — C3: Validate all Input & Handle Exceptions** e as diretrizes do **OWASP Cheat Sheet Series** (*Input Validation, Mass Assignment, Deserialization, File Upload, Unicode Encoding, Error Handling, Injection Prevention, Query Parameterization, OS Command Injection Defense, LDAP Injection Prevention, XML External Entity Prevention*), reforçadas por **WSTG-INPV** e **WSTG-ERRH**.

A auditoria deve garantir validação sintática e semântica de toda entrada em cada fronteira de confiança (*allow-list* / positive validation), canonicalização antes de validar, rejeição de dados malformados com *fail closed*, tratamento centralizado de exceções sem vazamento de detalhes internos, e ausência de dependência de sanitização como única defesa.

> **Nota de escopo:** este prompt cobre a disciplina transversal de validação e exceções. Vetores de injeção específicos e profundos são aprofundados em `api.md` (SSTI, ReDoS, uploads), `db.md` (SQLi/NoSQLi) e `frontend.md` (DOM XSS). Use-os em conjunto.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique a stack e as bibliotecas de validação/parsing (`zod`, `joi`, `yup`, `class-validator`, `ajv`, `valibot`, `pydantic`, `marshmallow`, `cerberus`, `go-playground/validator`, Bean Validation/`jakarta.validation`).
2. Identifique TODAS as fronteiras de confiança onde entra dado não confiável: bodies HTTP/JSON/form/multipart, query e path params, headers e cookies, mensagens de fila (Kafka/SQS/Rabbit), payloads de webhook, arquivos importados (CSV/XML/XLSX/JSON), argumentos de CLI, variáveis de ambiente usadas como dado, respostas de APIs de terceiros e conteúdo lido de storage.
3. Para cada fronteira, verifique se há schema de validação aplicado **antes** de qualquer uso do dado, e se o resultado usado adiante é o dado **parseado/coagido pelo schema** (não o objeto cru original).
4. Identifique os *sinks* perigosos alcançados por dados de entrada: queries, `exec`/`spawn`/`system`, `eval`/`Function`, template engines, `fs`/path, deserializadores (`pickle`, `yaml.load`, `Marshal`, `ObjectInputStream`, `unserialize`), parsers XML, redirects, e headers de resposta.
5. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.
6. **Diretriz Anti-Fadiga e Anti-Alucinação (Filtro Factual):** Só reporte falhas categoricamente comprovadas por um caminho de dado não validado até um uso sensível. É proibido levantar hipóteses sem evidência. Itens sem impacto real devem ser `[NIT]` ou descartados, com foco no *Blast Radius*.

---

## CHECKLIST DE AUDITORIA PRÁTICA (OWASP PROACTIVE C3 & CHEAT SHEETS)

### 1. Validação Positiva (Input Validation Cheat Sheet — WSTG-INPV)
- [ ] **Allow-List, não Deny-List:** Verifique que a validação define o que é aceitável (tipo, formato, faixa, comprimento, enum) e rejeita o resto — não tenta enumerar caracteres/padrões perigosos.
- [ ] **Validação Sintática e Semântica:** Além do formato (ex: é um e-mail bem formado, é uma data ISO), verifique regras de negócio (data não no passado, valor > 0, `endDate > startDate`, país na lista suportada).
- [ ] **Aplicada no Servidor e em Toda Fronteira:** Validação no cliente é UX, não segurança. Verifique validação server-side em cada entrypoint, inclusive consumidores de fila e webhooks (frequentemente esquecidos).
- [ ] **Uso do Valor Parseado:** Verifique que o código adiante usa o objeto retornado pelo schema (tipado/coagido/com defaults) e não o `req.body` cru — evita *type confusion* e campos não declarados.
- [ ] **Limites Explícitos:** Comprimento máximo de strings, tamanho máximo de arrays, profundidade máxima de JSON, tamanho máximo do corpo da requisição, número máximo de campos multipart — todos com teto definido (anti-DoS).
- [ ] **Canonicalização antes da Validação (Unicode Encoding Cheat Sheet):** Verifique normalização Unicode (NFC/NFKC), decodificação única e consistente de URL/percent-encoding, e normalização de path **antes** de validar/comparar — evita bypass por dupla codificação, homóglifos e `..%2f`.

### 2. Tipos Estruturais e Coerção
- [ ] **Schema Estrito (sem passthrough):** Verifique `zod.strict()`/`additionalProperties: false`/`extra="forbid"` — objetos com campos inesperados devem ser rejeitados, não silenciosamente aceitos.
- [ ] **Mass Assignment / Object Injection (Mass Assignment Cheat Sheet):** Verifique *allow-list* de propriedades graváveis em create/update; campos sensíveis (`role`, `isAdmin`, `ownerId`, `tenantId`, `balance`, `status`, `createdAt`) nunca vêm do input do cliente.
- [ ] **Type Juggling:** Verifique validação de tipo real em linguagens dinâmicas (`"0"` vs `0` vs `false`, arrays onde se espera string — `?id[]=` — quebrando comparações e queries).
- [ ] **Números:** Faixa (`min`/`max`), inteiro vs decimal, precisão monetária (sem `float` para dinheiro), `NaN`/`Infinity` rejeitados.

### 3. Deserialização e Parsing (Deserialization + XXE Cheat Sheets)
- [ ] **Deserialização Insegura:** Sem `pickle.loads`, `yaml.load` (sem `SafeLoader`), `Marshal.load`, `ObjectInputStream` nativo, `unserialize()` PHP ou `Function`/`eval` sobre dado não confiável. Preferir formatos de dados puros (JSON) com schema.
- [ ] **XXE / Entidades Externas:** Parsers de XML/SVG/DOCX/SOAP com `DOCTYPE`, entidades externas e resolução de rede desabilitadas explicitamente.
- [ ] **Zip/Arquivo Comprimido:** Proteção contra *zip bomb* (limite de razão de descompressão e tamanho total) e *zip slip* (path traversal na extração).
- [ ] **CSV/Planilha:** Neutralização de *formula injection* (`=`, `+`, `-`, `@` no início de célula) ao gerar arquivos consumidos por Excel/Sheets.

### 4. Passagem Segura para Sinks (Injection Prevention Cheat Sheets)
- [ ] **Parametrização, não Concatenação:** Queries SQL/NoSQL sempre parametrizadas/ORM seguro; comandos de SO via array de args sem shell (`execFile`/`spawn` sem `shell: true`), nunca string interpolada; LDAP/XPath com escaping da biblioteca.
- [ ] **Sanitização como Defesa Secundária:** Verifique que sanitização (ex: DOMPurify, bleach) complementa — e não substitui — output encoding contextual e validação; nenhuma proteção depende só de "remover tags".
- [ ] **Redirects e Headers:** Parâmetros de redirect validados contra allow-list de rotas internas (sem *open redirect*); valores refletidos em headers de resposta sem CR/LF (*response splitting*).
- [ ] **Path e Nome de Arquivo:** Caminhos derivados de input resolvidos (`path.resolve`) e confinados a um diretório raiz; nomes de arquivo gerados pelo servidor, não pelo cliente.

### 5. Tratamento de Exceções e Erros (Error Handling Cheat Sheet — WSTG-ERRH)
- [ ] **Fail Closed:** Verifique que falha de validação, erro de parsing ou exceção não tratada resulta em rejeição (`4xx`) e negação da operação — nunca em prosseguir com valor default silencioso ou `try/except: pass`.
- [ ] **Handler Global Centralizado:** Existe um *error handler* único que mapeia exceções para respostas seguras e padronizadas; controllers não montam mensagens de erro ad-hoc com detalhes internos.
- [ ] **Sem Vazamento:** Respostas de erro não contêm stack trace, caminho de arquivo, versão de framework, SQL, nomes de tabela/coluna, valores de config ou trecho de query. Mensagem genérica para o cliente + detalhe completo só no log server-side (com ID de correlação).
- [ ] **Sem Segredo em Log de Erro:** Exceções não logam corpo de requisição com senha/token/PII sem redação (conectar com Proactive C9 / `resilience_observability.md`).
- [ ] **Consistência:** Erros de validação retornam código e formato consistentes (ex: `422` + lista de campos), sem diferença de tempo/detalhe que sirva de oráculo (enumeração, existência de recurso).
- [ ] **Recursos Liberados:** `finally`/`defer`/context manager garante fechamento de conexões, arquivos e locks mesmo em erro.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica, exiba no chat a lista detalhada de achados ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados:

| ID | Arquivo / Ponto | Módulo / Padrão | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/consumers/order.ts:19` | Mensagem de fila usada sem validação de schema | ALTA | Baixo (40 min) | **SIM** |
| #2 | `src/controllers/user.ts:52` | Mass assignment: `role` aceito do body | CRÍTICA | Baixo (20 min) | **SIM** |
| #3 | `src/middleware/error.ts:8` | Stack trace retornado ao cliente em `500` | ALTA | Baixo (30 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item da tabela:
- **Achado #[ID]:** [Nome do Problema]
- **Controle / Cheat Sheet:** [ex: Proactive C3 / Mass Assignment Cheat Sheet / WSTG-INPV-11 / WSTG-ERRH-01]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Vetor de Ataque / Exploração:** Como um atacante explora a falha (payload malformado, campo extra, dupla codificação, exceção provocada para extrair detalhe).
- **Evidência:** Trecho do código-fonte vulnerável (fronteira sem validação → sink / handler que vaza).
- **Prova de Conceito (PoC / Reprodução):** Requisição reproduzível (`curl` / mensagem de fila) demonstrando a falha no contexto do projeto.
- **Correção Recomendada:** Schema *allow-list* estrito aplicado na fronteira + handler de erro seguro, com uso do valor parseado.
- **Comando de Verificação da Correção:** Como validar em 1 comando (teste que envia payload inválido e espera `422`/rejeição sem vazamento).

---

## GERAÇÃO DE RELATÓRIO PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script automatizado salvo em `docs/input-validation-audit/generate_report.py` para produzir:

1. **Relatório em PDF (`docs/input-validation-audit/relatorio-auditoria-validacao.pdf`):**
   - **Capa:** Título "Relatório de Auditoria de Validação de Entrada & Exceções (OWASP Proactive C3) — <nome do projeto>", data e escopo.
   - **Resumo Executivo:** Gráfico de rosca por severidade e gráfico de barras por categoria (Validação Positiva, Tipos/Coerção, Deserialização, Sinks, Tratamento de Exceções).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
   - **Mapa de Fronteiras de Confiança:** Tabela de cada entrypoint, tipo de entrada, schema aplicado (sim/não) e sinks alcançados.
   - **Tabela Detalhada de Achados** com tags de Quick Win e referências a arquivos e linhas.

2. **Seção "ISSUES PARA O GITHUB" no Relatório:**
   - Template Markdown completo pronto para copiar e colar para cada achado, com labels, passos de reprodução, impacto e critérios de aceite.

### REGRAS TÉCNICAS
- Use ambiente Python isolado (`venv` temporário com `reportlab` e `matplotlib`).
- Salve o script e os artefatos em `docs/input-validation-audit/`.
- Garanta formatação A4 impecável, paginação correta e sem quebras visuais em tabelas.

---

## ENTREGÁVEIS FINAIS
Ao concluir, informe no chat:
1. A confirmação da geração do relatório PDF.
2. A lista de achados (Parte 1 e Parte 2).
3. O caminho relativo dos arquivos gerados (`docs/input-validation-audit/relatorio-auditoria-validacao.pdf`, `docs/input-validation-audit/generate_report.py`).
