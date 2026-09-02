# PROMPT DE AUDITORIA COMPLETA: LÓGICA DE NEGÓCIO, FALHAS TRANSACIONAIS (OWASP BUSINESS LOGIC) E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Software e Especialista em AppSec (Business Logic & Financial Integrity Lead). Sua missão é realizar uma varredura completa no repositório para identificar **falhas na lógica de negócio (Business Logic Flaws)** e vulnerabilidades transacionais — categorias contextuais e arquiteturais que scanners DAST/SAST tradicionais não conseguem detectar.

A auditoria deve aplicar as diretrizes do **OWASP Business Logic Security Cheat Sheet Series** e os testes de lógica de negócio do **OWASP WSTG v4.2** (*WSTG-BUSL*), garantindo prevenção contra fraudes financeiras, manipulação de estado, uploads maliciosos em fluxos de negócio, burla de fluxos (*workflow bypass*), ataques de repetição (*replay attacks*), poluição de parâmetros (HPP) e ausência de trilhas de auditoria/não-repúdio.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique os domínios centrais da aplicação (ex: e-commerce, pagamentos/fintech, reservas/booking, planos/assinaturas SaaS, jogos/apostas, cupons/pontos, processamento de documentos, etc.).
2. Leia todos os arquivos de documentação, diagramas de máquina de estado, contratos de API e especificações de regras de negócio (`README.md`, `/docs`, RFCs internas, especificações OpenAPI).
3. Identifique e analise TODOS os arquivos da camada de domínio, casos de uso (*Use Cases*), *Services*, *State Machines*, processadores de checkout/pagamento, validadores de regras de negócio, manipuladores de eventos de domínio, uploads de comprovantes/documentos, jobs assíncronos e lógicas de carrinho/saldo.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Compreenda a *intenção* do fluxo de negócio antes de auditar a robustez de sua implementação.

---

## CHECKLIST DE AUDITORIA PRÁTICA (OWASP BUSINESS LOGIC & WSTG-BUSL)

### 1. Integridade Transacional, Preços e Idempotência (OWASP Transaction Authorization)
- [ ] **Manipulação de Preço, Desconto e Quantidade:** Identifique se o backend confia em preços, taxas, descontos ou valores totais enviados no payload da requisição pelo cliente, em vez de recalculá-los exclusivamente no backend com base no estado do banco de dados seguro.
- [ ] **Chaves de Idempotência em Transações Críticas:** Verifique se endpoints mutativos (pagamento, transferência, estorno, emissão de nota, envio de ordens) exigem e validam cabeçalhos `Idempotency-Key` com locks distribuídos, evitando processamento em dobro ou *double charge* em retentativas automáticas de rede.
- [ ] **Underflows, Decimais e Fraudes Numéricas:** Verifique a ausência de validação para quantidades negativas ou zero (ex: comprar `-5` itens para gerar crédito em conta) e falhas de precisão/arredondamento em ponto flutuante em operações financeiras (ex: exigir tipos `Decimal` / `BigInt` / centavos inteiros).
- [ ] **Abuso de Cotas e Cupons de Uso Único:** Identifique se o resgate de cupons, bônus de boas-vindas ou limites de planos gratuitos validam a unicidade atomicamente, impedindo que um mesmo cupom seja aplicado múltiplas vezes em paralelo ou em abas diferentes.

### 2. Quebra de Fluxo, Máquina de Estado e Uploads de Negócio (WSTG-BUSL)
- [ ] **Pulo de Etapas Obrigatórias (Skip-Step / Forced Browsing):** Verifique se fluxos em múltiplas etapas (ex: Carrinho $\rightarrow$ KYC $\rightarrow$ Pagamento $\rightarrow$ Conclusão) validam rigorosamente a conclusão e assinatura de cada etapa prévia no backend antes de permitir a próxima (impedindo acesso direto a rotas de conclusão).
- [ ] **Transições de Estado Inválidas (State Machine Corruption):** Identifique se a aplicação permite transições de estado ilegais no domínio (ex: cancelar um pedido já marcado como "Entregue", estornar uma transação "Rejeitada", ou reabrir um ticket "Fechado").
- [ ] **Uploads Maliciosos em Fluxos de Negócio (WSTG-BUSL-08/09):** Em fluxos que aceitam comprovantes, notas fiscais, fotos de perfil ou planilhas CSV/XML, verifique se há validação de **Magic Bytes** reais, renomeação segura com UUID para evitar Path Traversal (`../../`), e proteção contra XML External Entity (XXE) e CSV Injection.
- [ ] **Burla de MFA e Verificação de Identidade no Domínio:** Verifique se fluxos de login com MFA, redefinição de senha ou autorização de alto valor permitem pular a etapa de desafio alterando o estado da sessão ou enviando payloads incompletos.

### 3. Condições de Corrida e Concorrência Maliciosa (OWASP Race Conditions)
- [ ] **Time-of-Check to Time-of-Use (TOCTOU):** Identifique se a aplicação verifica uma condição (ex: `saldo >= valor_saque` ou `estoque > 0`) e, em seguida, executa a ação sem garantir atomicidade ou *lock*, permitindo que requisições paralelas passem pela checagem simultaneamente antes do débito no banco.
- [ ] **Resgate Concorrente de Recursos Limitados (Limit-Overrun):** Verifique ausência de locks pessimistas (`SELECT ... FOR UPDATE`), locks distribuídos (Redis Redlock) ou updates atômicos em operações de saque, reservas de assentos ou resgates de brindes.

### 4. Poluição de Parâmetros, Replay e Não-Repúdio (OWASP Business Integrity)
- [ ] **HTTP Parameter Pollution (HPP):** Verifique se o processamento de listas de parâmetros repetidos na query ou formulário (ex: `item_id=1&item_id=2` ou `discount=10&discount=90`) pode levar a discrepâncias na lógica de cálculo entre camadas de gateway/WAF e o serviço backend.
- [ ] **Ataques de Replay e Validade Temporal:** Verifique se requisições financeiras, callbacks de parceiros e links de autorização possuem validação de expiração temporal estrita (*timestamp window* curto) e uso de nonces únicos contra reenvio de pacotes capturados.
- [ ] **Trilha de Auditoria Imutável (Audit Trail & Non-Repudiation):** Identifique operações sensíveis de negócio (alteração de limites de crédito, cancelamento de débitos, estornos, concessão de permissões corporativas) que não registram logs de auditoria estruturados (Quem, Quando, O Quê, IP, Fingerprint, Valor Anterior vs Valor Novo).
- [ ] **Proteção Anti-Automação por Fluxo de Negócio:** Identifique endpoints sensíveis de negócio desprotegidos contra bots (criação em massa de contas para farmar benefícios, scraping de inventário/preços, ou brute-force em códigos promocionais).

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados:

| ID | Arquivo / Ponto | Categoria OWASP | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/services/checkout.ts:88` | Confiança em Preço de Cliente | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `src/services/wallet.ts:42` | TOCTOU / Saldo Concorrente | CRÍTICA | Médio (1 hr) | NÃO |
| #3 | `src/flows/receiptUpload.ts:25` | WSTG Upload (No Magic Bytes) | ALTA | Baixo (20 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [Manipulação de Preço / TOCTOU & Concorrência / Workflow Bypass / Upload de Negócio / Idempotência / Auditoria]
- **Cenário de Abuso & Impacto Financeiro:** Como um atacante explora essa falha lógica na prática para gerar prejuízo financeiro, roubo de inventário ou corrupção de estado.
- **Evidência:** Trecho do código-fonte atual identificado no repositório.
- **Correção Recomendada:** Código corrigido ou arquitetura recomendada (ex: transações atômicas, máquina de estado finita, validação estrita no backend).

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/business-logic-audit/relatorio-auditoria-logica.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Lógica de Negócio e Integridade Transacional (OWASP Standards) — <nome do projeto>", data, escopo auditado e nota metodológica.
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria de risco de negócio.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (regras de negócio blindadas, com evidência) e **Pontos Fracos** (os riscos centrais de fraude ou manipulação).
d) **Matriz de Conformidade OWASP Business Logic:** Tabela de status para integridade de preços, máquina de estados, concorrência e idempotência.
e) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição, com indicação/chip de severidade e tag de Quick Win.
f) **Recomendações Priorizadas** (P1, P2, P3...).
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[Business Logic/Fraude] <descrição curta da falha>`
   - Labels sugeridas: `security`, `business-logic`, `financial-risk` + severidade
   - Descrição do problema e cenário de abuso (passo a passo de reprodução)
   - Evidência: `arquivo:linha` com trecho de código
   - Impacto no negócio (fraude, perda financeira, inconsistência contábil)
   - Sugestão de correção detalhada
   - Critérios de aceite (checklist verificável)

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (`venv` Python com `reportlab` + `matplotlib`).
- Salve o script gerador em `docs/business-logic-audit/generate_report.py`.
- Formatação das páginas: tamanho A4, margens de 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS
Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/business-logic-audit/relatorio-auditoria-logica.pdf`, `docs/business-logic-audit/generate_report.py`).