# PROMPT DE AUDITORIA COMPLETA: FRONTEND & SPAS, SEGURANÇA CLIENT-SIDE, PERFORMANCE E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Frontend e Especialista em AppSec (Yellow Team). Sua missão é realizar uma varredura completa no repositório para identificar falhas de segurança no lado do cliente (Client-Side Security), vazamento de credenciais, vulnerabilidades clássicas de SPA (React, Vue, Angular, Svelte, Next.js/Nuxt), problemas críticos de performance web (Core Web Vitals) e violações de privacidade.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios do projeto e identifique a stack/framework utilizado (React, Next.js, Vue, Nuxt, Angular, Vite, Webpack, etc.).
2. Leia todos os arquivos de documentação técnica existentes (`README.md`, `/docs`, guias de contribuição).
3. Identifique e analise TODOS os arquivos da camada de cliente: componentes, páginas/rotas, gerenciadores de estado global (Redux, Zustand, Pinia), interceptadores HTTP/Axios/Fetch, arquivos de configuração de build, headers/meta-tags HTML e utilitários de autenticação.
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (FRONTEND & SPAS)

### 1. Injeções, Renderização e Domínios Inseguros (XSS & CSRF)
- [ ] **Cross-Site Scripting (DOM/Reflected XSS):** Identifique renderizações inseguras de HTML sem sanitização (ex: `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`, `bypassSecurityTrustHtml`).
- [ ] **Manipulação Direta do DOM:** Localize usos perigosos de `document.write()`, `eval()`, `window.location.href = userInput` ou injeção de scripts dinâmicos sem validação estrita.
- [ ] **Open Redirect no Cliente:** Verifique se parâmetros de query string (ex: `?redirect=/dashboard`) são usados para redirecionamento sem validação de domínio interno/relativo.
- [ ] **Prevenção CSRF:** Verifique se requisições mutativas (POST/PUT/DELETE) dependem apenas de cookies e se há tokens anti-CSRF ou cabeçalhos customizados nos interceptadores HTTP.

### 2. Armazenamento Seguro, Autenticação e Gestão de Sessão
- [ ] **Armazenamento Inseguro de Tokens:** Verifique se tokens JWT de acesso ou refresh tokens estão sendo persistidos em `localStorage` ou `sessionStorage` (expostos a XSS), em vez de cookies `HttpOnly` com flags `Secure` e `SameSite`.
- [ ] **Vazamento de Segredos no Bundle:** Identifique variáveis de ambiente privadas ou chaves de API secretas vazando nos arquivos de build do cliente (ex: expostas via prefixos `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` ou chaves privadas *hardcoded*).
- [ ] **Validação de Permissões no Cliente (UI Bypass):** Identifique se componentes sensíveis são apenas ocultados via CSS/JS (`v-if`, `&&`, `display: none`) sem validação correspondente no backend, permitindo que usuários manipulem o estado para ver interfaces proibidas.

### 3. Headers de Segurança, Dependências e Recursos Externos
- [ ] **Content Security Policy (CSP):** Verifique se o frontend define ou possui suporte a CSP restritivo para mitigar a execução de scripts inline e fontes externas não autorizadas.
- [ ] **Subresource Integrity (SRI):** Identifique scripts externos ou estilos carregados via CDNs de terceiros (`<script src="https://...">`) sem os atributos `integrity` e `crossorigin`.
- [ ] **Reverse Tabnabbing:** Verifique se tags `<a target="_blank">` possuem o atributo `rel="noopener noreferrer"` para impedir manipulação da página de origem (`window.opener`).

### 4. Performance, Bundle Size e Boas Práticas (Core Web Vitals)
- [ ] **Lazy Loading & Code Splitting:** Identifique ausência de carregamento dinâmico (`dynamic import`, `React.lazy`) em rotas pesadas ou bibliotecas volumosas (ex: Moment.js, Lodash inteiro, bibliotecas de gráficos importadas globalmente).
- [ ] **Vazamento de Memória no DOM:** Localize listeners de eventos (`window.addEventListener`), *intervals* (`setInterval`) ou *subscriptions* (RxJS) não cancelados no ciclo de desmontagem dos componentes (`useEffect cleanup`, `ngOnDestroy`, `onUnmounted`).
- [ ] **Exposição de Dados Sensíveis e PII:** Verifique se formulários desabilitam o preenchimento automático para campos críticos (`autocomplete="off"` / `"new-password"`) e se o código não executa `console.log()` com payloads sensíveis em produção.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `src/components/UserBio.tsx:34` | Segurança (XSS) | CRÍTICA | Baixo (15 min) | **SIM** |
| #2 | `src/utils/auth.ts:12` | Sessão (Storage) | ALTA | Médio (2 hrs) | NÃO |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome do Problema]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Categoria:** [XSS e Injeção / Armazenamento e Sessão / Headers e CDN / Performance e Memória / Vazamento de Segredos]
- **Problema:** Explicação direta do risco real em ambiente de produção para o usuário final.
- **Evidência:** Trecho do código-fonte atual identificado no repositório.
- **Correção Recomendada:** Código devidamente corrigido e refatorado aplicando as melhores práticas.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/frontend-audit/relatorio-auditoria-frontend.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Frontend e SPAs — <nome do projeto>", data, escopo auditado e nota metodológica (como cada categoria foi mapeada para a stack detectada).
b) **Resumo Executivo:** Total de achados por severidade, gráfico de rosca por severidade e gráfico de barras por categoria.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (o que está protegido no client-side, com evidência) e **Pontos Fracos** (os riscos centrais).
d) **Tabela de Achados Detalhados por Categoria:** Severidade | Arquivo:linha | Descrição, com indicação/chip de severidade e tag de Quick Win.
e) **Recomendações Priorizadas** (P1, P2, P3...).
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada achado acionável, o texto COMPLETO de uma issue em Markdown, pronto para copiar e colar, dentro de um bloco delimitado (ex: entre `--- ISSUE n ---` e `--- FIM ISSUE n ---`). Cada issue deve conter:
   - Título no formato `[Frontend/Segurança] <descrição curta da falha>`
   - Labels sugeridas: `frontend` + `security` ou `performance` + severidade
   - Descrição do problema e por que é explorável / degrada a experiência
   - Evidência: `arquivo:linha` com trecho de código
   - Impacto
   - Sugestão de correção
   - Critérios de aceite (checklist verificável)
   *(Nota: Agrupe achados triviais relacionados numa issue única quando fizer sentido para evitar spam).*

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Não instale pacotes globalmente no sistema. Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`, ou ferramentas equivalentes locais como `puppeteer`/HTML-to-PDF).
- Deixe o script gerador salvo no diretório `docs/frontend-audit/` para que o relatório possa ser regerado futuramente.
- Verifique o PDF gerado: garanta o número correto de páginas, a renderização adequada dos gráficos e a legibilidade das tabelas.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/frontend-audit/relatorio-auditoria-frontend.pdf`, `docs/frontend-audit/generate_report.py`).