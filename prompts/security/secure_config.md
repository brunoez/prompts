# PROMPT DE AUDITORIA COMPLETA: CONFIGURAÇÃO SEGURA POR PADRÃO (OWASP PROACTIVE CONTROL C5, OWASP ASVS v4.0.3 & OWASP RISK RATING METHODOLOGY), HEADERS, CORS, COOKIES, TLS E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Hardening de Aplicação (Yellow Team). Sua missão é realizar uma varredura completa no repositório aplicando o **OWASP Top 10 Proactive Controls 2024 — C5: Secure by Default Configurations**, as diretrizes do **OWASP Cheat Sheet Series** (*HTTP Security Response Headers, Content Security Policy, Transport Layer Security, HTTP Strict Transport Security, Cross-Site Request Forgery Prevention, Session Management (cookie attributes), Error Handling, Docker Security*), a categoria **A05:2021 — Security Misconfiguration**, os testes do **OWASP WSTG v4.2** (*WSTG-CONF*) e os requisitos normativos do **OWASP Application Security Verification Standard (OWASP ASVS v4.0.3)** (Capítulo V14 - Configuration, Capítulo V7 - Error Handling and Logging e Capítulo V9 - Communications Verification Requirements).

A severidade de cada vulnerabilidade identificada deve ser formalmente mensurada aplicando o **OWASP Risk Rating Methodology**, combinando a Probabilidade (*Likelihood*) com o Impacto (*Impact*) em uma matriz determinística 3x3.

A auditoria deve garantir que a aplicação seja segura no estado default: sem features de debug em produção, sem credenciais padrão, com headers defensivos, CORS restritivo, cookies endurecidos, TLS moderno obrigatório, superfície mínima exposta e mensagens de erro que não vazam detalhes internos.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique framework web (Express/Nest/Fastify, Django/FastAPI/Flask, Spring Boot, Rails, ASP.NET), reverse proxy/servidor (nginx, Caddy, Traefik, API Gateway) e plataforma de deploy.
2. Identifique e analise TODOS os arquivos de configuração: `app`/`main`/`server` bootstrap, middlewares globais (`helmet`, `cors`, `csurf`, `django.middleware.security`, `SecurityFilterChain`), `settings.py`/`config/*.{js,ts,yaml,env}`, `nginx.conf`/`Caddyfile`, `Dockerfile`/`docker-compose.yml`, manifests de deploy, `.env.example` e valores default embutidos no código.
3. Diferencie configuração por ambiente: verifique o que está ligado em `production` vs `development` e se o default (sem env var setada) falha para o modo **seguro**.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.
5. **Diretriz Anti-Fadiga e Anti-Alucinação (Filtro Factual):** Só reporte configurações inseguras categoricamente comprovadas pelos arquivos inspecionados. É proibido levantar hipóteses sem evidência. Ajustes cosméticos sem impacto real devem ser marcados como `[NIT]` ou descartados, com foco no risco real e no *Blast Radius*.

---

## CHECKLIST DE AUDITORIA PRÁTICA (OWASP PROACTIVE C5, CHEAT SHEETS & OWASP ASVS v4.0.3)

### 1. Estado Default e Superfície Exposta (A05:2021 / WSTG-CONF & ASVS V14.1, V14.2)
- [ ] **Secure by Default & ASVS V14.1.1, V14.2.1 (L1):** Verifique que, sem variáveis de ambiente definidas, a app não sobe em modo inseguro (debug on, auth desabilitada, CORS liberado, TLS off). O default ausente deve ser o mais restritivo.
- [ ] **Debug / Stack Traces Desligados em Produção & ASVS V14.1.4, V7.2.1 (L1):** `DEBUG=False` (Django), sem `app.set('env','development')`, sem `NODE_ENV` faltando, sem `spring.profiles=dev`, sem `detailed errors`/`whoops`/`werkzeug` debugger exposto.
- [ ] **Credenciais e Segredos Default & ASVS V14.1.2, V2.1.2 (L1):** Sem senha/admin/JWT secret padrão embutido (`changeme`, `admin/admin`, `secret`), sem chave de assinatura fixa no repositório, sem contas de seed com senha conhecida ativas em produção.
- [ ] **Endpoints de Diagnóstico & ASVS V14.2.2, V14.4.1 (L2):** `/actuator/*`, `/debug`, `/__debug__`, `/metrics`, `/graphql` playground, Swagger UI, `/.git`, `/.env`, listagem de diretório, `phpinfo` — verifique se estão desabilitados ou autenticados/segregados por rede em produção.
- [ ] **Versões e Banners & ASVS V14.3.1 (L1):** Verifique remoção/ocultação de `X-Powered-By`, `Server` verboso e mensagens que revelam framework/versão.

### 2. HTTP Security Response Headers (Headers + CSP Cheat Sheets & ASVS V14.4)
- [ ] **`Strict-Transport-Security` & ASVS V9.2.1, V14.4.1 (L1):** Presente com `max-age >= 31536000`, `includeSubDomains` e (se aplicável) `preload`. Só via HTTPS.
- [ ] **`Content-Security-Policy` & ASVS V14.4.2, V5.2.3 (L2):** Política restritiva definida (idealmente `default-src 'self'`, sem `unsafe-inline`/`unsafe-eval`, uso de nonce/hash); ausência de CSP ou CSP só em `report-only` sem enforcement é achado.
- [ ] **`X-Content-Type-Options: nosniff` & ASVS V14.4.3, V14.4.4 (L1):**, **`X-Frame-Options: DENY`/`SAMEORIGIN`** ou `frame-ancestors` na CSP (anti-clickjacking), **`Referrer-Policy`** restritivo (`no-referrer`/`strict-origin-when-cross-origin`), **`Permissions-Policy`** desligando APIs não usadas.
- [ ] **Cache de Respostas Sensíveis & ASVS V8.2.3, V14.4.5 (L2):** `Cache-Control: no-store` em respostas autenticadas/PII; ausência de dados sensíveis servidos com cache público.
- [ ] **Headers Legados/Perigosos & ASVS V14.4.6 (L1):** Sem `Access-Control-Allow-Origin: *` fixo em resposta autenticada; sem `X-XSS-Protection` habilitado com valores problemáticos.

### 3. CORS (definição no código, não só header & ASVS V14.4.7)
- [ ] **Origin Allow-List Estrita & ASVS V14.4.7 (L2):** Verifique lista fechada de origens confiáveis; ausência de `origin: true`/reflexão automática do header `Origin`, ausência de regex com ponto não escapado (`/.*\.exemplo\.com/` aceitando `exemploXcom`).
- [ ] **Credenciais + Wildcard & ASVS V14.4.7 (L2):** Verifique que `Access-Control-Allow-Credentials: true` nunca coexiste com origem `*` ou refletida sem allow-list.
- [ ] **Métodos e Headers & ASVS V14.4.7 (L2):** `Allow-Methods`/`Allow-Headers` mínimos necessários, sem `*` amplo; `Access-Control-Max-Age` razoável.

### 4. Cookies e CSRF (Session Management + CSRF Prevention Cheat Sheets & ASVS V3.4, V4.2)
- [ ] **Atributos de Cookie & ASVS V3.4.1, V3.4.2, V3.4.3 (L1):** Todo cookie de sessão/auth com `HttpOnly`, `Secure`, `SameSite=Lax`/`Strict`, `Path` restrito, sem `Domain` amplo, prefixo `__Host-` quando possível.
- [ ] **Proteção CSRF & ASVS V4.2.4, V4.2.5 (L1):** Para apps com sessão via cookie, verifique token anti-CSRF (sincronizador ou double-submit) OU dependência exclusiva de `SameSite` documentada e consistente; endpoints que mudam estado via `GET` são achado.
- [ ] **Escopo do Cookie & ASVS V3.4.4 (L2):** Sem cookies de auth enviados para subdomínios/caminhos que não precisam; sem segredo em cookie não assinado/não cifrado.

### 5. TLS e Transporte (TLS + HSTS Cheat Sheets & ASVS V9.1, V9.2)
- [ ] **Redirecionamento HTTP→HTTPS & ASVS V9.1.1 (L1):** forçado; sem endpoints sensíveis servidos em texto claro internamente sem justificativa.
- [ ] **Versões e Cifras & ASVS V9.1.2, V9.1.3 (L2):** TLS 1.2+ (preferir 1.3), sem SSLv3/TLS 1.0/1.1, sem cifras `RC4`/`3DES`/`NULL`/export.
- [ ] **Validação de Certificado em Chamadas de Saída & ASVS V9.2.2 (L1):** Sem `rejectUnauthorized: false`, `verify=False` (requests), `InsecureSkipVerify: true` (Go), `curl -k` em scripts de produção.
- [ ] **mTLS entre serviços internos sensíveis & ASVS V9.1.4 (L3):** quando o modelo de ameaça exige.

### 6. Hardening de Plataforma (Docker Security Cheat Sheet & ASVS V14.2, V14.4)
- [ ] **Isolamento de Contêineres & ASVS V14.2.3, V14.2.4 (L2):** Container não roda como `root` (`USER` não-privilegiado), sem `--privileged`, filesystem root read-only quando possível, sem secrets em `ENV`/`ARG` do `Dockerfile`, imagem base mínima e pinada por digest.
- [ ] **Exposição de Portas & ASVS V14.4.1 (L2):** Sem porta de serviço interno (DB, cache, admin) publicada no host/internet sem necessidade.

### 7. Gestão de Configuração (ASVS V14.1, V14.3)
- [ ] **Sem Segredo Versionado & ASVS V14.1.1 (L1):** `.env` real fora do repositório; só `.env.example` com placeholders. (Aprofundar em `secrets.md`.)
- [ ] **Parity e Auditoria & ASVS V14.3.2 (L2):** Configuração de produção derivada de fonte controlada (não editada à mão no servidor); mudança de config versionada e revisável.
- [ ] **Feature Flags Seguros & ASVS V1.1.7 (L2):** Flags de recurso arriscado default `off`; kill-switch documentado.

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
| #1 | `src/app.ts:18` | CORS reflete Origin / ASVS V14.4.7 (L2) | ALTA | ALTO | CRÍTICA | Baixo (20 min) | **SIM** |
| #2 | `config/settings.py:5` | DEBUG = True / ASVS V14.1.4 (L1) | ALTA | ALTO | CRÍTICA | Baixo (15 min) | **SIM** |
| #3 | `src/app.ts:30` | Sem HSTS / CSP / ASVS V14.4.1 (L1) | ALTA | MÉDIO | ALTA | Baixo (40 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item da tabela:
- **Achado #[ID]:** [Nome do Problema]
- **Controle / Cheat Sheet:** [ex: Proactive C5 / HTTP Security Response Headers Cheat Sheet / A05:2021 / WSTG-CONF-07]
- **OWASP ASVS v4.0.3:** [Capítulo e Requisito, ex: V14.4.1 (Level 1 - Web Server and Environment Configuration)]
- **Avaliação de Risco (OWASP Risk Rating Methodology):**
  - *Probabilidade (Likelihood):* [BAIXA | MÉDIA | ALTA] (Agente de Ameaça + Facilidade de Descoberta/Exploração)
  - *Impacto Técnico (Tech Impact):* [BAIXO | MÉDIO | ALTO] (Confidencialidade, Integridade, Disponibilidade)
  - *Impacto de Negócio (Business Impact):* [BAIXO | MÉDIO | ALTO] (Danos Financeiros, LGPD/GDPR, Reputação)
  - *Severidade Calculada:* [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Vetor de Ataque / Exploração:** Como a configuração é abusada (ex: roubo de resposta autenticada via CORS, RCE via debugger, clickjacking, downgrade para HTTP).
- **Evidência:** Trecho do código-fonte/configuração vulnerável.
- **Prova de Conceito (PoC / Reprodução):** `curl -I` mostrando headers ausentes, página de origem cruzada lendo resposta, etc.
- **Correção Recomendada:** Configuração/código endurecido, com default seguro por ambiente.
- **Comando de Verificação da Correção:** Como validar em 1 comando (`curl -I`, teste automatizado de headers/CORS).

---

## GERAÇÃO DE RELATÓRIO PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script automatizado salvo em `docs/secure-config-audit/generate_report.py` para produzir:

1. **Relatório em PDF (`docs/secure-config-audit/relatorio-auditoria-config-segura.pdf`):**
   - **Capa:** Título "Relatório de Auditoria de Configuração Segura & ASVS (OWASP Proactive C5) — <nome do projeto>", data e escopo.
   - **Resumo Executivo:** Gráfico de rosca por severidade, gráfico de barras por categoria e Matriz de Calor 3x3 do OWASP Risk Rating Methodology (Likelihood × Impact).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
   - **Checklist de Hardening & ASVS:** Tabela item × status (Conforme / Não Conforme / Não Aplicável) e conformidade ASVS V7, V9 e V14 (L1/L2/L3).
   - **Tabela Detalhada de Achados** com tags de Quick Win, notas de risco RRM e referências a arquivos e linhas.

2. **Seção "ISSUES PARA O GITHUB" no Relatório:**
   - Template Markdown completo pronto para copiar e colar para cada achado, com labels, passos de reprodução, avaliação de risco formal (RRM: Probabilidade x Impacto), impacto e critérios de aceite.

### REGRAS TÉCNICAS
- Use ambiente Python isolado (`venv` temporário com `reportlab` e `matplotlib`).
- Salve o script e os artefatos em `docs/secure-config-audit/`.
- Garanta formatação A4 impecável, paginação correta e sem quebras visuais em tabelas.

---

## ENTREGÁVEIS FINAIS
Ao concluir, informe no chat:
1. A confirmação da geração do relatório PDF.
2. A lista de achados (Parte 1 e Parte 2).
3. O caminho relativo dos arquivos gerados (`docs/secure-config-audit/relatorio-auditoria-config-segura.pdf`, `docs/secure-config-audit/generate_report.py`).
