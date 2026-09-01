# PROMPT DE MODELAGEM DE AMEAÇAS (THREAT MODELING): FRAMEWORK STRIDE, ARQUITETURA DEFENSIVA E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Segurança de Aplicações e Especialista em Arquitetura Defensiva (Yellow Team Lead). Sua missão é conduzir uma sessão aprofundada de **Modelagem de Ameaças (Threat Modeling)** no repositório, utilizando os frameworks **STRIDE** e **PASTA**. O objetivo é identificar proativamente superfícies de ataque, fronteiras de confiança (*Trust Boundaries*), fluxos de dados sensíveis (DFD) e vetores de exploração antes que cheguem a produção, definindo a matriz de contramedidas arquiteturais necessárias.

Ao final da modelagem de ameaças, você deve listar os riscos no chat/terminal e gerar um relatório completo em formato PDF e templates de Contramedidas/Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a arquitetura global do repositório: serviços backend, bancos de dados, storages, filas, gateways, caches, integrações de terceiros e clientes web/mobile.
2. Identifique todos os pontos de entrada e saída de dados (*Ingress/Egress*), fronteiras de confiança e fluxos de autenticação/autorização.
3. Você DEVE ler e analisar cada componente de infraestrutura e código que processa ou armazena dados confidenciais (PII, tokens, dados financeiros).

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (THREAT MODELING - STRIDE)

### 1. Spoofing (Falsificação de Identidade)
- [ ] **Falsificação de Usuários e Clientes:** Avalie se atacantes podem forjar tokens de autenticação, forjar headers de proxy (`X-Forwarded-For`, `X-User-Id`), reutilizar sessões roubadas ou clonar identidades sem validação criptográfica no backend.
- [ ] **Falsificação de Serviços Internos (Service Spoofing):** Verifique se microsserviços confiam cegamente em chamadas internas na mesma VPC sem mTLS ou tokens de serviço-a-serviço (JWTs assimétricos).

### 2. Tampering (Adulteração de Dados)
- [ ] **Adulteração em Trânsito:** Verifique se todas as comunicações (internas e externas) exigem TLS 1.3/1.2 com cifras seguras, impedindo ataques de Man-in-the-Middle (MitM).
- [ ] **Adulteração de Parâmetros e Estado:** Identifique se parâmetros críticos de negócio (preços, permissões, status de pedidos) podem ser alterados no cliente ou em trânsito sem validação de integridade (HMAC / assinaturas digitais).

### 3. Repudiation (Não-Repúdio e Auditoria)
- [ ] **Trilha de Auditoria Imutável para Ações Críticas:** Verifique se operações financeiras, alterações administrativas, exclusão de dados e acessos a PII gravam logs de auditoria contendo: Quem, O quê, Quando, Onde e Por quê.
- [ ] **Proteção de Logs contra Adulteração:** Avalie se logs de auditoria podem ser limpos ou editados por invasores que comprometem a aplicação.

### 4. Information Disclosure (Vazamento de Informações)
- [ ] **Vazamento de Dados em Repouso e em Trânsito:** Avalie a criptografia de campos sensíveis no banco (ex: AES-GCM em números de cartão e documentos), proteção de backups e ausência de dados confidenciais em query strings de URL.
- [ ] **Vazamento por Respostas de Erro e Metadados:** Verifique se mensagens de erro, cabeçalhos de resposta HTTP (`Server`, `X-Powered-By`) ou endpoints de debug expõem topologia interna ou versões de software.

### 5. Denial of Service (Esgotamento de Recursos e DoS)
- [ ] **Esgotamento de Recursos Computacionais:** Identifique endpoints que realizam operações de alto custo (processamento de imagens, parse de XML/Regex complexos - ReDoS, consultas pesadas sem índice) sem limitação de concorrência ou rate limit.
- [ ] **Esgotamento de Conexões e Memória:** Avalie se a aplicação possui proteções contra payloads gigantescos (*Request Body Bombs*) e starvation de conexões de banco de dados.

### 6. Elevation of Privilege (Escalação de Privilégios)
- [ ] **Escalação Horizontal e Vertical:** Avalie a solidez das políticas RBAC/ABAC e Row-Level Security (RLS), identificando brechas que permitam a usuários comuns executar funções de administradores ou acessar tenants vizinhos.
- [ ] **Privilégios de Execução em Ambientes de Nuvem:** Verifique se as permissões de IAM atribuídas aos pods/containers excedem estritamente o necessário para sua operação (*Overprivileged Roles*).

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a modelagem, exiba no chat a lista detalhada de ameaças identificadas, ordenada por risco (DREAD / CVSS):

### PARTE 1: MATRIZ DE AMEAÇAS E QUICK WINS

| ID | Componente / Fronteira | Categoria STRIDE | Risco | Contramedida Principal | Quick Win? |
|---|---|---|---|---|---|
| #1 | `API Gateway -> Auth Service` | Spoofing | CRÍTICO | Validação de Assinatura mTLS | NÃO |
| #2 | `Order Controller` | Tampering | ALTO | Schema Strict & Re-cálculo | **SIM** |

*(Quick Win: Risco ALTO ou MÉDIO com Contramedida de BAIXO esforço).*

### PARTE 2: DETALHAMENTO DAS AMEAÇAS E CONTRAMEDIDAS
Para CADA ameaça mapeada:
- **Ameaça #[ID]:** [Nome do Vetor de Ataque]
- **Categoria STRIDE:** [Spoofing | Tampering | Repudiation | Information Disclosure | DoS | Elevation of Privilege]
- **Fronteira de Confiança Impactada:** [ex: Cliente Web $\rightarrow$ API Pública]
- **Severidade / Risco:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Cenário de Ataque:** Passo a passo de como um invasor explora a brecha.
- **Contramedida Arquitetural Recomendada:** Padrão defensivo para neutralizar a ameaça.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/threat-model/relatorio-threat-modeling.pdf`, contendo:

a) **Capa:** Título "Relatório de Modelagem de Ameaças (Threat Modeling STRIDE) — <nome do projeto>", data, arquitetura avaliada e premissas de segurança.
b) **Resumo Executivo:** Total de ameaças por categoria STRIDE, gráfico de rosca por severidade e gráfico de radar de exposição por superfície de ataque.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Diagrama de Fluxo de Dados (DFD) e Fronteiras de Confiança.**
d) **Tabela Completa de Ameaças e Contramedidas Arquiteturais.**
e) **Seção Final "ISSUES PARA O GITHUB":** Para cada contramedida necessária, a issue pronta para implementação pelo Yellow Team.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`).
- Deixe o script gerador salvo no diretório `docs/threat-model/`.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de ameaças no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/threat-model/relatorio-threat-modeling.pdf`, `docs/threat-model/generate_report.py`).
