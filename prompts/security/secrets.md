# PROMPT DE AUDITORIA COMPLETA: GESTÃO DE SEGREDOS, ARMAZENAMENTO DE SENHAS (OWASP PASSWORD STORAGE & WSTG), CRIPTOGRAFIA, OWASP ASVS v4.0.3, OWASP RISK RATING METHODOLOGY E SCANNER AUTOMATIZADO

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Criptografia Aplicada (Yellow Team / Defesa Ativa). Sua missão é realizar uma varredura rigorosa no repositório aplicando as diretrizes do **OWASP Cheat Sheet Series** (*Secrets Management, Password Storage, Cryptographic Storage, Key Management e Credential Stuffing Prevention*), os testes essenciais do **OWASP WSTG v4.2** (*WSTG-SESS e WSTG-IDNT*) e os requisitos normativos do **OWASP Application Security Verification Standard (OWASP ASVS v4.0.3)** (Capítulo V6 - Stored Cryptography, Capítulo V8 - Data Protection e Capítulo V14 - Configuration Verification Requirements).

A severidade de cada vulnerabilidade identificada deve ser formalmente mensurada aplicando o **OWASP Risk Rating Methodology**, combinando a Probabilidade (*Likelihood*) com o Impacto (*Impact*) em uma matriz determinística 3x3.

O foco é identificar vazamento de segredos, credenciais hardcoded, configurações inseguras de ambiente, vulnerabilidades em algoritmos de hashing de senhas, falhas de regeneração de sessão (*Session Fixation*), enumeração de contas (*Account Harvesting*), ataques de tempo (*timing attacks*), certificados expostos e histórico git comprometido.

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
3. Leia todos os arquivos de autenticação, hashing de senhas, gerenciamento de sessões, criptografia, carregamento de variáveis de ambiente e arquivos `.gitignore`.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP SECRETS, CRYPTO, WSTG & OWASP ASVS v4.0.3)

### 1. Hardcoded Secrets e Chaves de API (OWASP Secrets Management & ASVS V14.1, V6.4)
- [ ] **Credenciais de Provedores de Nuvem e Terceiros & ASVS V14.1.1, V6.4.1 (L1):** Identifique chaves de API (AWS Access Keys, GCP Service Account JSONs, Azure Connection Strings, Stripe, Twilio, SendGrid, OpenAI, etc.) inseridas diretamente no código-fonte.
- [ ] **Chaves Criptográficas Privadas e Certificados & ASVS V6.4.2 (L1):** Localize arquivos de chave privada (`.pem`, `.key`, `id_rsa`, `id_ed25519`) ou certificados digitais com chave privada commitados no repositório.
- [ ] **Segredos de Autenticação Interna e JWT & ASVS V14.1.2 (L1):** Identifique `JWT_SECRET`, senhas de banco de dados, chaves de sessão ou segredos de webhook gravados como literais estáticos no código.
- [ ] **Fallbacks Inseguros em Código & ASVS V14.1.3 (L1):** Identifique padrões perigosos de fallback de configuração (ex: `const secret = process.env.API_SECRET || "minha-senha-secreta-padrao"`).

### 2. Padrões de Hashing de Senhas e Autenticação (OWASP Password Storage & ASVS V2.4, V6.2)
- [ ] **Conformidade de Algoritmo de Hashing & ASVS V2.4.1, V2.4.2 (L2):** Verifique qual algoritmo é utilizado para persistir senhas:
  - **Padrão Ouro Recomendado:** `Argon2id` (mínimo: $64\,\text{MB}$ de memória, $3$ iterações, $4$ threads de paralelismo).
  - **Alternativas Seguras:** `scrypt`, `bcrypt` (com fator de custo $\ge 12$) ou `PBKDF2` (com HMAC-SHA256 $\ge 600.000$ iterações).
  - **Vulnerabilidades Críticas (Banidos):** Uso de `MD5`, `SHA-1`, `SHA-256/512` simples/sem KDF, ou `bcrypt` com custo fraco ($< 10$).
- [ ] **Arquitetura de Salt & Pepper & ASVS V2.4.3, V6.2.2 (L2):** Verifique se o hash utiliza um Salt criptograficamente seguro (CSPRNG) único por usuário e se há suporte a Pepper global gerenciado em cofre seguro (HSM / KMS) fora do banco de dados.
- [ ] **Resistência a Timing Attacks na Autenticação & ASVS V2.1.12, V6.2.8 (L2):** Verifique se a comparação de hashes de senha, tokens de verificação e assinaturas HMAC utiliza funções de tempo constante (ex: `crypto.timingSafeEqual()`, `hmac.compare_digest()`, `MessageDigest.isEqual()`) para impedir ataques de temporização (*side-channel timing attacks*).
- [ ] **Fixação de Sessão & Enumeração de Usuários (WSTG-SESS-03 / IDNT-04 & ASVS V3.3.1, V2.1.7 - L2):** Verifique se o Session ID é regenerado obrigatoriamente após a autenticação bem-sucedida e se mensagens e tempos de resposta em login e redefinição de senha são homogêneos, impedindo enumeração de e-mails/usuários.

### 3. Gestão de Variáveis de Ambiente, .gitignore e Cofres (ASVS V14.1, V14.3)
- [ ] **Exposição de Arquivos .env & ASVS V14.1.1 (L1):** Verifique se arquivos contendo segredos reais (ex: `.env`, `.env.production`, `.env.local`) estão presentes no repositório ou ausentes no arquivo `.gitignore`.
- [ ] **Arquivos .env.example Inseguros & ASVS V14.1.2 (L1):** Verifique se arquivos de exemplo (`.env.example`, `.env.template`) contêm valores de produção reais esquecidos em vez de apenas placeholders explicativos.
- [ ] **Integração com Secrets Managers & ASVS V6.4.1, V14.3.1 (L2):** Identifique aplicações corporativas que realizam gestão manual de segredos em vez de consumir serviços de cofre gerenciados (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, GCP Secret Manager).
- [ ] **Hardcoded Secrets em CI/CD e Docker & ASVS V14.1.1, V14.2.1 (L1):** Verifique se scripts de pipeline (`.github/workflows/`, `.gitlab-ci.yml`) ou `Dockerfiles` utilizam segredos em texto claro via `ARG` ou `ENV` estáticos em vez de GitHub Secrets / OIDC.

### 4. Ciclo de Vida de Chaves e Higiene de Memória (Key Management & ASVS V6.3, V6.4)
- [ ] **Rotação de Chaves sem Downtime & ASVS V6.3.1, V6.4.3 (L2):** Avalie se a aplicação suporta rotação de chaves e segredos (ex: múltiplos segredos aceitos durante período de transição / *dual-key grace period*).
- [ ] **Limpeza de Segredos da Memória (Zeroization) & ASVS V6.4.4 (L3):** Em linguagens com gerenciamento de memória (Go, Rust, C, Java com `char[]`), verifique se buffers de senhas e chaves privadas são sobrescritos com zeros após o uso (`secure_zero`), evitando que permaneçam em dumps de memória/heap.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica e a triagem do Trufflehog3, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados confirmados, avaliados segundo o **OWASP Risk Rating Methodology**:

$$\text{Risco (Severidade)} = \text{Probabilidade (Likelihood)} \times \text{Impacto (Impact)}$$

*Critério da Matriz 3x3 OWASP:*
- **Alta Probabilidade × Alto Impacto** = **CRÍTICA**
- **Alta × Médio** ou **Média × Alto** = **ALTA**
- **Alta × Baixo**, **Média × Médio** ou **Baixa × Alto** = **MÉDIA**
- **Média × Baixo**, **Baixa × Médio** ou **Baixa × Baixo** = **BAIXA**

| ID | Arquivo / Ponto | Categoria / ASVS | Probabilidade | Impacto | Severidade (RRM) | Esforço Estimado | Quick Win? | Origem |
|---|---|---|---|---|---|---|---|---|
| #1 | `src/config/aws.ts:14` | AWS Key / ASVS V14.1.1 (L1) | ALTA | ALTO | CRÍTICA | Baixo (10 min) | **SIM** | Trufflehog3 + Validação |
| #2 | `src/auth/hash.ts:25` | SHA-256 / ASVS V2.4.1 (L2) | ALTA | ALTO | CRÍTICA | Baixo (30 min) | **SIM** | Análise Estática |
| #3 | `src/auth/session.ts:18` | Session Fixation / ASVS V3.3.1 (L2) | ALTA | MÉDIO | ALTA | Baixo (15 min) | **SIM** | Análise Estática |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Categoria / Padrão:** [OWASP Secrets / Password Storage / Cryptographic Storage / Session Fixation / Timing Attacks]
- **OWASP ASVS v4.0.3:** [Capítulo e Requisito, ex: V14.1.1 (Level 1 - Hardcoded Secrets)]
- **Avaliação de Risco (OWASP Risk Rating Methodology):**
  - *Probabilidade (Likelihood):* [BAIXA | MÉDIA | ALTA] (Agente de Ameaça + Facilidade de Descoberta/Exploração)
  - *Impacto Técnico (Tech Impact):* [BAIXO | MÉDIO | ALTO] (Confidencialidade, Integridade, Disponibilidade)
  - *Impacto de Negócio (Business Impact):* [BAIXO | MÉDIO | ALTO] (Danos Financeiros, LGPD/GDPR, Reputação)
  - *Severidade Calculada:* [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Status de Triagem:** [Segredo Real / Falso Positivo Mitigado / Débito de Teste / Algoritmo Fraco]
- **Problema & Vetor de Exploração:** Explicação direta do risco de vazamento, quebra de hash por força bruta ou exploração em produção.
- **Evidência:** Trecho do código-fonte ou linha do segredo (mascarando dados ultra-críticos como `akid...XXXX`).
- **Correção Recomendada:** Código corrigido aplicando injeção de variáveis de ambiente, Argon2id ou funções em tempo constante.
- **Comando de Verificação da Correção:** Como o desenvolvedor valida em 1 comando (teste automatizado) que a correção funcionou sem quebrar o acesso a serviços.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/secrets-audit/relatorio-auditoria-segredos.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Gestão de Segredos, Criptografia & ASVS (OWASP & WSTG) — <nome do projeto>", data, escopo auditado e nota metodológica (explicando o uso combinado de análise estática e `trufflehog3`).
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade, gráfico de barras por categoria OWASP e Matriz de Calor 3x3 do OWASP Risk Rating Methodology (Likelihood × Impact).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (políticas de `.gitignore`, uso de cofres, boas práticas criptográficas já adotadas) e **Pontos Fracos** (riscos centrais).
d) **Matriz de Conformidade OWASP Secrets, Password Storage & ASVS:** Tabela de conformidade com os requisitos de hashing, encriptação, cofre e conformidade ASVS V6, V8 e V14 (L1/L2/L3).
e) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição | Status de Triagem, com indicação/chip de severidade, nota RRM e tag de Quick Win.
f) **Recomendações Priorizadas** (P1, P2, P3...).
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[AppSec/Secrets] <descrição curta da falha>`
   - Labels sugeridas: `security`, `secrets`, `cryptography` + severidade
   - Descrição técnica do problema, passos de mitigação/rotação e avaliação formal de risco (RRM: Probabilidade x Impacto)
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
