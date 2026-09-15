# PROMPT DE AUDITORIA COMPLETA: FRONTEND & SPAS, OWASP CLIENT-SIDE SECURITY (WSTG), OWASP ASVS v4.0.3, OWASP RISK RATING METHODOLOGY, PERFORMANCE E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Frontend e Especialista em AppSec Client-Side (Yellow Team / Browser Security Lead). Sua missão é realizar uma varredura completa no repositório aplicando as diretrizes do **OWASP Client-Side Security Cheat Sheet Series**, os testes de cliente do **OWASP WSTG v4.2** (*WSTG-CLNT*) e os requisitos normativos do **OWASP Application Security Verification Standard (OWASP ASVS v4.0.3)** (Capítulo V5 - Validation, Sanitization and Encoding, Capítulo V3 - Session Management e Capítulo V14 - Configuration Verification Requirements).

A severidade de cada vulnerabilidade identificada deve ser formalmente mensurada aplicando o **OWASP Risk Rating Methodology**, combinando a Probabilidade (*Likelihood*) com o Impacto (*Impact*) em uma matriz determinística 3x3.

A auditoria deve identificar falhas de segurança no lado do cliente (Client-Side Security), vulnerabilidades clássicas e modernas de SPAs (React, Vue, Angular, Svelte, Next.js/Nuxt), SSTI em Server-Side Rendering, segurança em WebSockets (CSWSH), riscos de *Prototype Pollution* no navegador, comunicação insegura via `window.postMessage`, vazamento de credenciais em bundles, headers defensivos e problemas críticos de performance web (Core Web Vitals).

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios do projeto e identifique a stack/framework utilizado (React, Next.js, Vue, Nuxt, Angular, SvelteKit, Vite, Webpack, etc.).
2. Leia todos os arquivos de documentação técnica existentes (`README.md`, `/docs`, guias de contribuição).
3. Identifique e analise TODOS os arquivos da camada de cliente e SSR: componentes, páginas/rotas, templates de renderização no servidor, conexões de WebSocket, gerenciadores de estado global (Redux, Zustand, Pinia), interceptadores HTTP (Axios, Fetch, TanStack Query), arquivos de configuração de build, headers/meta-tags HTML, manipuladores de eventos (`message`, `storage`) e utilitários de autenticação.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP CLIENT-SIDE, WSTG-CLNT & OWASP ASVS v4.0.3)

### 1. Injeções, DOM XSS e Sanitização Moderna (OWASP DOM-based XSS & WSTG-INPV-18 & ASVS V5.2)
- [ ] **Cross-Site Scripting (DOM & Reflected XSS) & ASVS V5.2.1, V5.2.2 (L1):** Identifique renderizações inseguras de HTML sem sanitização estrita (ex: `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`, `bypassSecurityTrustHtml`).
- [ ] **Manipulação Direta e Sinks Inseguros do DOM & ASVS V5.2.3, V5.2.7 (L1):** Localize usos perigosos de `eval()`, `document.write()`, `element.insertAdjacentHTML()`, `window.location.href = userInput` ou injeção dinâmica de scripts sem validação de URL.
- [ ] **Trusted Types API Support & ASVS V5.2.8 (L2):** Verifique se a aplicação possui suporte a **Trusted Types** (`require-trusted-types-for 'script'` no CSP e uso de `trustedTypes.createPolicy()`), bloqueando injeção de strings brutas no DOM diretamente no motor do navegador.
- [ ] **SSTI em Server-Side Rendering (WSTG-INPV-18 & ASVS V5.2.4 - L2):** Em aplicações com SSR (Next.js, Nuxt, SvelteKit) ou templates no servidor (EJS, Handlebars, Pug), identifique interpolação direta de entrada de usuário no corpo de templates gerando execução arbitrária de código.
- [ ] **Client-Side Prototype Pollution & ASVS V5.2.6 (L2):** Identifique funções recursivas de clonagem ou merge de objetos (`lodash.merge`, `Object.assign`, `deepMerge`) recebendo inputs não confiáveis do cliente ou queries que possam poluir `Object.prototype`.
- [ ] **Open Redirect no Cliente & ASVS V5.1.1, V5.2.5 (L1):** Verifique se parâmetros de query string (ex: `?redirect=/dashboard` ou `?returnUrl=https://...`) são usados diretamente em roteadores/redirecionamentos sem validação de caminhos relativos ou whitelist de domínios seguros.

### 2. Comunicação Entre Janelas, WebSockets, Clickjacking e CSRF (WSTG-CLNT & ASVS V4.2, V13.1)
- [ ] **Segurança de `window.postMessage` & ASVS V4.2.4, V14.4.6 (L1):** Verifique se os ouvintes de eventos de mensagem (`window.addEventListener('message', ...)`) validam rigorosamente a origem (`event.origin === TRUSTED_DOMAIN`) e a fonte (`event.source`) antes de processar payloads ou executar ações no estado global.
- [ ] **WebSocket Security & CSWSH (WSTG-CLNT-10 & ASVS V13.1.2 - L2):** Verifique se conexões WebSocket no cliente validam tokens de autenticação temporários e se o handshake exige verificação estrita do cabeçalho `Origin` no servidor, mitigando Cross-Site WebSocket Hijacking.
- [ ] **Defesa contra Clickjacking / UI Redressing & ASVS V14.4.3 (L1):** Verifique a presença de `Content-Security-Policy: frame-ancestors 'none'` ou `'self'` (ou `X-Frame-Options: DENY`), impedindo que a aplicação seja renderizada dentro de iframes maliciosos transparentes.
- [ ] **Prevenção CSRF e Interceptadores HTTP & ASVS V4.2.4 (L1):** Verifique se requisições mutativas (POST/PUT/DELETE) que utilizam cookies de sessão possuem cabeçalhos anti-CSRF customizados (ex: `X-Requested-With`, `X-CSRF-Token`) ou se os cookies utilizam `SameSite=Strict/Lax`.
- [ ] **Reverse Tabnabbing & ASVS V14.4.6 (L1):** Verifique se todas as tags `<a target="_blank">` possuem o atributo `rel="noopener noreferrer"` para impedir manipulação da página de origem (`window.opener`).

### 3. Armazenamento Seguro, Tokens e Cookies (ASVS V3.4, V3.5, V8.2)
- [ ] **Armazenamento Inseguro de Tokens & ASVS V3.5.5, V8.2.3 (L2):** Verifique se tokens JWT de acesso ou refresh tokens estão sendo persistidos em `localStorage` ou `sessionStorage` (expostos a roubo via XSS), em vez de cookies `HttpOnly` com flags `Secure` e `SameSite`.
- [ ] **Prefixos de Cookies Seguros (RFC 6265bis & ASVS V3.4.2 - L2):** Verifique o uso de prefixos `__Host-` ou `__Secure-` para cookies de sessão e autenticação, garantindo que não sejam sobrescritos por subdomínios não confiáveis.
- [ ] **Vazamento de Segredos no Bundle Client-Side & ASVS V14.1.1, V14.1.2 (L1):** Identifique variáveis de ambiente privadas ou chaves de API secretas vazando nos arquivos de build do cliente (ex: expostas via prefixos `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` ou chaves privadas *hardcoded*).
- [ ] **Validação de Permissões no Cliente (UI Bypass) & ASVS V4.1.3 (L1):** Identifique se regras críticas de negócio e componentes sensíveis são apenas ocultados via CSS/JS (`v-if`, `&&`, `display: none`) sem validação correspondente e estrita no backend.

### 4. Headers de Segurança, Subresource Integrity e Performance (ASVS V14.4, V10.3)
- [ ] **Content Security Policy (CSP Estrito) & ASVS V14.4.2 (L2):** Verifique se o frontend define um CSP robusto sem diretivas perigosas (`'unsafe-eval'`, `'unsafe-inline'` desnecessário), utilizando nonces criptográficos ou hashes SHA-256 para scripts inline.
- [ ] **Subresource Integrity (SRI) & ASVS V10.3.1, V14.4.6 (L2):** Identifique scripts externos ou estilos carregados via CDNs de terceiros (`<script src="https://...">`) sem os atributos `integrity="sha384-..."` e `crossorigin="anonymous"`.
- [ ] **Lazy Loading & Bundle Size:** Identifique ausência de carregamento dinâmico (`dynamic import`, `React.lazy`) em rotas pesadas ou bibliotecas volumosas importadas globalmente.
- [ ] **Vazamentos de Memória e PII em Logs & ASVS V7.1.1 (L2):** Localize listeners de eventos, timers (`setInterval`) ou subscriptions não cancelados no ciclo de desmontagem (`useEffect cleanup`, `onUnmounted`) e verifique a ausência de `console.log()` com dados PII em produção.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, avaliados segundo o **OWASP Risk Rating Methodology**:

$$\text{Risco (Severidade)} = \text{Probabilidade (Likelihood)} \times \text{Impacto (Impact)}$$

*Critério da Matriz 3x3 OWASP:*
- **Alta Probabilidade × Alto Impacto** = **CRÍTICA**
- **Alta × Médio** ou **Média × Alto** = **ALTA**
- **Alta × Baixo**, **Média × Médio** ou **Baixa × Alto** = **MÉDIA**
- **Média × Baixo**, **Baixa × Médio** ou **Baixa × Baixo** = **BAIXA**

| ID | Arquivo / Ponto | Categoria / ASVS | Probabilidade | Impacto | Severidade (RRM) | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|---|---|
| #1 | `src/components/UserBio.tsx:34` | OWASP DOM XSS / ASVS V5.2.1 (L1) | ALTA | ALTO | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `src/listeners/message.ts:12` | PostMessage / ASVS V14.4.6 (L1) | ALTA | MÉDIO | ALTA | Baixo (20 min) | **SIM** |
| #3 | `src/utils/auth.ts:25` | Tokens localStorage / ASVS V3.5.5 (L2) | MÉDIA | ALTO | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Categoria / Padrão:** [DOM XSS & Trusted Types / PostMessage & WebSockets / Clickjacking & CSRF / Storage & Secrets / CSP & SRI / Performance]
- **OWASP ASVS v4.0.3:** [Capítulo e Requisito, ex: V5.2.1 (Level 1 - Output Encoding and Injection Prevention)]
- **Avaliação de Risco (OWASP Risk Rating Methodology):**
  - *Probabilidade (Likelihood):* [BAIXA | MÉDIA | ALTA] (Agente de Ameaça + Facilidade de Descoberta/Exploração)
  - *Impacto Técnico (Tech Impact):* [BAIXO | MÉDIO | ALTO] (Confidencialidade, Integridade, Disponibilidade)
  - *Impacto de Negócio (Business Impact):* [BAIXO | MÉDIO | ALTO] (Danos Financeiros, LGPD/GDPR, Reputação)
  - *Severidade Calculada:* [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Vetor de Exploração:** Explicação direta de como um atacante pode injetar scripts, roubar sessões, manipular iframes ou sequestrar conexões em tempo real.
- **Evidência:** Trecho do código-fonte atual identificado no repositório.
- **Correção Recomendada:** Código devidamente refatorado aplicando as melhores práticas do OWASP Client-Side Security, WSTG e ASVS.
- **Comando de Verificação da Correção:** Como o desenvolvedor valida em 1 comando (teste automatizado ou verificação estática) que a correção funcionou.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/frontend-audit/relatorio-auditoria-frontend.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Frontend, SPAs & ASVS (OWASP Client-Side & WSTG) — <nome do projeto>", data, escopo auditado e nota metodológica.
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade, gráfico de barras por categoria OWASP e Matriz de Calor 3x3 do OWASP Risk Rating Methodology (Likelihood × Impact).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (o que está protegido no client-side, com evidência) e **Pontos Fracos** (os riscos centrais).
d) **Matriz de Conformidade OWASP Client-Side, WSTG & ASVS:** Tabela indicando status para DOM XSS, PostMessage, WebSockets, CSP, Cookies, Clickjacking e conformidade ASVS V3, V5 e V14 (L1/L2/L3).
e) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição, com indicação/chip de severidade, nota RRM e tag de Quick Win.
f) **Recomendações Priorizadas** (P1, P2, P3...).
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[Frontend/Segurança] <descrição curta da falha>`
   - Labels sugeridas: `frontend`, `security`, `performance` + severidade
   - Descrição do problema, cenário de exploração no browser e avaliação formal de risco (RRM: Probabilidade x Impacto)
   - Evidência: `arquivo:linha` com trecho de código
   - Impacto (ex: roubo de token de sessão, execução arbitrária de JavaScript, sequestro de interface)
   - Sugestão de correção com código seguro
   - Critérios de aceite (checklist verificável)

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use ambiente Python isolado (`venv` com `reportlab` + `matplotlib`).
- Salve o script gerador em `docs/frontend-audit/generate_report.py`.
- Formatação das páginas: tamanho A4, margens de 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS
Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/frontend-audit/relatorio-auditoria-frontend.pdf`, `docs/frontend-audit/generate_report.py`).