# PROMPT DE AUDITORIA COMPLETA: LÓGICA DE NEGÓCIO (BUSINESS LOGIC FLAWS), INTEGRIDADE E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Software e Especialista em AppSec (Foco em Lógica de Negócio). Sua missão é realizar uma varredura completa no repositório para identificar **falhas na lógica de negócio (Business Logic Flaws)** — vulnerabilidades contextuais e arquiteturais que scanners automatizados não conseguem detectar. O foco é prevenir fraudes financeiras, manipulação de estado, burla de fluxos (*workflow bypass*), condições de corrida em regras de negócio e escalonamento de privilégios.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique os domínios centrais da aplicação (ex: e-commerce, finanças, reservas, SaaS, etc.).
2. Leia todos os arquivos de documentação, diagramas de máquina de estado e especificações de regras de negócio (`README.md`, `/docs`, RFCs internas).
3. Identifique e analise TODOS os arquivos da camada de domínio e serviços: Casos de uso (*Use Cases*), *Services*, *State Machines*, processadores de pagamento/checkout, validadores de regras de negócio, manipuladores de eventos de domínio e lógicas de carrinho/assinatura.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Compreenda a *intenção* da regra de negócio antes de apontar a vulnerabilidade.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (BUSINESS LOGIC FLAWS)

### 1. Manipulação de Transações e Integridade de Dados
- [ ] **Manipulação de Preço e Quantidade:** Identifique se o backend confia em preços, descontos ou valores totais enviados diretamente pelo cliente na requisição, em vez de recalcular com base no ID do produto no banco de dados seguro.
- [ ] **Valores Negativos e Limites (Integer/Float Underflow):** Verifique a ausência de validação para quantidades negativas ou zero (ex: comprar `-5` itens para gerar crédito na conta) e falhas de arredondamento em cálculos financeiros (ex: *floating-point math*).
- [ ] **Abuso de Limites e Cotas:** Identifique se há falta de controle rígido em limites de uso, como aplicar cupons de "uso único" múltiplas vezes, solicitar múltiplos saques simultâneos ou exceder a cota de uso de uma API do plano gratuito.

### 2. Quebra de Fluxo e Máquina de Estado (Workflow Bypass)
- [ ] **Pulo de Etapas Obrigatórias (Skip-Step):** Verifique se fluxos em múltiplas etapas (ex: Carrinho $\rightarrow$ Pagamento $\rightarrow$ Recibo) validam rigorosamente em cada rota se a etapa anterior foi concluída com sucesso. Identifique se é possível acessar `/checkout/success` sem passar pela transação financeira.
- [ ] **Inconsistência de Estado (State Manipulation):** Identifique se a aplicação permite transições de estado inválidas no domínio (ex: cancelar um pedido que já foi "Enviado", ou estornar um pagamento "Recusado").
- [ ] **Burla de Verificação de Identidade/MFA:** Verifique se o fluxo de autenticação de múltiplos fatores ou recuperação de senha permite pular a etapa de verificação de token alterando o estado da sessão ou da requisição.

### 3. Condições de Corrida no Negócio (Business Race Conditions)
- [ ] **Time-of-Check to Time-of-Use (TOCTOU):** Identifique se a aplicação verifica uma condição (ex: `saldo >= valor_saque` ou `estoque > 0`) e, em seguida, executa a ação sem garantir atomicidade ou *lock*, permitindo que múltiplas requisições simultâneas passem pela verificação antes do desconto no banco.
- [ ] **Abuso de Uso Concorrente (Simultaneous Transactions):** Verifique a ausência de bloqueios transacionais ao aplicar descontos, resgatar prêmios, ou reservar assentos, permitindo resgates duplicados.

### 4. Confiança Indevida e Escalonamento de Privilégios (Domain Level)
- [ ] **Confiança no Cliente para Regras de Domínio:** Identifique payloads de atualização (ex: `PUT /api/users/me`) que aceitam e processam campos que deveriam ser protegidos pela lógica de negócio (ex: forçar `"status": "ACTIVE"` ou `"subscription_valid_until": "2099-01-01"`).
- [ ] **Reutilização de Identificadores Gessados:** Verifique se links de expiração, tokens de redefinição de senha ou carrinhos de compra falham em ser invalidados imediatamente após o primeiro uso com sucesso.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/services/checkout.ts:88` | Integridade (Confiança no Preço) | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `src/flows/orderState.ts:45` | Workflow Bypass (Estado Inválido) | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [Manipulação Financeira / Quebra de Fluxo / Condição de Corrida / Confiança Indevida / Estado]
- **Problema:** Explicação direta de como um atacante poderia abusar dessa falha lógica para gerar prejuízo financeiro, roubo de serviços ou corrupção de estado.
- **Evidência:** Trecho do código-fonte atual identificado no repositório.
- **Correção Recomendada:** Código corrigido ou arquitetura recomendada (ex: validações no backend, uso de máquinas de estado finitas, validação em cada etapa).

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/business-logic-audit/relatorio-auditoria-logica.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Lógica de Negócio (Business Logic) — <nome do projeto>", data, escopo auditado e nota metodológica.
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (regras de negócio blindadas, com evidência) e **Pontos Fracos** (os riscos centrais de fraude ou manipulação).
d) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição, com indicação/chip de severidade e tag de Quick Win.
e) **Recomendações Priorizadas** (P1, P2, P3...).
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[Business Logic/Fraude] <descrição curta da falha>`
   - Labels sugeridas: `security`, `business-logic`, `bug` + severidade
   - Descrição do problema e cenário de abuso (como explorar)
   - Evidência: `arquivo:linha` com trecho de código
   - Impacto (ex: fraude financeira, bypass de pagamento)
   - Sugestão de correção (mudança na regra ou validação)
   - Critérios de aceite (checklist verificável)
   *(Nota: Agrupe achados triviais relacionados numa issue única quando fizer sentido).*

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Não instale pacotes globalmente no sistema. Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`, ou ferramentas equivalentes locais como `puppeteer`/HTML-to-PDF).
- Deixe o script gerador salvo no diretório `docs/business-logic-audit/` para que o relatório possa ser regerado futuramente.
- Verifique o PDF gerado: garanta o número correto de páginas, a renderização adequada dos gráficos e a legibilidade das tabelas.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/business-logic-audit/relatorio-auditoria-logica.pdf`, `docs/business-logic-audit/generate_report.py`).