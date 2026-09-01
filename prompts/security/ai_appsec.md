# PROMPT DE AUDITORIA COMPLETA: SEGURANÇA EM APLICAÇÕES COM IA (OWASP TOP 10 FOR LLMS / GENAI) E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de IA/ML e Especialista em AppSec para Inteligência Artificial (Yellow Team / AI Red Teaming). Sua missão é auditar o repositório para identificar vulnerabilidades e riscos emergentes em aplicações que consomem **Modelos de Linguagem (LLMs), Agentes Autônomos, RAG (Retrieval-Augmented Generation) e Integrações de IA Generativa**, alinhando a validação aos padrões do **OWASP Top 10 for Large Language Model Applications**.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todos os pontos de integração com IA: chamadas para APIs de LLM (OpenAI, Anthropic, Gemini, Ollama, LangChain, LlamaIndex), pipelines de RAG, bancos vetoriais (Pinecone, Qdrant, Chroma, PGVector), tools de agentes e renderizadores de resposta de IA.
2. Identifique os prompts de sistema (*System Prompts*), funções expostas a chamadas de ferramentas (*Tool/Function Calling*) e parsers de saída.
3. Você DEVE ler e analisar cada arquivo de integração de IA linha por linha.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP LLM TOP 10)

### 1. Injeção de Prompt (Prompt Injection: Direta e Indireta)
- [ ] **Injeção Direta de Prompt (Jailbreak / System Prompt Override):** Verifique se entradas não confiáveis do usuário são concatenadas diretamente no prompt sem separação estruturada (ex: interpolação de strings em vez de mensagens com papéis `user` / `system`).
- [ ] **Injeção Indireta de Prompt (RAG / External Data Poisoning):** Avalie se dados extraídos de fontes externas (páginas web, e-mails, PDFs de terceiros, documentos indexados) são inseridos no contexto do LLM sem sanitização ou delimitação clara (`<untrusted_content>`), permitindo que instruções maliciosas dentro do documento comandem a IA.

### 2. Manipulação Insegura de Saída (Insecure Output Handling)
- [ ] **Renderização Direta de Conteúdo de IA no Frontend (XSS via LLM):** Identifique se respostas geradas pelo LLM (Markdown, HTML, SVG) são renderizadas diretamente no DOM via `dangerouslySetInnerHTML` ou `v-html` sem sanitização estrita (DOMPurify).
- [ ] **Execução de Código ou Queries Geradas por IA:** Verifique se saídas de LLMs (SQL, comandos shell, código Python/JS) são executadas diretamente pelo backend sem validação em sandbox isolado e checagem estrita de parâmetros parametrizados.

### 3. Agência Excessiva e Autonomia Descontrolada (Excessive Agency)
- [ ] **Ferramentas de Agente com Privilégios Excessivos:** Identifique tools/functions de agentes com permissões destrutivas (ex: `delete_user`, `transfer_funds`, `drop_table`) expostas sem exigência de confirmação humana explícita (*Human-in-the-Loop*).
- [ ] **Falta de Limites de Execução de Agentes:** Verifique se os loops de execução de agentes autônomos possuem travas de contagem máxima de passos (*Max Iterations*), timeouts e limites de gasto de tokens para evitar loops infinitos e estouro de custos (*Denial of Wallet*).

### 4. Vazamento de Dados Sensíveis e Isolamento no RAG (Data Leakage)
- [ ] **Vazamento de PII e Segredos no Contexto do Prompt:** Verifique se dados sensíveis de usuários (senhas, CPFs, cartões, chaves de API) são enviados desnecessariamente nos prompts para o provedor de LLM em nuvem.
- [ ] **Isolamento de Tenants em Bancos Vetoriais:** Verifique se as consultas vetoriais no pipeline de RAG aplicam filtros estritos de tenant/usuário no nível da query vetorial (ex: `filter: { tenant_id: current_tenant }`), impedindo que um usuário recupere trechos confidenciais de outro tenant via busca semântica.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/ai/rag.ts:42` | Falta de Filtro de Tenant em Vetores | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `src/ai/agent.ts:110` | Excessive Agency sem Confirmação | ALTA | Médio (45 min) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome da Vulnerabilidade em IA]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [Prompt Injection / Insecure Output / Excessive Agency / RAG Isolation / Data Leakage]
- **Problema:** Explicação direta de como um usuário malicioso pode burlar a IA ou acessar dados confidenciais.
- **Evidência:** Trecho de código com a integração de IA vulnerável.
- **Correção Recomendada:** Código corrigido com guardrails e sanitização aplicados.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/ai-audit/relatorio-auditoria-ai.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Segurança em Aplicações com IA (OWASP LLM Top 10) — <nome do projeto>", data, modelos/frameworks avaliados e escopo.
b) **Resumo Executivo:** Total de riscos de IA por severidade, gráfico de rosca de severidade e gráfico de barras por categoria OWASP LLM.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (uso de guardrails, isolamento de RAG) e **Pontos Fracos** (injeções potenciais, excesso de agência).
d) **Tabela de Achados Detalhados:** Severidade | Componente IA | Risco Identificado | Mitigação.
e) **Guia de Guardrails e Defesa Ativa para LLMs.**
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada brecha de IA mapeada, a issue com a mitigação recomendada.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`).
- Deixe o script gerador salvo no diretório `docs/ai-audit/`.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/ai-audit/relatorio-auditoria-ai.pdf`, `docs/ai-audit/generate_report.py`).
