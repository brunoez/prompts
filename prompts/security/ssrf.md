# PROMPT DE AUDITORIA COMPLETA: SERVER-SIDE REQUEST FORGERY (SSRF) — OWASP PROACTIVE CONTROL C10, OWASP ASVS v4.0.3 & OWASP RISK RATING METHODOLOGY E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de AppSec e Especialista em Segurança de Rede de Aplicação (Yellow/Red Team). Sua missão é realizar uma varredura completa no repositório aplicando o **OWASP Top 10 Proactive Controls 2024 — C10: Stop Server Side Request Forgery**, as diretrizes do **OWASP SSRF Prevention Cheat Sheet**, os testes do **OWASP WSTG v4.2** (*WSTG-INPV-19*), a categoria **A10:2021 — SSRF** e os requisitos normativos do **OWASP Application Security Verification Standard (OWASP ASVS v4.0.3)** (Capítulo V12 - File and Resources - V12.6 SSRF Protection e Capítulo V5 - Validation, Sanitization and Encoding Verification Requirements).

A severidade de cada vulnerabilidade identificada deve ser formalmente mensurada aplicando o **OWASP Risk Rating Methodology**, combinando a Probabilidade (*Likelihood*) com o Impacto (*Impact*) em uma matriz determinística 3x3.

A auditoria deve identificar todo ponto onde o servidor faz requisições de saída (HTTP, DNS, TCP, arquivos) para destinos que o cliente pode influenciar — webhooks, importadores de URL, proxies de imagem, geradores de PDF/thumbnail, integrações, fetch de metadados de link, parsers de XML/SVG — e verificar as defesas contra acesso a rede interna, endpoints de metadata de nuvem e serviços locais.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura completa de diretórios e identifique a stack e os clientes HTTP usados (`fetch`, `axios`, `got`, `undici`, `node-fetch`, `requests`, `httpx`, `urllib`, `net/http` Go, `HttpClient` Java/.NET, `curl` em subprocesso).
2. Identifique e analise TODOS os pontos de saída influenciáveis pelo cliente:
   - Endpoints que recebem uma URL/host/IP no body, query, header ou webhook config (`callbackUrl`, `imageUrl`, `avatar_url`, `webhook`, `redirect_to`, `source`, `target`, `url`).
   - Renderizadores/conversores: HTML→PDF (`wkhtmltopdf`, Puppeteer, WeasyPrint), thumbnail de imagem/vídeo, preview de link (Open Graph), importação de feed/RSS/CSV remoto.
   - Parsers que resolvem entidades externas: XML (XXE→SSRF), SVG, `<img>`/`<link>` em e-mail, bibliotecas de OpenAPI/JSON-Schema que fazem `$ref` remoto.
   - Proxies genéricos, health-checkers, e integrações "conecte sua conta" (OAuth de terceiros com endpoint configurável).
3. Identifique a topologia de rede: a aplicação roda em nuvem (AWS/GCP/Azure) com endpoint de metadata (`169.254.169.254`, `metadata.google.internal`)? Há serviços internos sem autenticação (Redis, Elasticsearch, Kubernetes API, bancos, painéis admin)?
4. Você DEVE ler e analisar cada arquivo identificado linha por linha. Não faça suposições sem validar o código-fonte correspondente.
5. **Diretriz Anti-Fadiga e Anti-Alucinação (Filtro Factual):** Só reporte SSRF categoricamente comprovado por um caminho de dados do input do cliente até uma requisição de saída. É proibido levantar hipóteses sem evidência no repositório. Achados sem controlabilidade real do destino devem ser marcados como `[NIT]` ou descartados, com foco no *Blast Radius* (o que a rede interna expõe).

---

## CHECKLIST DE AUDITORIA PRÁTICA (OWASP PROACTIVE C10, CHEAT SHEET & OWASP ASVS v4.0.3)

### 1. Identificação da Superfície e Controlabilidade (ASVS V12.6, V5.1)
- [ ] **Rastreio de Fonte→Sink & ASVS V12.6.1 (L1):** Para cada cliente HTTP, rastreie se a URL, host, porta ou path derivam (mesmo parcialmente) de input do usuário sem *allow-list*. Concatenar um domínio fixo com path do usuário ainda pode ser abusável (`https://api.interno/` + `../../` ou `@evil.com`).
- [ ] **Parâmetros Ocultos & ASVS V12.6.1, V5.1.1 (L2):** Verifique headers como `X-Forwarded-Host`, `Host`, `Referer` usados para montar URLs de callback/absolute links.
- [ ] **Redirecionamentos Seguidos & ASVS V12.6.1 (L2):** Verifique se o cliente HTTP segue redirects automaticamente (`maxRedirects`) — um destino permitido pode responder `302` para `http://169.254.169.254/`. A validação deve reexecutar a cada salto ou os redirects devem ser desabilitados.

### 2. Defesa Primária — Allow-List (Cheat Sheet: "Application Layer" & ASVS V12.6.1)
- [ ] **Allow-List de Destino, não Deny-List & ASVS V12.6.1 (L1):** Verifique se destinos permitidos são um conjunto fechado de domínios/hosts/portas esperados (ex: só `api.stripe.com:443`). Deny-list de `localhost`/`127.0.0.1` é insuficiente (bypass via `0.0.0.0`, `[::1]`, `2130706433`, `127.1`, `0x7f.1`, DNS rebinding, domínios que resolvem para IP interno).
- [ ] **Validação Pós-Resolução DNS & ASVS V12.6.1 (L2):** Verifique se, após resolver o hostname, o IP resultante é checado contra faixas privadas/reservadas **e** se a conexão é fixada (*pinned*) a esse IP validado para impedir **DNS rebinding** (TOCTOU entre validação e request).
- [ ] **Bloqueio de Faixas Não-Roteáveis & ASVS V12.6.1 (L1):** Verifique bloqueio de `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16` (link-local + metadata), `::1/128`, `fc00::/7`, `fe80::/10`, `100.64.0.0/10` (CGNAT) e `0.0.0.0/8`.
- [ ] **Esquema e Porta & ASVS V12.6.1, V5.1.1 (L1):** Verifique que só `https` (ou `http` quando estritamente necessário) é aceito — bloquear `file://`, `gopher://`, `dict://`, `ftp://`, `ldap://`, `data://`. Restringir portas ao esperado (443/80).
- [ ] **Sem Credenciais/Fragmento Enganosos & ASVS V12.6.1, V5.1.4 (L2):** Verifique parsing robusto que rejeita `https://allowed.com@attacker.com`, `https://attacker.com#allowed.com`, unicode/punycode e barras/backslashes ambíguas.

### 3. Defesa em Profundidade — Rede e Ambiente (Cheat Sheet: "Network Layer" & ASVS V1.14, V14.4)
- [ ] **Egress Filtering & ASVS V1.14.2, V14.4.1 (L2):** Verifique se há política de saída (Security Group / NetworkPolicy / firewall / proxy forward obrigatório) restringindo para onde os pods/hosts da aplicação podem abrir conexão.
- [ ] **Metadata de Nuvem Protegida & ASVS V14.4.1 (L2):** AWS — IMDSv2 obrigatório (`HttpTokens: required`, hop limit 1) ou IMDS desabilitado; GCP/Azure — cabeçalho `Metadata-Flavor`/rota bloqueada no nível de rede quando não usada.
- [ ] **Isolamento do Componente Fetcher & ASVS V1.14.3 (L2):** Renderizadores de PDF/imagem e proxies rodam em rede segregada, sem acesso a serviços internos, idealmente sem rota para a VPC.
- [ ] **Serviços Internos Autenticados & ASVS V2.1.1, V4.1.1 (L2):** Verifique que Redis, Elasticsearch, bancos, API do Kubernetes e dashboards internos exigem autenticação — SSRF não deve virar RCE/leak por atingir serviço interno aberto.

### 4. Tratamento da Resposta e Vazamento (ASVS V12.6.1, V7.2)
- [ ] **Não Refletir a Resposta Crua & ASVS V12.6.1, V7.2.1 (L2):** Verifique que corpo, headers, status e tempo da resposta da requisição de saída não são devolvidos ao cliente de forma que permita exfiltrar conteúdo interno (*blind vs full-read SSRF*).
- [ ] **Timeout e Limite de Tamanho & ASVS V13.2.3 (L2):** Verifique timeout curto de conexão/leitura e limite máximo de bytes lidos para evitar DoS e leitura de respostas grandes de serviços internos.
- [ ] **Mensagens de Erro & ASVS V7.2.1 (L1):** Verifique que erros de conexão (`ECONNREFUSED` vs `timeout` vs `200`) não são repassados ao cliente, servindo de oráculo de varredura de porta interna.

### 5. Vetores Específicos (ASVS V5.5, V12.1)
- [ ] **XXE → SSRF & ASVS V5.5.3 (L2):** Parsers de XML/SVG/DOCX/SVG com resolução de entidade externa e `DOCTYPE` habilitados.
- [ ] **`$ref` Remoto & ASVS V5.5.1, V12.6.1 (L2):** Bibliotecas de OpenAPI/JSON-Schema/GraphQL SDL que dereferenciam `$ref: "http://..."` durante o carregamento.
- [ ] **Webhooks de Saída & ASVS V12.6.1, V13.2.5 (L2):** Endpoints onde o usuário cadastra a URL de webhook — aplicar allow-list, assinatura HMAC e bloqueio de rede interna; permitir opt-out de retries que amplificam.
- [ ] **PDF/Screenshot Services & ASVS V12.1.1, V12.6.1 (L2):** HTML controlado pelo usuário renderizado server-side com `<img src>`, `<iframe>`, `@import`, `<link>` apontando para rede interna.

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
| #1 | `src/services/pdf.ts:22` | HTML→PDF SSRF / ASVS V12.6.1 (L1) | ALTA | ALTO | CRÍTICA | Médio (3 hrs) | NÃO |
| #2 | `src/routes/webhook.ts:14` | Webhook URL / ASVS V12.6.1 (L1) | ALTA | ALTO | CRÍTICA | Baixo (40 min) | **SIM** |
| #3 | `src/lib/http.ts:9` | Redirects / ASVS V12.6.1 (L2) | ALTA | MÉDIO | ALTA | Baixo (30 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item da tabela:
- **Achado #[ID]:** [Nome do Problema]
- **Controle / Cheat Sheet:** [ex: Proactive C10 / SSRF Prevention Cheat Sheet / WSTG-INPV-19 / A10:2021]
- **OWASP ASVS v4.0.3:** [Capítulo e Requisito, ex: V12.6.1 (Level 1 - SSRF Protections)]
- **Avaliação de Risco (OWASP Risk Rating Methodology):**
  - *Probabilidade (Likelihood):* [BAIXA | MÉDIA | ALTA] (Agente de Ameaça + Facilidade de Descoberta/Exploração)
  - *Impacto Técnico (Tech Impact):* [BAIXO | MÉDIO | ALTO] (Confidencialidade, Integridade, Disponibilidade)
  - *Impacto de Negócio (Business Impact):* [BAIXO | MÉDIO | ALTO] (Danos Financeiros, LGPD/GDPR, Reputação)
  - *Severidade Calculada:* [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/arquivo.ext:linha`
- **Vetor de Ataque / Exploração:** Payload concreto (ex: `imageUrl=http://169.254.169.254/latest/meta-data/iam/security-credentials/`, DNS rebinding, `@`-bypass).
- **Evidência:** Trecho do código-fonte vulnerável (fonte→sink).
- **Prova de Conceito (PoC / Reprodução):** Requisição reproduzível (`curl`) e o que o atacante obtém (credenciais IMDS, varredura de porta interna, leitura de serviço interno).
- **Correção Recomendada:** Código refatorado com allow-list, validação pós-DNS + pinning, redirects desabilitados e egress filtering.
- **Comando de Verificação da Correção:** Como validar em 1 comando (teste que envia URL interna e espera rejeição `400`/`403`).

---

## GERAÇÃO DE RELATÓRIO PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script automatizado salvo em `docs/ssrf-audit/generate_report.py` para produzir:

1. **Relatório em PDF (`docs/ssrf-audit/relatorio-auditoria-ssrf.pdf`):**
   - **Capa:** Título "Relatório de Auditoria de SSRF & ASVS (OWASP Proactive C10) — <nome do projeto>", data e escopo.
   - **Resumo Executivo:** Gráfico de rosca por severidade, gráfico de barras por categoria e Matriz de Calor 3x3 do OWASP Risk Rating Methodology (Likelihood × Impact).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
   - **Mapa de Superfície SSRF & ASVS:** Tabela de cada sink de saída, fonte do destino, controlabilidade e conformidade ASVS V12.6 e V5 (L1/L2/L3).
   - **Tabela Detalhada de Achados** com tags de Quick Win, notas de risco RRM e referências a arquivos e linhas.

2. **Seção "ISSUES PARA O GITHUB" no Relatório:**
   - Template Markdown completo pronto para copiar e colar para cada achado, com labels, passos de reprodução, avaliação de risco formal (RRM: Probabilidade x Impacto), impacto e critérios de aceite.

### REGRAS TÉCNICAS
- Use ambiente Python isolado (`venv` temporário com `reportlab` e `matplotlib`).
- Salve o script e os artefatos em `docs/ssrf-audit/`.
- Garanta formatação A4 impecável, paginação correta e sem quebras visuais em tabelas.

---

## ENTREGÁVEIS FINAIS
Ao concluir, informe no chat:
1. A confirmação da geração do relatório PDF.
2. A lista de achados (Parte 1 e Parte 2).
3. O caminho relativo dos arquivos gerados (`docs/ssrf-audit/relatorio-auditoria-ssrf.pdf`, `docs/ssrf-audit/generate_report.py`).
