# PROMPT DE AUDITORIA COMPLETA: IDENTIDADES DIGITAIS, AUTENTICAÇÃO, SESSÃO, MFA & OAUTH2/OIDC (OWASP PROACTIVE CONTROL C7) E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Gestão de Identidades (Identity & Access Management Lead / Yellow Team). Sua missão é realizar uma varredura completa no repositório aplicando o **OWASP Top 10 Proactive Controls 2024 — C7: Secure Digital Identities** e as diretrizes do **OWASP Cheat Sheet Series** (*Authentication, Session Management, JSON Web Token for Java, Forgot Password, Choosing and Using Security Questions, Multifactor Authentication, Credential Stuffing Prevention e Password Storage*), reforçadas pelos testes de código do **OWASP WSTG v4.2** (*WSTG-ATHN, WSTG-SESS, WSTG-IDNT*).

A auditoria deve garantir autenticação robusta, gestão de sessão à prova de fixação e roubo, segundo fator (MFA/2FA) corretamente implementado, fluxos de cadastro/recuperação de conta sem enumeração nem tomada de conta (ATO), e integração segura com provedores de identidade federada (OAuth2 / OpenID Connect / SAML).

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique a stack/tecnologia utilizada (Node.js/Nest/Express/Passport, Python/FastAPI/Django-allauth, Go, Java/Spring Security, Rails/Devise, .NET Identity, etc.) e as bibliotecas de identidade (`passport`, `next-auth`/`Auth.js`, `lucia`, `authlib`, `python-jose`, `pyjwt`, `jsonwebtoken`, `bcrypt`, `argon2`, `otplib`, `speakeasy`, `webauthn`).
2. Identifique e analise TODOS os arquivos dos fluxos de identidade: rotas/handlers de `login`, `logout`, `register`/`signup`, `verify-email`, `forgot-password`, `reset-password`, `change-password`, `refresh-token`, `mfa/enroll`, `mfa/verify`, callbacks OAuth/OIDC (`/auth/callback`), middlewares de sessão/JWT, guards de rota, configuração de cookies e stores de sessão (Redis, DB, JWT stateless).
3. Identifique a configuração de tokens: emissão, algoritmo de assinatura, TTL de access token e refresh token, claims (`iss`, `aud`, `exp`, `sub`, `jti`), rotação e revogação.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.
5. **Diretriz Anti-Fadiga e Anti-Alucinação (Filtro Factual):** Só reporte vulnerabilidades que possam ser categoricamente comprovadas pelo código-fonte ou configurações inspecionadas. É proibido levantar suposições hipotéticas sem evidência no repositório. Recomendações puramente cosméticas ou de estilo sem impacto real de segurança devem ser marcadas como `[NIT]` ou descartadas, mantendo o foco no risco real e no raio de impacto (*Blast Radius*).

---

## CHECKLIST DE AUDITORIA PRÁTICA (OWASP PROACTIVE C7 & CHEAT SHEETS)

### 1. Autenticação e Armazenamento de Credenciais (Authentication + Password Storage Cheat Sheets)
- [ ] **Hashing de Senha Moderno:** Verifique se as senhas são armazenadas com `Argon2id` (preferencial), `scrypt` ou `bcrypt` com fator de custo adequado — nunca `MD5`, `SHA-1`, `SHA-256` puro, hashes sem salt ou salt global/hardcoded.
- [ ] **Comparação em Tempo Constante:** Verifique se a validação de senha, tokens e códigos MFA usa comparação resistente a *timing attacks* (`crypto.timingSafeEqual`, `hmac.compare_digest`) e não `===` / `==`.
- [ ] **Política de Credenciais (NIST 800-63B):** Verifique validação de comprimento mínimo (>= 8, idealmente >= 12), ausência de regras de complexidade contraproducentes que forcem rotação periódica, e checagem da senha contra lista de senhas vazadas (*breached password check* — k-anonymity/HIBP).
- [ ] **Proteção contra Força Bruta e Credential Stuffing:** Verifique rate limiting por conta + por IP, backoff progressivo ou lockout temporário, CAPTCHA/prova de trabalho após N tentativas, e alerta ao usuário em login suspeito/novo dispositivo.
- [ ] **Mensagens e Tempos Homogêneos (Anti-Enumeração — WSTG-IDNT-04):** Verifique se `login`, `forgot-password` e `signup` retornam respostas e tempos de execução idênticos para conta existente vs inexistente (sem `"usuário não encontrado"` vs `"senha inválida"`).

### 2. Gestão de Sessão (Session Management Cheat Sheet — WSTG-SESS)
- [ ] **Regeneração de ID de Sessão no Login (Session Fixation — WSTG-SESS-03):** Verifique se o identificador de sessão é regenerado imediatamente após autenticação bem-sucedida e após elevação de privilégio, invalidando o ID pré-login.
- [ ] **Atributos de Cookie de Sessão:** Verifique `HttpOnly`, `Secure`, `SameSite=Lax` ou `Strict`, `Path` restrito, ausência de `Domain` excessivamente amplo e uso do prefixo `__Host-` quando aplicável.
- [ ] **Expiração e Invalidação:** Verifique *idle timeout* e *absolute timeout* server-side, invalidação real da sessão no logout (destruição no store, não apenas remoção do cookie no cliente) e invalidação de todas as sessões após troca/reset de senha.
- [ ] **Fixação via Query/Header:** Verifique que o ID de sessão nunca trafega em URL, query string ou é aceito via parâmetro controlável pelo cliente.

### 3. Tokens JWT e Federação OAuth2 / OpenID Connect (JWT + OAuth Cheat Sheets)
- [ ] **Validação de Assinatura e Algoritmo:** Verifique rejeição explícita de `alg: none`, *allow-list* de algoritmos (ex: só `RS256`/`EdDSA`), impossibilidade de confusão de algoritmo (`HS256` verificado com chave pública RSA) e validação de `kid` contra JWKS confiável.
- [ ] **Validação de Claims:** Verifique validação estrita de `exp`, `nbf`, `iss`, `aud` e binding do token ao usuário/tenant. Access tokens com TTL curto (minutos) e refresh tokens com rotação + detecção de reuso (*refresh token replay*).
- [ ] **Revogação:** Verifique existência de blacklist/denylist por `jti` ou versionamento de credencial (`token_version`) para invalidar tokens antes do `exp` (logout, ban, troca de senha).
- [ ] **Fluxo OAuth2/OIDC Correto:** Verifique uso de **Authorization Code + PKCE** (nunca Implicit Flow), validação obrigatória do parâmetro `state` (anti-CSRF) e `nonce` (anti-replay), *allow-list* estrita de `redirect_uri` (sem match por prefixo/wildcard) e validação do `id_token` (assinatura, `aud`, `iss`, `nonce`).
- [ ] **Armazenamento de Token no Cliente:** Verifique que tokens de sessão não são gravados em `localStorage`/`sessionStorage` (expostos a XSS); preferência por cookie `HttpOnly` + padrão BFF (*Backend-for-Frontend*).

### 4. MFA / 2FA (Multifactor Authentication Cheat Sheet)
- [ ] **Enrollment e Verificação:** Verifique que o segredo TOTP é gerado com CSPRNG, transmitido uma única vez, e que a verificação valida janela de tempo estreita e impede reuso do mesmo código (*OTP replay*).
- [ ] **Códigos de Recuperação:** Verifique que *backup codes* são de uso único, hasheados no banco e regeneráveis.
- [ ] **Anti-Bypass:** Verifique que rotas protegidas por MFA não são acessíveis com sessão "pré-MFA" (estado intermediário), que "lembrar deste dispositivo" usa token assinado e expirável, e que o fluxo de reset de senha não pula o segundo fator.
- [ ] **WebAuthn/Passkeys (se presente):** Verifique validação de `challenge`, `origin`, `rpId` e contador de assinatura (*signature counter*) contra clonagem de autenticador.

### 5. Cadastro, Verificação e Recuperação de Conta (Forgot Password Cheat Sheet)
- [ ] **Token de Reset Seguro:** Verifique que o token de recuperação/verificação é gerado com CSPRNG (>= 128 bits), armazenado **hasheado** no banco, tem TTL curto (ex: 15–60 min), é de uso único e é invalidado após uso ou nova solicitação.
- [ ] **Sem Vazamento de Token:** Verifique que o token não aparece em logs, no `Referer` (link para domínio externo na página de reset) nem em histórico de e-mail encaminhável sem expiração.
- [ ] **Perguntas de Segurança:** Se existirem, verifique que não são usadas como único fator de recuperação (Cheat Sheet desaconselha) e que respostas são hasheadas.
- [ ] **Confirmação e Notificação:** Verifique envio de e-mail de notificação em toda troca de senha, e-mail ou fator MFA, e exigência de senha atual para mudanças sensíveis (*re-authentication*).
- [ ] **Account Takeover via E-mail Change:** Verifique que a troca de e-mail exige confirmação no endereço antigo **e** no novo, e não transfere sessões/privilégios antes da confirmação.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica, exiba no chat a lista detalhada de achados ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados:

| ID | Arquivo / Ponto | Módulo / Padrão | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/auth/login.ts:44` | Session Fixation (sem regeneração) | CRÍTICA | Baixo (20 min) | **SIM** |
| #2 | `src/auth/jwt.ts:12` | JWT aceita `alg: none` | CRÍTICA | Baixo (30 min) | **SIM** |
| #3 | `src/auth/reset.ts:70` | Token de reset em texto claro no DB | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item da tabela:
- **Achado #[ID]:** [Nome do Problema]
- **Controle / Cheat Sheet:** [ex: Proactive C7 / Session Management Cheat Sheet / WSTG-SESS-03]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Vetor de Ataque / Exploração:** Como um atacante explora a falha (ex: reuso de session ID, forjar JWT, enumerar contas, replay de OTP).
- **Evidência:** Trecho do código-fonte vulnerável.
- **Prova de Conceito (PoC / Reprodução):** Requisição reproduzível (`curl` / script) demonstrando a falha no contexto do projeto.
- **Correção Recomendada:** Código refatorado e seguro.
- **Comando de Verificação da Correção:** Como o desenvolvedor valida em 1 comando (teste automatizado) que a correção funcionou sem quebrar o fluxo de login.

---

## GERAÇÃO DE RELATÓRIO PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script automatizado salvo em `docs/authn-audit/generate_report.py` para produzir:

1. **Relatório em PDF (`docs/authn-audit/relatorio-auditoria-identidade.pdf`):**
   - **Capa:** Título "Relatório de Auditoria de Identidades Digitais & Autenticação (OWASP Proactive C7) — <nome do projeto>", data e escopo.
   - **Resumo Executivo:** Gráfico de rosca por severidade e gráfico de barras por categoria (Autenticação, Sessão, JWT/OAuth, MFA, Recuperação).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
   - **Matriz de Conformidade C7 & Cheat Sheets:** Tabela com status por item do checklist.
   - **Tabela Detalhada de Achados** com tags de Quick Win e referências a arquivos e linhas.

2. **Seção "ISSUES PARA O GITHUB" no Relatório:**
   - Template Markdown completo pronto para copiar e colar para cada achado, com labels, passos de reprodução, impacto e critérios de aceite.

### REGRAS TÉCNICAS
- Use ambiente Python isolado (`venv` temporário com `reportlab` e `matplotlib`).
- Salve o script e os artefatos em `docs/authn-audit/`.
- Garanta formatação A4 impecável, paginação correta e sem quebras visuais em tabelas.

---

## ENTREGÁVEIS FINAIS
Ao concluir, informe no chat:
1. A confirmação da geração do relatório PDF.
2. A lista de achados (Parte 1 e Parte 2).
3. O caminho relativo dos arquivos gerados (`docs/authn-audit/relatorio-auditoria-identidade.pdf`, `docs/authn-audit/generate_report.py`).
