# PROMPT DE AUDITORIA COMPLETA: CONFIGURAÇÃO SEGURA POR PADRÃO (OWASP PROACTIVE CONTROL C5), HEADERS, CORS, COOKIES, TLS E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Hardening de Aplicação (Yellow Team). Sua missão é realizar uma varredura completa no repositório aplicando o **OWASP Top 10 Proactive Controls 2024 — C5: Secure by Default Configurations** e as diretrizes do **OWASP Cheat Sheet Series** (*HTTP Security Response Headers, Content Security Policy, Transport Layer Security, HTTP Strict Transport Security, Cross-Site Request Forgery Prevention, Session Management (cookie attributes), Error Handling, Docker Security*), reforçadas por **A05:2021 — Security Misconfiguration** e **WSTG-CONF**.

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

## CHECKLIST DE AUDITORIA PRÁTICA (OWASP PROACTIVE C5 & CHEAT SHEETS)

### 1. Estado Default e Superfície Exposta (A05:2021 / WSTG-CONF)
- [ ] **Secure by Default:** Verifique que, sem variáveis de ambiente definidas, a app não sobe em modo inseguro (debug on, auth desabilitada, CORS liberado, TLS off). O default ausente deve ser o mais restritivo.
- [ ] **Debug / Stack Traces Desligados em Produção:** `DEBUG=False` (Django), sem `app.set('env','development')`, sem `NODE_ENV` faltando, sem `spring.profiles=dev`, sem `detailed errors`/`whoops`/`werkzeug` debugger exposto.
- [ ] **Credenciais e Segredos Default:** Sem senha/admin/JWT secret padrão embutido (`changeme`, `admin/admin`, `secret`), sem chave de assinatura fixa no repositório, sem contas de seed com senha conhecida ativas em produção.
- [ ] **Endpoints de Diagnóstico:** `/actuator/*`, `/debug`, `/__debug__`, `/metrics`, `/graphql` playground, Swagger UI, `/.git`, `/.env`, listagem de diretório, `phpinfo` — verifique se estão desabilitados ou autenticados/segregados por rede em produção.
- [ ] **Versões e Banners:** Verifique remoção/ocultação de `X-Powered-By`, `Server` verboso e mensagens que revelam framework/versão.

### 2. HTTP Security Response Headers (Headers + CSP Cheat Sheets)
- [ ] **`Strict-Transport-Security`:** Presente com `max-age >= 31536000`, `includeSubDomains` e (se aplicável) `preload`. Só via HTTPS.
- [ ] **`Content-Security-Policy`:** Política restritiva definida (idealmente `default-src 'self'`, sem `unsafe-inline`/`unsafe-eval`, uso de nonce/hash); ausência de CSP ou CSP só em `report-only` sem enforcement é achado.
- [ ] **`X-Content-Type-Options: nosniff`**, **`X-Frame-Options: DENY`/`SAMEORIGIN`** ou `frame-ancestors` na CSP (anti-clickjacking), **`Referrer-Policy`** restritivo (`no-referrer`/`strict-origin-when-cross-origin`), **`Permissions-Policy`** desligando APIs não usadas.
- [ ] **Cache de Respostas Sensíveis:** `Cache-Control: no-store` em respostas autenticadas/PII; ausência de dados sensíveis servidos com cache público.
- [ ] **Headers Legados/Perigosos:** Sem `Access-Control-Allow-Origin: *` fixo em resposta autenticada; sem `X-XSS-Protection` habilitado com valores problemáticos.

### 3. CORS (definição no código, não só header)
- [ ] **Origin Allow-List Estrita:** Verifique lista fechada de origens confiáveis; ausência de `origin: true`/reflexão automática do header `Origin`, ausência de regex com ponto não escapado (`/.*\.exemplo\.com/` aceitando `exemploXcom`).
- [ ] **Credenciais + Wildcard:** Verifique que `Access-Control-Allow-Credentials: true` nunca coexiste com origem `*` ou refletida sem allow-list.
- [ ] **Métodos e Headers:** `Allow-Methods`/`Allow-Headers` mínimos necessários, sem `*` amplo; `Access-Control-Max-Age` razoável.

### 4. Cookies e CSRF (Session Management + CSRF Prevention Cheat Sheets)
- [ ] **Atributos de Cookie:** Todo cookie de sessão/auth com `HttpOnly`, `Secure`, `SameSite=Lax`/`Strict`, `Path` restrito, sem `Domain` amplo, prefixo `__Host-` quando possível.
- [ ] **Proteção CSRF:** Para apps com sessão via cookie, verifique token anti-CSRF (sincronizador ou double-submit) OU dependência exclusiva de `SameSite` documentada e consistente; endpoints que mudam estado via `GET` são achado.
- [ ] **Escopo do Cookie:** Sem cookies de auth enviados para subdomínios/caminhos que não precisam; sem segredo em cookie não assinado/não cifrado.

### 5. TLS e Transporte (TLS + HSTS Cheat Sheets)
- [ ] **Redirecionamento HTTP→HTTPS** forçado; sem endpoints sensíveis servidos em texto claro internamente sem justificativa.
- [ ] **Versões e Cifras:** TLS 1.2+ (preferir 1.3), sem SSLv3/TLS 1.0/1.1, sem cifras `RC4`/`3DES`/`NULL`/export.
- [ ] **Validação de Certificado em Chamadas de Saída:** Sem `rejectUnauthorized: false`, `verify=False` (requests), `InsecureSkipVerify: true` (Go), `curl -k` em scripts de produção.
- [ ] **mTLS entre serviços internos sensíveis** quando o modelo de ameaça exige.

### 6. Hardening de Plataforma (Docker Security Cheat Sheet — complementa `iac_docker_k8s.md`)
- [ ] Container não roda como `root` (`USER` não-privilegiado), sem `--privileged`, filesystem root read-only quando possível, sem secrets em `ENV`/`ARG` do `Dockerfile`, imagem base mínima e pinada por digest.
- [ ] Sem porta de serviço interno (DB, cache, admin) publicada no host/internet sem necessidade.

### 7. Gestão de Configuração
- [ ] **Sem Segredo Versionado:** `.env` real fora do repositório; só `.env.example` com placeholders. (Aprofundar em `secrets.md`.)
- [ ] **Parity e Auditoria:** Configuração de produção derivada de fonte controlada (não editada à mão no servidor); mudança de config versionada e revisável.
- [ ] **Feature Flags Seguros:** Flags de recurso arriscado default `off`; kill-switch documentado.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica, exiba no chat a lista detalhada de achados ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados:

| ID | Arquivo / Ponto | Módulo / Padrão | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/app.ts:18` | CORS reflete `Origin` com `credentials:true` | CRÍTICA | Baixo (20 min) | **SIM** |
| #2 | `config/settings.py:5` | `DEBUG = True` sem guard de ambiente | CRÍTICA | Baixo (15 min) | **SIM** |
| #3 | `src/app.ts:30` | Sem HSTS nem CSP | ALTA | Baixo (40 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item da tabela:
- **Achado #[ID]:** [Nome do Problema]
- **Controle / Cheat Sheet:** [ex: Proactive C5 / HTTP Security Response Headers Cheat Sheet / A05:2021 / WSTG-CONF-07]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
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
   - **Capa:** Título "Relatório de Auditoria de Configuração Segura (OWASP Proactive C5) — <nome do projeto>", data e escopo.
   - **Resumo Executivo:** Gráfico de rosca por severidade e gráfico de barras por categoria (Estado Default, Headers/CSP, CORS, Cookies/CSRF, TLS, Plataforma).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
   - **Checklist de Hardening:** Tabela item × status (Conforme / Não Conforme / Não Aplicável).
   - **Tabela Detalhada de Achados** com tags de Quick Win e referências a arquivos e linhas.

2. **Seção "ISSUES PARA O GITHUB" no Relatório:**
   - Template Markdown completo pronto para copiar e colar para cada achado, com labels, passos de reprodução, impacto e critérios de aceite.

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
