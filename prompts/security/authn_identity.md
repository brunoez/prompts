# PROMPT DE AUDITORIA COMPLETA: IDENTIDADES DIGITAIS, AUTENTICAÇÃO, SESSÃO, MFA & OAUTH2/OIDC (OWASP PROACTIVE CONTROL C7, OWASP ASVS v4.0.3 & OWASP RISK RATING METHODOLOGY) E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Gestão de Identidades (Identity & Access Management Lead / Yellow Team). Sua missão é realizar uma varredura completa no repositório aplicando o **OWASP Top 10 Proactive Controls 2024 — C7: Secure Digital Identities**, as diretrizes do **OWASP Cheat Sheet Series** (*Authentication, Session Management, JSON Web Token for Java, Forgot Password, Choosing and Using Security Questions, Multifactor Authentication, Credential Stuffing Prevention e Password Storage*), os testes essenciais do **OWASP WSTG v4.2** (*WSTG-ATHN, WSTG-SESS, WSTG-IDNT*) e os requisitos normativos do **OWASP Application Security Verification Standard (OWASP ASVS v4.0.3)** (Capítulo V2 - Authentication e Capítulo V3 - Session Management Verification Requirements).

A severidade de cada vulnerabilidade identificada deve ser formalmente mensurada aplicando o **OWASP Risk Rating Methodology**, combinando a Probabilidade (*Likelihood*) com o Impacto (*Impact*) em uma matriz determinística 3x3.

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

## CHECKLIST DE AUDITORIA PRÁTICA (OWASP PROACTIVE C7, CHEAT SHEETS & OWASP ASVS v4.0.3)

### 1. Autenticação e Armazenamento de Credenciais (Authentication + Password Storage Cheat Sheets & ASVS V2)
- [ ] **Hashing de Senha Moderno & ASVS V2.4.1, V2.4.2 (L2):** Verifique se as senhas são armazenadas com `Argon2id` (preferencial), `scrypt` ou `bcrypt` com fator de custo adequado — nunca `MD5`, `SHA-1`, `SHA-256` puro, hashes sem salt ou salt global/hardcoded.
- [ ] **Comparação em Tempo Constante & ASVS V2.1.12 (L2):** Verifique se a validação de senha, tokens e códigos MFA usa comparação resistente a *timing attacks* (`crypto.timingSafeEqual`, `hmac.compare_digest`) e não `===` / `==`.
- [ ] **Política de Credenciais (NIST 800-63B & ASVS V2.1.1, V2.1.2 - L2):** Verifique validação de comprimento mínimo (>= 8, idealmente >= 12), ausência de regras de complexidade contraproducentes que forcem rotação periódica, e checagem da senha contra lista de senhas vazadas (*breached password check* — k-anonymity/HIBP).
- [ ] **Proteção contra Força Bruta e Credential Stuffing & ASVS V2.2.1, V2.2.2 (L2):** Verifique rate limiting por conta + por IP, backoff progressivo ou lockout temporário, CAPTCHA/prova de trabalho após N tentativas, e alerta ao usuário em login suspeito/novo dispositivo.
- [ ] **Mensagens e Tempos Homogêneos (Anti-Enumeração — WSTG-IDNT-04 & ASVS V2.1.7 - L2):** Verifique se `login`, `forgot-password` e `signup` retornam respostas e tempos de execução idênticos para conta existente vs inexistente (sem `"usuário não encontrado"` vs `"senha inválida"`).

### 2. Gestão de Sessão (Session Management Cheat Sheet — WSTG-SESS & ASVS V3)
- [ ] **Regeneração de ID de Sessão no Login (Session Fixation — WSTG-SESS-03 & ASVS V3.3.1 - L2):** Verifique se o identificador de sessão é regenerado imediatamente após autenticação bem-sucedida e após elevação de privilégio, invalidando o ID pré-login.
- [ ] **Atributos de Cookie de Sessão & ASVS V3.4.1, V3.4.2, V3.4.3 (L2):** Verifique `HttpOnly`, `Secure`, `SameSite=Lax` ou `Strict`, `Path` restrito, ausência de `Domain` excessivamente amplo e uso do prefixo `__Host-` quando aplicável.
- [ ] **Expiração e Invalidação & ASVS V3.2.1, V3.3.2 (L2):** Verifique *idle timeout* e *absolute timeout* server-side, invalidação real da sessão no logout (destruição no store, não apenas remoção do cookie no cliente) e invalidação de todas as sessões após troca/reset de senha.
- [ ] **Fixação via Query/Header & ASVS V3.1.1 (L2):** Verifique que o ID de sessão nunca trafega em URL, query string ou é aceito via parâmetro controlável pelo cliente.

### 3. Tokens JWT e Federação OAuth2 / OpenID Connect (JWT + OAuth Cheat Sheets & ASVS V3.5, V3.6)
- [ ] **Validação de Assinatura e Algoritmo & ASVS V3.5.2, V3.5.3 (L2):** Verifique rejeição explícita de `alg: none`, *allow-list* de algoritmos (ex: só `RS256`/`EdDSA`), impossibilidade de confusão de algoritmo (`HS256` verificado com chave pública RSA) e validação de `kid` contra JWKS confiável.
- [ ] **Validação de Claims & ASVS V3.5.1, V3.6.1 (L2):** Verifique validação estrita de `exp`, `nbf`, `iss`, `aud` e binding do token ao usuário/tenant. Access tokens com TTL curto (minutos) e refresh tokens com rotação + detecção de reuso (*refresh token replay*).
- [ ] **Revogação & ASVS V3.5.4 (L2):** Verifique existência de blacklist/denylist por `jti` ou versionamento de credencial (`token_version`) para invalidar tokens antes do `exp` (logout, ban, troca de senha).
- [ ] **Fluxo OAuth2/OIDC Correto & ASVS V3.6.2, V3.6.3 (L2):** Verifique uso de **Authorization Code + PKCE** (nunca Implicit Flow), validação obrigatória do parâmetro `state` (anti-CSRF) e `nonce` (anti-replay), *allow-list* estrita de `redirect_uri` (sem match por prefixo/wildcard) e validação do `id_token` (assinatura, `aud`, `iss`, `nonce`).
- [ ] **Armazenamento de Token no Cliente & ASVS V3.5.5 (L2):** Verifique que tokens de sessão não são gravados em `localStorage`/`sessionStorage` (expostos a XSS); preferência por cookie `HttpOnly` + padrão BFF (*Backend-for-Frontend*).

### 4. MFA / 2FA (Multifactor Authentication Cheat Sheet & ASVS V2.8)
- [ ] **Enrollment e Verificação & ASVS V2.8.1, V2.8.2 (L2):** Verifique que o segredo TOTP é gerado com CSPRNG, transmitido uma única vez, e que a verificação valida janela de tempo estreita e impede reuso do mesmo código (*OTP replay*).
- [ ] **Códigos de Recuperação & ASVS V2.8.4 (L2):** Verifique que *backup codes* são de uso único, hasheados no banco e regeneráveis.
- [ ] **Anti-Bypass & ASVS V2.8.5 (L2):** Verifique que rotas protegidas por MFA não são acessíveis com sessão "pré-MFA" (estado intermediário), que "lembrar deste dispositivo" usa token assinado e expirável, e que o fluxo de reset de senha não pula o segundo fator.
- [ ] **WebAuthn/Passkeys (se presente) & ASVS V2.8.7 (L2):** Verifique validação de `challenge`, `origin`, `rpId` e contador de assinatura (*signature counter*) contra clonagem de autenticador.

### 5. Cadastro, Verificação e Recuperação de Conta (Forgot Password Cheat Sheet & ASVS V2.5, V2.6, V2.7)
- [ ] **Token de Reset Seguro & ASVS V2.5.1, V2.5.2 (L2):** Verifique que o token de recuperação/verificação é gerado com CSPRNG (>= 128 bits), armazenado **hasheado** no banco, tem TTL curto (ex: 15–60 min), é de uso único e é invalidado após uso ou nova solicitação.
- [ ] **Sem Vazamento de Token & ASVS V2.5.3 (L2):** Verifique que o token não aparece em logs, no `Referer` (link para domínio externo na página de reset) nem em histórico de e-mail encaminhável sem expiração.
- [ ] **Perguntas de Segurança & ASVS V2.5.6 (L2):** Se existirem, verifique que não são usadas como único fator de recuperação (Cheat Sheet desaconselha) e que respostas são hasheadas.
- [ ] **Confirmação e Notificação & ASVS V2.6.1 (L2):** Verifique envio de e-mail de notificação em toda troca de senha, e-mail ou fator MFA, e exigência de senha atual para mudanças sensíveis (*re-authentication*).
- [ ] **Account Takeover via E-mail Change & ASVS V2.7.1 (L2):** Verifique que a troca de e-mail exige confirmação no endereço antigo **e** no novo, e não transfere sessões/privilégios antes da confirmação.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica, exiba no chat a lista detalhada de achados ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados, avaliados segundo o **OWASP Risk Rating Methodology**:

$$\text{Risco (Severidade)} = \text{Probabilidade (Likelihood)} \times \text{Impacto (Impact)}$$

*Critério da Matriz 3x3 OWASP:*
- **Alta Probabilidade × Alto Impacto** = **CRÍTICA**
- **Alta × Médio** ou **Média × Alto** = **ALTA**
- **Alta × Baixo**, **Média × Médio** ou **Baixa × Alto** = **MÉDIA**
- **Média × Baixo**, **Baixa × Médio** ou **Baixa × Baixo** = **BAIXA**

| ID | Arquivo / Ponto | Módulo / Padrão / ASVS | Probabilidade | Impacto | Severidade (RRM) | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|---|---|
| #1 | `src/auth/login.ts:44` | Session Fixation / ASVS V3.3.1 (L2) | ALTA | ALTO | CRÍTICA | Baixo (20 min) | **SIM** |
| #2 | `src/auth/jwt.ts:12` | JWT alg: none / ASVS V3.5.2 (L2) | ALTA | ALTO | CRÍTICA | Baixo (30 min) | **SIM** |
| #3 | `src/auth/reset.ts:70` | Token Claro no DB / ASVS V2.5.1 (L2) | MÉDIA | ALTO | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item da tabela:
- **Achado #[ID]:** [Nome do Problema]
- **Controle / Cheat Sheet:** [ex: Proactive C7 / Session Management Cheat Sheet / WSTG-SESS-03]
- **OWASP ASVS v4.0.3:** [Capítulo e Requisito, ex: V3.3.1 (Level 2 - Session ID Regeneration)]
- **Avaliação de Risco (OWASP Risk Rating Methodology):**
  - *Probabilidade (Likelihood):* [BAIXA | MÉDIA | ALTA] (Agente de Ameaça + Facilidade de Descoberta/Exploração)
  - *Impacto Técnico (Tech Impact):* [BAIXO | MÉDIO | ALTO] (Confidencialidade, Integridade, Disponibilidade)
  - *Impacto de Negócio (Business Impact):* [BAIXO | MÉDIO | ALTO] (Danos Financeiros, LGPD/GDPR, Reputação)
  - *Severidade Calculada:* [CRÍTICA | ALTA | MÉDIA | BAIXA]
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
   - **Capa:** Título "Relatório de Auditoria de Identidades Digitais, Autenticação & ASVS (OWASP Proactive C7) — <nome do projeto>", data e escopo.
   - **Resumo Executivo:** Gráfico de rosca por severidade, gráfico de barras por categoria e Matriz de Calor 3x3 do OWASP Risk Rating Methodology (Likelihood × Impact).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
   - **Matriz de Conformidade C7, Cheat Sheets & ASVS:** Tabela com status por item do checklist e conformidade ASVS V2 e V3 (L1/L2/L3).
   - **Tabela Detalhada de Achados** com tags de Quick Win, notas de risco RRM e referências a arquivos e linhas.

2. **Seção "ISSUES PARA O GITHUB" no Relatório:**
   - Template Markdown completo pronto para copiar e colar para cada achado, com labels, passos de reprodução, avaliação de risco formal (RRM: Probabilidade x Impacto), impacto e critérios de aceite.

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
