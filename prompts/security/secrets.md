# PROMPT DE AUDITORIA COMPLETA: GESTÃO DE SEGREDOS, CONFIGURAÇÕES E SCANNER AUTOMATIZADO COM TRUFFLEHOG3

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em DevSecOps (Yellow Team / Defesa Ativa). Sua missão é realizar uma varredura rigorosa no repositório para identificar vazamento de segredos, chaves de API, credenciais hardcoded, certificados expostos, configurações inseguras de ambiente e histórico git comprometido.

Para complementar e acelerar a auditoria estática manual, você DEVE configurar um ambiente isolado em Python (`venv`), instalar e rodar a ferramenta `trufflehog3`, analisar criticamente o output da ferramenta para filtrar falsos positivos e mocks de testes, e consolidar todos os achados reais no relatório final.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## EXECUÇÃO DO SCANNER AUTOMATIZADO (TRUFFLEHOG3 NO VENV)

Antes de iniciar a leitura detalhada do código, configure o ambiente isolado e execute a ferramenta:

1. Crie o ambiente virtual e instale as dependências necessárias:
   ```bash
   python3 -m venv .audit-venv
   source .audit-venv/bin/activate
   pip install --upgrade pip
   pip install trufflehog3 reportlab matplotlib
```

2. Execute o scan do repositório gerando a saída estruturada:

```bash
# Scan completo no diretório atual ignorando o próprio venv e pastas de build
trufflehog3 -v -f json -o docs/secrets-audit/trufflehog-raw.json --exclude "(\.audit-venv|\.git|node_modules|dist|build|\.venv)" .
```


3. Leia o arquivo `docs/secrets-audit/trufflehog-raw.json` gerado.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA & TRIAGEM

1. Mapeie a estrutura completa de diretórios do projeto e os arquivos de configuração (`.env*`, `.npmrc`, `.pypirc`, `settings.json`, `config/`, `serverless.yml`, etc.).
2. **Triagem Crítica de Falsos Positivos do Trufflehog3:**
* **Mocks e Testes:** Identifique segredos que estão dentro de diretórios `/test`, `/spec`, `__mocks__` ou arquivos de fixture. Marque-os como *Baixa Severidade / Débito Técnico* se forem strings óbvias de teste (ex: `TEST_SECRET_123`), mas alerte caso pareçam chaves reais reaproveitadas.
* **Hashes Públicos e UUIDs:** Ignore hashes de commit, UUIDs, IDs públicos de recursos ou strings randômicas que não representam credenciais funcionais.
* **Chaves Reais em Produção/Config:** Destaque como **CRÍTICA** qualquer chave válida (AWS, GCP, OpenAI, Stripe, JWT Secrets, Private Keys) encontrada em código ou arquivos de configuração versionados.


3. Leia todos os arquivos de configuração, carregamento de variáveis de ambiente e arquivos `.gitignore`. Não faça suposições sem validar o código-fonte correspondente.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (SECRETS & CONFIGS)

### 1. Hardcoded Secrets e Chaves de API

* [ ] **Credenciais de Cloud e Terceiros:** Identifique chaves de API (AWS Access Keys, GCP Service Account JSONs, Stripe, Twilio, SendGrid, OpenAI, etc.) inseridas diretamente no código-fonte.
* [ ] **Chaves Criptográficas e Certificados:** Localize arquivos de chave privada (`.pem`, `.key`, `id_rsa`, `id_ed25519`) ou certificados digitais com chave privada commitados no repositório.
* [ ] **Segredos de Autenticação Interna:** Identifique `JWT_SECRET`, senhas de banco de dados, chaves de sessão ou tokens de webhook gravados como literais estáticos no código.

### 2. Gestão de Variáveis de Ambiente e .gitignore

* [ ] **Exposição de Arquivos .env:** Verifique se arquivos contendo segredos reais (ex: `.env`, `.env.production`, `.env.local`) estão presentes no repositório ou ausentes no arquivo `.gitignore`.
* [ ] **Arquivos .env.example Inseguros:** Verifique se arquivos de exemplo (`.env.example`, `.env.template`) contêm valores de produção reais esquecidos em vez de apenas placeholders explicativos.
* [ ] **Fallbacks Inseguros em Código:** Identifique padrões perigosos de fallback de configuração (ex: `const secret = process.env.API_SECRET || "minha-senha-secreta-padrao"`).

### 3. Integração com Cofres e Injeção de Segredos

* [ ] **Ausência de Secrets Manager:** Identifique aplicações corporativas que realizam gestão manual de segredos em vez de consumir serviços de cofre (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, GCP Secret Manager).
* [ ] **Hardcoded Secrets em Arquivos de CI/CD e Docker:** Verifique se scripts de pipeline (`.github/workflows/`, `.gitlab-ci.yml`) ou `Dockerfiles` utilizam segredos em texto claro via `ARG` ou `ENV` estáticos em vez de GitHub Secrets / OIDC.

### 4. Configurações Inseguras de Ambientes e Debugging

* [ ] **Flags de Debug e Modo de Desenvolvimento em Produção:** Localize variáveis como `DEBUG=True`, `NODE_ENV="development"`, `ENVIRONMENT="dev"` forçadas no código ou sem possibilidade de sobrescrita.
* [ ] **Configurações Default Inseguras:** Identifique se credenciais padrão de fábrica (como `admin/admin`, `root/root`) são mantidas ativas caso as variáveis de ambiente não sejam fornecidas.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica e a triagem do Trufflehog3, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS

Apresente uma tabela inicial contendo TODOS os achados confirmados (reais e débitos de teste), ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? | Origem |
| --- | --- | --- | --- | --- | --- | --- |
| #1 | `src/config/aws.ts:14` | Segredos (AWS Key) | CRÍTICA | Baixo (10 min) | **SIM** | Trufflehog3 + Validação |
| #2 | `config/database.js:8` | Fallback Inseguro | ALTA | Baixo (15 min) | **SIM** | Análise Estática |
| #3 | `tests/mocks/stripe.ts:5` | Segredo em Teste | BAIXA | Baixo (5 min) | NÃO | Falso Positivo / Mock |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS

Para CADA item listado na tabela, forneça a análise completa:

* **Achado #[ID]:** [Nome do Problema]
* **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
* **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
* **Tag:** [QUICK WIN] *(se aplicável)*
* **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
* **Categoria:** [Hardcoded Secrets / .env & Gitignore / Fallback Inseguro / CI/CD & Docker / Config Insegura]
* **Status de Triagem:** [Segredo Real / Falso Positivo Mitigado / Mock de Teste]
* **Problema:** Explicação direta do risco de vazamento ou exploração em produção.
* **Evidência:** Trecho do código-fonte ou linha do segredo (mascarando dados ultra-críticos como `akid...XXXX`).
* **Correção Recomendada:** Código corrigido aplicando injeção de variáveis de ambiente ou integração com cofre de segredos.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/secrets-audit/relatorio-auditoria-segredos.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Gestão de Segredos e Configurações — ", data, escopo auditado e nota metodológica (explicando o uso combinado de análise estática e `trufflehog3`, com detalhes da triagem de falsos positivos).
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria.

* **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (políticas de `.gitignore`, uso de cofres, boas práticas já adotadas) e **Pontos Fracos** (riscos centrais de vazamento de credenciais).
d) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição | Status de Triagem, com indicação/chip de severidade e tag de Quick Win.
e) **Recomendações Priorizadas** (P1, P2, P3...).
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
* Título no formato `[AppSec/Secrets] <descrição curta da falha>`
* Labels sugeridas: `security`, `secrets` ou `configuration` + severidade
* Descrição técnica do problema e por que a chave/configuração precisa ser revogada ou protegida
* Evidência: `arquivo:linha` com trecho de código mascarado
* Impacto (ex: risco de tomada de conta em nuvem, acesso indevido ao banco de dados)
* Sugestão de correção e rotação de credenciais
* Critérios de aceite (checklist verificável de validação)
*(Nota: Agrupe achados triviais relacionados numa issue única quando fizer sentido).*

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF

* Utilize o próprio ambiente isolado `.audit-venv` criado na etapa inicial para rodar o script com `reportlab` e `matplotlib`.
* Deixe o script gerador salvo no diretório `docs/secrets-audit/` para que o relatório possa ser regerado futuramente.
* Verifique o PDF gerado: garanta o número correto de páginas, a renderização adequada dos gráficos e a legibilidade das tabelas.
* Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:

1. A confirmação de execução do `trufflehog3` e geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/secrets-audit/relatorio-auditoria-segredos.pdf`, `docs/secrets-audit/trufflehog-raw.json`, `docs/secrets-audit/generate_report.py`).

