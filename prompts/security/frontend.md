# PROMPT DE AUDITORIA COMPLETA: FRONTEND & SPAS, OWASP CLIENT-SIDE SECURITY, PERFORMANCE E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Frontend e Especialista em AppSec Client-Side (Yellow Team / Browser Security Lead). Sua missão é realizar uma varredura completa no repositório aplicando as diretrizes do **OWASP Client-Side Security Cheat Sheet Series** (*DOM-based XSS Prevention, XSS Prevention, Content Security Policy, HTML5 Security, Clickjacking Defense, CSRF Prevention e Secure Cookies*).

A auditoria deve identificar falhas de segurança no lado do cliente (Client-Side Security), vulnerabilidades clássicas e modernas de SPAs (React, Vue, Angular, Svelte, Next.js/Nuxt), riscos de *Prototype Pollution* no navegador, comunicação insegura via `window.postMessage`, vazamento de credenciais em bundles, headers defensivos e problemas críticos de performance web (Core Web Vitals).

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios do projeto e identifique a stack/framework utilizado (React, Next.js, Vue, Nuxt, Angular, SvelteKit, Vite, Webpack, etc.).
2. Leia todos os arquivos de documentação técnica existentes (`README.md`, `/docs`, guias de contribuição).
3. Identifique e analise TODOS os arquivos da camada de cliente: componentes, páginas/rotas, gerenciadores de estado global (Redux, Zustand, Pinia, Recoil), interceptadores HTTP (Axios, Fetch, TanStack Query), arquivos de configuração de build, headers/meta-tags HTML, manipuladores de eventos (`message`, `storage`) e utilitários de autenticação.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP CLIENT-SIDE SECURITY & SPAS)

### 1. Injeções, DOM XSS e Sanitização Moderna (OWASP DOM-based XSS & Trusted Types)
- [ ] **Cross-Site Scripting (DOM & Reflected XSS):** Identifique renderizações inseguras de HTML sem sanitização estrita (ex: `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`, `bypassSecurityTrustHtml`).
- [ ] **Manipulação Direta e Sinks Inseguros do DOM:** Localize usos perigosos de `eval()`, `document.write()`, `element.insertAdjacentHTML()`, `window.location.href = userInput` ou injeção dinâmica de scripts sem validação de URL.
- [ ] **Trusted Types API Support:** Verifique se a aplicação possui suporte a **Trusted Types** (`require-trusted-types-for 'script'` no CSP e uso de `trustedTypes.createPolicy()`), bloqueando injeção de strings brutas no DOM diretamente no motor do navegador.
- [ ] **Client-Side Prototype Pollution:** Identifique funções recursivas de clonagem ou merge de objetos (`lodash.merge`, `Object.assign`, `deepMerge`) recebendo inputs não confiáveis do cliente ou queries que possam poluir `Object.prototype`.
- [ ] **Open Redirect no Cliente:** Verifique se parâmetros de query string (ex: `?redirect=/dashboard` ou `?returnUrl=https://...`) são usados diretamente em roteadores/redirecionamentos sem validação de caminhos relativos ou whitelist de domínios seguros.

### 2. Comunicação Entre Janelas, Clickjacking e CSRF (OWASP HTML5 & Defense)
- [ ] **Segurança de `window.postMessage`:** Verifique se os ouvintes de eventos de mensagem (`window.addEventListener('message', ...)`) validam rigorosamente a origem (`event.origin === TRUSTED_DOMAIN`) e a fonte (`event.source`) antes de processar payloads ou executar ações no estado global.
- [ ] **Defesa contra Clickjacking / UI Redressing:** Verifique a presença de `Content-Security-Policy: frame-ancestors 'none'` ou `'self'` (ou `X-Frame-Options: DENY`), impedindo que a aplicação seja renderizada dentro de iframes maliciosos transparentes.
- [ ] **Prevenção CSRF e Interceptadores HTTP:** Verifique se requisições mutativas (POST/PUT/DELETE) que utilizam cookies de sessão possuem cabeçalhos anti-CSRF customizados (ex: `X-Requested-With`, `X-CSRF-Token`) ou se os cookies utilizam `SameSite=Strict/Lax`.
- [ ] **Reverse Tabnabbing:** Verifique se todas as tags `<a target="_blank">` possuem o atributo `rel="noopener noreferrer"` para impedir manipulação da página de origem (`window.opener`).

### 3. Armazenamento Seguro, Tokens e Cookies (OWASP Storage & Cookies Cheat Sheet)
- [ ] **Armazenamento Inseguro de Tokens:** Verifique se tokens JWT de acesso ou refresh tokens estão sendo persistidos em `localStorage` ou `sessionStorage` (expostos a roubo via XSS), em vez de cookies `HttpOnly` com flags `Secure` e `SameSite`.
- [ ] **Prefixos de Cookies Seguros (RFC 6265bis):** Verifique o uso de prefixos `__Host-` ou `__Secure-` para cookies de sessão e autenticação, garantindo que não sejam sobrescritos por subdomínios não confiáveis.
- [ ] **Vazamento de Segredos no Bundle Client-Side:** Identifique variáveis de ambiente privadas ou chaves de API secretas vazando nos arquivos de build do cliente (ex: expostas via prefixos `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` ou chaves privadas *hardcoded*).
- [ ] **Validação de Permissões no Cliente (UI Bypass):** Identifique se regras críticas de negócio e componentes sensíveis são apenas ocultados via CSS/JS (`v-if`, `&&`, `display: none`) sem validação correspondente e estrita no backend.

### 4. Headers de Segurança, Subresource Integrity e Performance (Core Web Vitals)
- [ ] **Content Security Policy (CSP Estrito):** Verifique se o frontend define um CSP robusto sem diretivas perigosas (`'unsafe-eval'`, `'unsafe-inline'` desnecessário), utilizando nonces criptográficos ou hashes SHA-256 para scripts inline.
- [ ] **Subresource Integrity (SRI):** Identifique scripts externos ou estilos carregados via CDNs de terceiros (`<script src="https://...">`) sem os atributos `integrity="sha384-..."` e `crossorigin="anonymous"`.
- [ ] **Lazy Loading & Bundle Size:** Identifique ausência de carregamento dinâmico (`dynamic import`, `React.lazy`) em rotas pesadas ou bibliotecas volumosas importadas globalmente.
- [ ] **Vazamentos de Memória e PII em Logs:** Localize listeners de eventos, timers (`setInterval`) ou subscriptions não cancelados no ciclo de desmontagem (`useEffect cleanup`, `onUnmounted`) e verifique a ausência de `console.log()` com dados PII em produção.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/components/UserBio.tsx:34` | OWASP DOM XSS | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `src/listeners/message.ts:12` | PostMessage Inseguro (No Origin Check) | ALTA | Baixo (20 min) | **SIM** |
| #3 | `src/utils/auth.ts:25` | Tokens em localStorage | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [DOM XSS & Trusted Types / PostMessage Security / Clickjacking & CSRF / Storage & Secrets / CSP & SRI / Performance]
- **Vetor de Exploração:** Explicação direta de como um atacante pode injetar scripts, roubar sessões, manipular iframes ou sequestrar contas no navegador.
- **Evidência:** Trecho do código-fonte atual identificado no repositório.
- **Correção Recomendada:** Código devidamente refatorado aplicando as melhores práticas do OWASP Client-Side Security.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/frontend-audit/relatorio-auditoria-frontend.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Frontend e SPAs (OWASP Client-Side Standards) — <nome do projeto>", data, escopo auditado e nota metodológica.
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria OWASP.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (o que está protegido no client-side, com evidência) e **Pontos Fracos** (os riscos centrais).
d) **Matriz de Conformidade OWASP Client-Side:** Tabela indicando status para DOM XSS, PostMessage, CSP, Cookies e Clickjacking.
e) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição, com indicação/chip de severidade e tag de Quick Win.
f) **Recomendações Priorizadas** (P1, P2, P3...).
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[Frontend/Segurança] <descrição curta da falha>`
   - Labels sugeridas: `frontend`, `security`, `performance` + severidade
   - Descrição do problema e cenário de exploração no browser
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