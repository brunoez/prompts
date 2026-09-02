# PROMPT DE AUDITORIA COMPLETA: SEGURANÇA EM CI/CD, PIPELINES (OWASP CI/CD SECURITY) E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de DevSecOps e Especialista em Segurança de Pipelines (CI/CD Security & Pipeline Hardening Lead). Sua missão é realizar uma varredura rigorosa em todas as configurações de **CI/CD e automação** do repositório (GitHub Actions, GitLab CI, CircleCI, Bitbucket Pipelines, Jenkinsfiles, Azure Pipelines), aplicando as diretrizes do **OWASP CI/CD Security Cheat Sheet** e do **OWASP Top 10 CI/CD Security Risks**.

A auditoria deve prevenir injeção de comandos em runners (*Workflow Script Injection*), vazamento de credenciais na esteira, uso de ações/plugins vulneráveis de terceiros (falta de SHA Pinning), abuso de gatilhos em pull requests de forks (`pull_request_target`), permissões excessivas de tokens de CI, ausência de isolamento em runners e ataques de cadeia de suprimentos na entrega contínua.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie todos os arquivos de configuração de automação e esteira:
   - **GitHub Actions:** `.github/workflows/*.yml`, `.github/workflows/*.yaml`, `.github/actions/`.
   - **GitLab CI:** `.gitlab-ci.yml`, arquivos incluídos em `ci/`.
   - **Outros:** `Jenkinsfile`, `.circleci/config.yml`, `bitbucket-pipelines.yml`, `azure-pipelines.yml`.
2. Identifique os gatilhos (*triggers*), matriz de execução, permissões de tokens, segredos referenciados e scripts executados nos jobs.
3. Você DEVE ler e analisar cada workflow linha por linha. Não faça suposições sem validar o código-fonte correspondente.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP CI/CD SECURITY & PIPELINE HARDENING)

### 1. Injeção de Expressões e Comandos (Workflow Script Injection)
- [ ] **Uso Inseguro de Contextos em Scripts Inline:** Identifique o uso direto de variáveis de contexto controladas pelo usuário (ex: `${{ github.event.issue.title }}`, `${{ github.head_ref }}`, `${{ github.event.comment.body }}`, `${{ github.event.pull_request.title }}`) dentro de comandos `run:`, permitindo execução arbitrária de código (`eval/bash injection`).
- [ ] **Uso de Variáveis de Ambiente Intermediárias:** Verifique se os inputs dinâmicos são passados de forma segura como variáveis de ambiente (`env: PR_TITLE: ${{ github.event.issue.title }}`) antes de serem lidos pelo script shell.
- [ ] **Gatilhos Inseguros em PRs de Forks (`pull_request_target`):** Verifique se workflows com `pull_request_target` realizam `checkout` de código de forks não confiáveis com privilégios de gravação ou acesso a segredos do repositório.

### 2. Permissões de Tokens e Princípio do Menor Privilégio (OWASP CI Token Hardening)
- [ ] **Escopo de `GITHUB_TOKEN` / CI Tokens:** Verifique se os workflows definem permissões mínimas explícitas no nível de arquivo ou job (ex: `permissions: contents: read` ou `permissions: {}`), evitando o padrão perigoso de `permissions: write-all` ou permissões implícitas de escrita.
- [ ] **Autenticação OIDC vs Chaves Estáticas de Nuvem:** Verifique se as integrações com AWS, GCP ou Azure utilizam autenticação federada via **OpenID Connect (OIDC)** com assunção de Roles temporárias, em vez de chaves de acesso estáticas de longa duração (`AWS_SECRET_ACCESS_KEY`, `GOOGLE_APPLICATION_CREDENTIALS`) salvas em segredos de CI.

### 3. Imutabilidade e Pinning de Ações de Terceiros (Supply Chain Defense)
- [ ] **Pinning por SHA-256 (Full Commit Hash):** Identifique o uso de Actions de terceiros apontando para tags mutáveis de versão (ex: `uses: actions/checkout@v4` ou `uses: third-party/action@master`) em vez do SHA imutável do commit (`uses: actions/checkout@2541b1294d2704b0964813337f33b291d3f8596b # v4.0.0`), prevenindo ataques de sequestro de repositório de Actions.
- [ ] **Auditoria de Reputação de Ações:** Identifique Actions mantidas por usuários desconhecidos sem verificação oficial da plataforma ou sem histórico confiável.

### 4. Gestão de Segredos, Artefatos e Isolamento de Runners (OWASP Runner Security)
- [ ] **Exposição de Segredos em Logs:** Verifique se comandos de echo, dumps de ambiente (`printenv`, `env`) ou scripts de debug podem imprimir segredos desmascarados nos logs de execução do pipeline.
- [ ] **Runners Auto-Hospedados (Self-Hosted Runners):** Verifique se runners auto-hospedados são utilizados em repositórios públicos sem isolamento efêmero (abertos a execução de código arbitrário por qualquer pull request externo).
- [ ] **Assinatura e Rastreabilidade de Artefatos:** Verifique se imagens Docker e pacotes gerados na esteira são assinados digitalmente com Cosign/Sigstore e contêm atestados de proveniência (SLSA Level 2+).

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `.github/workflows/deploy.yml:15` | Script Injection via Context | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `.github/workflows/ci.yml:3` | Permissão Excessiva (Write-All) | ALTA | Baixo (5 min) | **SIM** |
| #3 | `.github/workflows/release.yml:22` | Falta de SHA Pinning | MÉDIA | Baixo (10 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome da Vulnerabilidade em CI/CD]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/workflow.yml:linha`
- **Categoria:** [Script Injection / Token Permissions / Action Pinning / OIDC Hardening / Log Leakage / Runner Security]
- **Vetor de Exploração:** Explicação direta de como um atacante pode comprometer a esteira, roubar segredos de produção ou injetar código malicioso no build.
- **Evidência:** Trecho do arquivo YAML de workflow.
- **Correção Recomendada:** Código YAML corrigido e seguro.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/cicd-audit/relatorio-auditoria-cicd.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Segurança em CI/CD e Pipelines (OWASP CI/CD Standards) — <nome do projeto>", data, esteiras mapeadas e postura de DevSecOps.
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca de severidade e gráfico de barras por categoria de risco de pipeline.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (uso de OIDC, permissões restritas) e **Pontos Fracos** (injeções potenciais, pinning ausente).
d) **Matriz de Conformidade OWASP CI/CD:** Tabela indicando status para Script Injection, Tokens, Pinning e OIDC.
e) **Tabela de Achados Detalhados:** Severidade | Workflow:Linha | Risco Identificado | Correção.
f) **Diretrizes de Pipeline Hardening para o Time.**
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada workflow inseguro, o template completo de issue com o código corrigido.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (`venv` Python com `reportlab` + `matplotlib`).
- Salve o script gerador em `docs/cicd-audit/generate_report.py`.
- Formatação das páginas: tamanho A4, margens de 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS
Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/cicd-audit/relatorio-auditoria-cicd.pdf`, `docs/cicd-audit/generate_report.py`).
