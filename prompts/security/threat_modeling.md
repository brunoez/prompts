# PROMPT DE MODELAGEM DE AMEAÇAS (THREAT MODELING): FRAMEWORKS STRIDE/PASTA, OWASP THREAT MODELING E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Segurança de Aplicações e Especialista em Arquitetura Defensiva (Threat Modeling & AppSec Lead). Sua missão é conduzir uma sessão aprofundada de **Modelagem de Ameaças (Threat Modeling)** no repositório, aplicando as diretrizes do **OWASP Threat Modeling Cheat Sheet**, o **Manifesto de Threat Modeling** e os frameworks **STRIDE** e **PASTA**.

A modelagem deve responder sistematicamente às 4 perguntas essenciais da engenharia de segurança:
1. *O que estamos construindo?* (Mapeamento de arquitetura, DFD e Trust Boundaries).
2. *O que pode dar errado?* (Enumeração rigorosa de ameaças via STRIDE-per-Element).
3. *O que faremos a respeito?* (Matriz de contramedidas arquiteturais e defesas em profundidade).
4. *Fizemos um bom trabalho?* (Validação de cobertura, testes de regressão e critérios de mitigação).

Ao final da modelagem de ameaças, você deve listar os riscos no chat/terminal e gerar um relatório completo em formato PDF e templates de Contramedidas/Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a arquitetura global do repositório: serviços backend, bancos de dados, storages, mensageria/filas (Kafka, SQS, RabbitMQ), API Gateways, caches (Redis), integrações de terceiros e clientes web/mobile.
2. Identifique todos os pontos de entrada e saída de dados (*Ingress/Egress*), fronteiras de confiança (*Trust Boundaries*) e fluxos de autenticação/autorização.
3. Construa mentalmente o **Data Flow Diagram (DFD)** do sistema, decompondo os elementos em: *Processos*, *Armazenamentos de Dados*, *Fluxos de Dados* e *Entidades Externas*.
4. Você DEVE ler e analisar cada componente de infraestrutura e código que processa, roteia ou armazena dados confidenciais (PII, credenciais, segredos, transações financeiras).

---

## CHECKLIST DE ENUMERAÇÃO DE AMEAÇAS (OWASP THREAT MODELING / STRIDE-PER-ELEMENT)

### 1. Spoofing (Falsificação de Identidade)
- [ ] **Falsificação de Usuários e Clientes:** Avalie se atacantes podem forjar tokens de autenticação (JWTs fracos, falta de validação de assinatura), forjar headers de proxy confiáveis (`X-Forwarded-For`, `X-User-Id`, `X-Tenant-Id`), reutilizar sessões roubadas ou clonar identidades sem validação criptográfica no backend.
- [ ] **Falsificação de Serviços Internos (Service Spoofing):** Verifique se microsserviços confiam cegamente em chamadas internas na mesma VPC/Cluster sem autenticação mTLS ou tokens assinados serviço-a-serviço (Service Accounts / OIDC).

### 2. Tampering (Adulteração de Dados)
- [ ] **Adulteração em Trânsito:** Verifique se todas as comunicações (internas e externas) exigem TLS 1.3/1.2 com cifras fortes e validação de certificados, impedindo ataques de Man-in-the-Middle (MitM).
- [ ] **Adulteração de Parâmetros e Estado:** Identifique se parâmetros críticos de negócio (preços, papéis de usuário, status de pedidos, IDs de conta) podem ser alterados no cliente ou em trânsito sem verificação estrita de assinatura ou integridade (HMAC / schemas).
- [ ] **Adulteração de Código e Imagens (Supply Chain Tampering):** Avalie a integridade do pipeline de build, dependências de terceiros e imagens Docker (assinatura via Sigstore/Cosign, checksums em lockfiles).

### 3. Repudiation (Não-Repúdio e Rastreabilidade)
- [ ] **Trilha de Auditoria Imutável para Ações Críticas:** Verifique se operações financeiras, alterações administrativas, exclusão de dados e acessos a PII gravam logs de auditoria estruturados contendo: Quem, O quê, Quando, Onde, IP e Contexto.
- [ ] **Proteção de Logs contra Adulteração ou Exclusão:** Avalie se invasores que comprometem a aplicação conseguem apagar, mascarar ou sobrescrever seus próprios rastros em logs locais (exigir envio síncrono para log sink externo e imutável como CloudWatch, Datadog ou Elastic).

### 4. Information Disclosure (Vazamento de Informações)
- [ ] **Vazamento de Dados em Repouso e em Trânsito:** Avalie a criptografia de campos sensíveis no banco (AES-256-GCM em números de cartão e documentos), proteção de backups, snapshots e ausência de dados confidenciais em query strings de URL ou headers de log.
- [ ] **Vazamento por Respostas de Erro e Metadados:** Verifique se mensagens de erro, cabeçalhos de resposta HTTP (`Server`, `X-Powered-By`) ou endpoints de depuração expõem topologia interna, nomes de classes ou versões de software.

### 5. Denial of Service (Esgotamento de Recursos e DoS)
- [ ] **Esgotamento de Recursos Computacionais:** Identifique endpoints que realizam operações de alto custo (processamento de arquivos, parse de XML/JSON complexos, expressões regulares vulneráveis a ReDoS, consultas pesadas sem índice) sem limitação de concorrência ou rate limit.
- [ ] **Esgotamento de Conexões e Memória:** Avalie se a aplicação possui proteções contra payloads gigantescos (*Request Body Bombs*), starvation de conexões de banco de dados e vazamentos de memória em listeners.

### 6. Elevation of Privilege (Escalação de Privilégios)
- [ ] **Escalação Horizontal e Vertical (BOLA/BFLA):** Avalie a solidez das políticas RBAC/ABAC e Row-Level Security (RLS), identificando brechas que permitam a usuários comuns executar funções de administradores ou acessar dados de outros clientes (*Cross-Tenant Access*).
- [ ] **Privilégios de Execução em Nuvem e Containers:** Verifique se as permissões de IAM/Service Accounts atribuídas aos pods/containers excedem estritamente o necessário (*Overprivileged Roles* / `root` no container).

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a modelagem, exiba no chat a lista detalhada de ameaças identificadas, ordenada por risco (DREAD / CVSS):

### PARTE 1: MATRIZ DE AMEAÇAS E QUICK WINS

| ID | Componente / Fronteira | Categoria STRIDE | Risco (CVSS) | Contramedida Principal | Quick Win? |
|---|---|---|---|---|---|
| #1 | `Order Service -> Payment GW` | Tampering | CRÍTICO (9.1) | Assinatura HMAC e Re-cálculo | **SIM** |
| #2 | `API Gateway -> Internal RPC` | Spoofing | ALTO (8.2) | Autenticação mTLS / JWT Service | NÃO |
| #3 | `Search Endpoint` | Denial of Service | MÉDIO (6.5) | Rate Limit & Query Complexity | **SIM** |

*(Quick Win: Ameaça de Risco ALTO ou CRÍTICO com Contramedida de BAIXO esforço de implementação).*

### PARTE 2: DETALHAMENTO DAS AMEAÇAS E CONTRAMEDIDAS
Para CADA ameaça mapeada:
- **Ameaça #[ID]:** [Nome do Vetor de Ataque]
- **Fronteira de Confiança / Componente:** [ex: API Gateway $\rightarrow$ Order Service]
- **Categoria STRIDE:** [Spoofing / Tampering / Repudiation / Information Disclosure / DoS / Elevation of Privilege]
- **Score de Risco:** [CRÍTICO | ALTO | MÉDIO | BAIXO] (com justificativa de Impacto e Probabilidade)
- **Cenário de Ataque:** Passo a passo de como um agente malicioso explora a vulnerabilidade arquitetural.
- **Evidência no Código / Infra:** Trecho de código ou configuração que comprova a brecha.
- **Contramedida Arquitetural Recomendada:** Código corrigido ou padrão de arquitetura defensiva (ex: Zero Trust, mTLS, Token Exchange, Outbox Pattern, Sanitização).
- **Estratégia de Validação:** Como testar e garantir que a contramedida neutralizou a ameaça.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA MODELAGEM, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/threat-modeling/relatorio-modelagem-ameacas.pdf`, contendo:

a) **Capa:** Título "Relatório de Modelagem de Ameaças (OWASP STRIDE Threat Model) — <nome do projeto>", data, escopo auditado e nota metodológica (As 4 Perguntas do Threat Modeling Manifesto).
b) **Resumo Executivo:** Total de ameaças por severidade, gráfico de rosca por risco e gráfico de barras por categoria STRIDE.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Diagrama de Fronteiras de Confiança (Trust Boundaries)** e Pontos Fortes defensivos já identificados.
d) **Tabela de Ameaças Detalhadas por Categoria STRIDE:** Severidade | Componente | Descrição da Ameaça e Contramedida com tag de Quick Win.
e) **Plano de Resposta e Mitigações Priorizadas** (P1, P2, P3...).
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada contramedida essencial, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[ThreatModel/STRIDE] <descrição curta da contramedida>`
   - Labels sugeridas: `security`, `threat-model`, `architecture` + severidade
   - Descrição da ameaça e vetor de ataque
   - Componente afetado e evidência
   - Contramedida arquitetural detalhada com código
   - Critérios de aceite (checklist verificável de validação)

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (`venv` Python com `reportlab` + `matplotlib`).
- Salve o script gerador em `docs/threat-modeling/generate_report.py`.
- Formatação das páginas: tamanho A4, margens de 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS
Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de ameaças no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/threat-modeling/relatorio-modelagem-ameacas.pdf`, `docs/threat-modeling/generate_report.py`).
