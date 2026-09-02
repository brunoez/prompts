# PROMPT DE AUDITORIA COMPLETA: GESTÃO DE SEGREDOS, ARMAZENAMENTO DE SENHAS (OWASP PASSWORD STORAGE), CRIPTOGRAFIA E SCANNER AUTOMATIZADO

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Criptografia Aplicada (Yellow Team / Defesa Ativa). Sua missão é realizar uma varredura rigorosa no repositório aplicando as diretrizes do **OWASP Cheat Sheet Series** (*Secrets Management, Password Storage, Cryptographic Storage, Key Management e Credential Stuffing Prevention*).

O foco é identificar vazamento de segredos, credenciais hardcoded, configurações inseguras de ambiente, vulnerabilidades em algoritmos de hashing de senhas, ataques de tempo (*timing attacks*), certificados expostos e histórico git comprometido.

Para complementar a auditoria estática manual, você DEVE configurar um ambiente isolado em Python (`venv`), instalar e rodar a ferramenta `trufflehog3`, analisar criticamente o output para filtrar falsos positivos e mocks de testes, e consolidar todos os achados reais no relatório final.

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

3. Leia o arquivo `docs/secrets-audit/trufflehog-raw.json` gerado para realizar a triagem.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA & TRIAGEM

1. Mapeie a estrutura completa de diretórios do projeto e os arquivos de configuração (`.env*`, `.npmrc`, `.pypirc`, `settings.json`, `config/`, `serverless.yml`, workflows de CI/CD, Dockerfiles, etc.).
2. **Triagem Crítica de Falsos Positivos do Trufflehog3:**
   - **Mocks e Testes:** Identifique segredos em `/test`, `/spec`, `__mocks__` ou fixtures. Marque-os como *Baixa Severidade / Débito Técnico* se forem strings óbvias de teste (ex: `TEST_SECRET_123`), mas alerte caso pareçam chaves reais reaproveitadas.
   - **Hashes Públicos e UUIDs:** Ignore hashes de commit, UUIDs, IDs públicos de recursos ou strings randômicas que não representam credenciais funcionais.
   - **Chaves Reais em Produção/Config:** Destaque como **CRÍTICA** qualquer chave válida (AWS, GCP, OpenAI, Stripe, JWT Secrets, Private Keys) encontrada em código ou arquivos de configuração versionados.
3. Leia todos os arquivos de autenticação, hashing de senhas, criptografia, carregamento de variáveis de ambiente e arquivos `.gitignore`.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP SECRETS & CRYPTO STANDARDS)

### 1. Hardcoded Secrets e Chaves de API (OWASP Secrets Management)
- [ ] **Credenciais de Provedores de Nuvem e Terceiros:** Identifique chaves de API (AWS Access Keys, GCP Service Account JSONs, Azure Connection Strings, Stripe, Twilio, SendGrid, OpenAI, etc.) inseridas diretamente no código-fonte.
- [ ] **Chaves Criptográficas Privadas e Certificados:** Localize arquivos de chave privada (`.pem`, `.key`, `id_rsa`, `id_ed25519`) ou certificados digitais com chave privada commitados no repositório.
- [ ] **Segredos de Autenticação Interna e JWT:** Identifique `JWT_SECRET`, senhas de banco de dados, chaves de sessão ou segredos de webhook gravados como literais estáticos no código.
- [ ] **Fallbacks Inseguros em Código:** Identifique padrões perigosos de fallback de configuração (ex: `const secret = process.env.API_SECRET || "minha-senha-secreta-padrao"`).

### 2. Padrões de Hashing de Senhas (OWASP Password Storage Cheat Sheet)
- [ ] **Conformidade de Algoritmo de Hashing:** Verifique qual algoritmo é utilizado para persistir senhas:
  - **Padrão Ouro Recomendado:** `Argon2id` (mínimo: $64\,\text{MB}$ de memória, $3$ iterações, $4$ threads de paralelismo).
  - **Alternativas Seguras:** `scrypt`, `bcrypt` (com fator de custo $\ge 12$) ou `PBKDF2` (com HMAC-SHA256 $\ge 600.000$ iterações).
  - **Vulnerabilidades Críticas (Banidos):** Uso de `MD5`, `SHA-1`, `SHA-256/512` simples/sem KDF, ou `bcrypt` com custo fraco ($< 10$).
- [ ] **Arquitetura de Salt & Pepper:** Verifique se o hash utiliza um Salt criptograficamente seguro (CSPRNG) único por usuário e se há suporte a Pepper global gerenciado em cofre seguro (HSM / KMS) fora do banco de dados.
- [ ] **Resistência a Timing Attacks na Autenticação:** Verifique se a comparação de hashes de senha, tokens de verificação e assinaturas HMAC utiliza funções de tempo constante (ex: `crypto.timingSafeEqual()`, `hmac.compare_digest()`, `MessageDigest.isEqual()`) para impedir ataques de temporização (*side-channel timing attacks*).

### 3. Gestão de Variáveis de Ambiente, .gitignore e Cofres
- [ ] **Exposição de Arquivos .env:** Verifique se arquivos contendo segredos reais (ex: `.env`, `.env.production`, `.env.local`) estão presentes no repositório ou ausentes no arquivo `.gitignore`.
- [ ] **Arquivos .env.example Inseguros:** Verifique se arquivos de exemplo (`.env.example`, `.env.template`) contêm valores de produção reais esquecidos em vez de apenas placeholders explicativos.
- [ ] **Integração com Secrets Managers:** Identifique aplicações corporativas que realizam gestão manual de segredos em vez de consumir serviços de cofre gerenciados (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, GCP Secret Manager).
- [ ] **Hardcoded Secrets em CI/CD e Docker:** Verifique se scripts de pipeline (`.github/workflows/`, `.gitlab-ci.yml`) ou `Dockerfiles` utilizam segredos em texto claro via `ARG` ou `ENV` estáticos em vez de GitHub Secrets / OIDC.

### 4. Ciclo de Vida de Chaves e Higiene de Memória (Key Management & Zeroization)
- [ ] **Rotação de Chaves sem Downtime:** Avalie se a aplicação suporta rotação de chaves e segredos (ex: múltiplos segredos aceitos durante período de transição / *dual-key grace period*).
- [ ] **Limpeza de Segredos da Memória (Zeroization):** Em linguagens com gerenciamento de memória (Go, Rust, C, Java com `char[]`), verifique se buffers de senhas e chaves privadas são sobrescritos com zeros após o uso (`secure_zero`), evitando que permaneçam em dumps de memória/heap.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica e a triagem do Trufflehog3, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados confirmados:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? | Origem |
|---|---|---|---|---|---|---|
| #1 | `src/config/aws.ts:14` | OWASP Secrets (AWS Key) | CRÍTICA | Baixo (10 min) | **SIM** | Trufflehog3 + Validação |
| #2 | `src/auth/hash.ts:25` | OWASP Password Storage (SHA-256) | CRÍTICA | Baixo (30 min) | **SIM** | Análise Estática |
| #3 | `src/auth/token.ts:50` | Crypto (Timing Attack) | MÉDIA | Baixo (15 min) | **SIM** | Análise Estática |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [OWASP Secrets / Password Storage / Cryptographic Storage / Key Management / Timing Attacks]
- **Status de Triagem:** [Segredo Real / Falso Positivo Mitigado / Débito de Teste / Algoritmo Fraco]
- **Problema & Vetor de Exploração:** Explicação direta do risco de vazamento, quebra de hash por força bruta ou exploração em produção.
- **Evidência:** Trecho do código-fonte ou linha do segredo (mascarando dados ultra-críticos como `akid...XXXX`).
- **Correção Recomendada:** Código corrigido aplicando injeção de variáveis de ambiente, Argon2id ou funções em tempo constante.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/secrets-audit/relatorio-auditoria-segredos.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Gestão de Segredos e Criptografia (OWASP Standards) — <nome do projeto>", data, escopo auditado e nota metodológica (explicando o uso combinado de análise estática e `trufflehog3`).
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria OWASP.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (políticas de `.gitignore`, uso de cofres, boas práticas criptográficas já adotadas) e **Pontos Fracos** (riscos centrais).
d) **Matriz de Conformidade OWASP Secrets & Password Storage:** Tabela de conformidade com os requisitos de hashing, encriptação e cofre.
e) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição | Status de Triagem, com indicação/chip de severidade e tag de Quick Win.
f) **Recomendações Priorizadas** (P1, P2, P3...).
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[AppSec/Secrets] <descrição curta da falha>`
   - Labels sugeridas: `security`, `secrets`, `cryptography` + severidade
   - Descrição técnica do problema e passos de mitigação/rotação
   - Evidência: `arquivo:linha` com trecho mascarado
   - Impacto e risco
   - Sugestão de correção com código seguro
   - Critérios de aceite (checklist verificável)

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Utilize o próprio ambiente isolado `.audit-venv` criado na etapa inicial para rodar o script com `reportlab` e `matplotlib`.
- Salve o script gerador em `docs/secrets-audit/generate_report.py`.
- Formatação das páginas: tamanho A4, margens de 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS
Ao concluir todas as etapas, informe no chat:
1. A confirmação de execução do `trufflehog3` e geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (`docs/secrets-audit/relatorio-auditoria-segredos.pdf`, `docs/secrets-audit/trufflehog-raw.json`, `docs/secrets-audit/generate_report.py`).
