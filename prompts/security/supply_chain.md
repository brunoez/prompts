# PROMPT DE AUDITORIA COMPLETA: SOFTWARE SUPPLY CHAIN, GESTÃO DE DEPENDÊNCIAS (SCA/SBOM), OWASP SCVS, OWASP ASVS v4.0.3 & OWASP RISK RATING METHODOLOGY E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Segurança em Supply Chain e Especialista em DevSecOps (Supply Chain & SCA Lead). Sua missão é realizar uma varredura rigorosa no repositório para garantir a integridade da cadeia de suprimentos de software (**Software Supply Chain Security**), aplicando as diretrizes do **OWASP Software Component Verification Standard (SCVS)**, do **OWASP Vulnerable Dependency Management Cheat Sheet Series** e os requisitos normativos do **OWASP Application Security Verification Standard (OWASP ASVS v4.0.3)** (Capítulo V10 - Malicious Code e Capítulo V14 - Configuration Verification Requirements - V14.2 Third-Party Components).

A severidade de cada vulnerabilidade identificada deve ser formalmente mensurada aplicando o **OWASP Risk Rating Methodology**, combinando a Probabilidade (*Likelihood*) com o Impacto (*Impact*) em uma matriz determinística 3x3.

A auditoria foca na prevenção contra ataques de injeção de dependências (*Dependency Confusion*), **alucinações de pacotes por IA (*Slopsquatting / Package Hallucination*)**, pacotes maliciosos com scripts de ciclo de vida (`preinstall`/`postinstall`), manipulação de lockfiles (*Lockfile Injection / Drift*), geração e conformidade de **SBOM (CycloneDX/SPDX)**, vulnerabilidades conhecidas em dependências transitivas (SCA / CVEs), licenças incompatíveis e assinatura de proveniência (SLSA / Sigstore).

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura de dependências do projeto em todos os ecossistemas presentes:
   - **Node.js/JavaScript/TypeScript:** `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `.npmrc`.
   - **Python:** `pyproject.toml`, `requirements.txt`, `Pipfile`, `poetry.lock`, `setup.py`, `pip.conf`.
   - **Go:** `go.mod`, `go.sum`.
   - **Rust:** `Cargo.toml`, `Cargo.lock`.
   - **Java/Kotlin:** `pom.xml`, `build.gradle`, `build.gradle.kts`, `gradle.lockfile`.
   - **PHP/Ruby/C#:** `composer.json`, `Gemfile`, `*.csproj`, `packages.config`.
2. Identifique e analise TODOS os pacotes declarados, tanto em `dependencies` quanto em `devDependencies`/`build-dependencies`.
3. Você DEVE ler e analisar os arquivos de manifesto e lockfiles linha por linha.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (OWASP SCVS, SUPPLY CHAIN & OWASP ASVS v4.0.3)

### 1. Detecção de Alucinação de Pacotes por IA & Slopsquatting (Vibe Coding Defense & ASVS V10.2, V14.2)
- [ ] **Validação de Existência Real de Pacotes & ASVS V10.2.1, V14.2.1 (L1):** Identifique se há dependências declaradas que possuem nomes incomuns, erros de digitação (*Typosquatting*) ou que parecem invenções de LLMs que não possuem histórico público no npm, PyPI, crates.io ou Maven Central.
- [ ] **Idade, Reputação e Saúde do Pacote & ASVS V10.2.2 (L2):** Alerte sobre pacotes criados recentemente (< 30 dias), com contagem ínfima de downloads, sem repositório de código público linkado ou mantidos por autores anônimos.
- [ ] **Namespace e Dependency Confusion & ASVS V14.2.2 (L2):** Identifique pacotes internos/privados da organização que não utilizam escopo protegido (ex: `@minha-empresa/pacote`) e que poderiam ser sequestrados no registro público oficial por atacantes externos.

### 2. Integridade de Lockfiles, Registries e Builds Determinísticos (OWASP SCVS Level 2 & ASVS V10.3, V14.2)
- [ ] **Presença e Sincronismo Obrigatório de Lockfiles & ASVS V10.3.2, V14.2.3 (L1):** Verifique se os arquivos de lock (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`) estão versionados no repositório e estritamente sincronizados com os manifestos principais (impedindo desvios em tempo de build).
- [ ] **Prevenção de Versões Flutuantes Agressivas & ASVS V14.2.1 (L2):** Identifique dependências críticas usando curingas muito abertos (ex: `*`, `^`, `>=`) sem travas de versão estável para bibliotecas de segurança, autenticação e criptografia.
- [ ] **Auditoria de Registries e Protocolos Seguros & ASVS V9.1.1, V14.2.2 (L1):** Verifique se `.npmrc` ou `pip.conf` apontam para registries corporativos autenticados e se bloqueiam conexões HTTP sem TLS (`http://`).

### 3. Scripts de Ciclo de Vida e Execução Arbitrária de Código (ASVS V10.2, V10.3)
- [ ] **Scripts de Build e Postinstall Maliciosos & ASVS V10.2.1, V10.3.1 (L2):** Verifique se as dependências instaladas executam scripts arbitrários no momento da instalação (`preinstall`, `install`, `postinstall`, `setup.py`, `build.rs`) sem justificativa técnica clara.
- [ ] **Bloqueio de Scripts na Instalação em CI/CD & ASVS V10.3.3 (L2):** Verifique se a esteira de CI/CD e ambientes de desenvolvimento utilizam flags de proteção (ex: `npm ci --ignore-scripts`, ou `pnpm` com whitelist de scripts autorizados).

### 4. Vulnerabilidades Conhecidas (SCA / CVEs), SBOM e Licenças (ASVS V14.2)
- [ ] **Varredura de CVEs (Vulnerabilidades Críticas e Altas) & ASVS V14.2.1 (L1):** Identifique dependências com vulnerabilidades públicas registradas (via `npm audit`, `pip-audit`, `osv-scanner`, `trivy`, `snyk`) com foco em Execução Remota de Código (RCE), Prototype Pollution, SQLi e Negação de Serviço (DoS).
- [ ] **Geração e Conformidade de SBOM (Software Bill of Materials) & ASVS V14.2.5 (L2):** Verifique se o projeto possui automação para gerar arquivos de SBOM padronizados (em formato **CycloneDX** ou **SPDX**) para inventário completo de software e auditoria de terceiros.
- [ ] **Dependências Obsoletas ou Abandonadas & ASVS V14.2.4 (L2):** Localize bibliotecas que não recebem atualizações há mais de 2 anos ou foram arquivadas oficialmente pelos mantenedores.
- [ ] **Conformidade de Licenças de Código Aberto & ASVS V14.2.6 (L3):** Identifique pacotes com licenças restritivas (ex: AGPL-3.0, GPL-3.0, SSPL) em projetos proprietários fechados que possam exigir a abertura indesejada do código-fonte corporativo.

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
| #1 | `package.json:28` | Pacote Alucinado / ASVS V10.2.1 (L1) | ALTA | ALTO | CRÍTICA | Baixo (10 min) | **SIM** |
| #2 | `package-lock.json` | CVE em Dependência / ASVS V14.2.1 (L1) | ALTA | ALTO | CRÍTICA | Baixo (15 min) | **SIM** |
| #3 | `.npmrc:5` | Dependency Confusion / ASVS V14.2.2 (L2) | MÉDIA | ALTO | ALTA | Baixo (20 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou CRÍTICA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome da Dependência / Vulnerabilidade]
- **Categoria / Padrão:** [Package Hallucination / Dependency Confusion / CVE / Malicious Script / Lockfile Drift / License Risk / SBOM]
- **OWASP ASVS v4.0.3:** [Capítulo e Requisito, ex: V14.2.1 (Level 1 - Third-Party Components Verification)]
- **Avaliação de Risco (OWASP Risk Rating Methodology):**
  - *Probabilidade (Likelihood):* [BAIXA | MÉDIA | ALTA] (Agente de Ameaça + Facilidade de Descoberta/Exploração)
  - *Impacto Técnico (Tech Impact):* [BAIXO | MÉDIO | ALTO] (Confidencialidade, Integridade, Disponibilidade)
  - *Impacto de Negócio (Business Impact):* [BAIXO | MÉDIO | ALTO] (Danos Financeiros, LGPD/GDPR, Reputação)
  - *Severidade Calculada:* [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/manifesto.ext:linha`
- **Vetor de Risco / Exploração:** Explicação direta de como o pacote vulnerável ou alucinado pode ser explorado em produção ou na máquina do desenvolvedor.
- **Evidência:** Declaração da dependência no manifesto ou lockfile.
- **Correção Recomendada:** Remoção do pacote alucinado, fixação de versão corrigida ou substituto oficial confiável.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/supply-chain-audit/relatorio-auditoria-supply-chain.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Supply Chain, Gestão de Dependências & ASVS (OWASP SCVS) — <nome do projeto>", data, ecossistemas analisados e metodologia de SCA.
b) **Resumo Executivo:** Total de dependências auditadas, total de vulnerabilidades por severidade, gráfico de rosca de severidade, gráfico de barras por categoria de risco e Matriz de Calor 3x3 do OWASP Risk Rating Methodology (Likelihood × Impact).
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (lockfiles consistentes, dependências auditadas) e **Pontos Fracos** (pacotes desatualizados ou sem travas de versão).
d) **Matriz de Conformidade OWASP SCVS & ASVS:** Tabela indicando conformidade para inventário, lockfiles, scripts, CVEs e capítulos ASVS V10 e V14 (L1/L2/L3).
e) **Tabela de Achados Detalhados:** Severidade | Pacote:Versão | Vulnerabilidade/CVE/Risco | Correção | Nota RRM.
f) **Inventário de Dependências Críticas (Resumo do SBOM).**
g) **Seção Final "ISSUES PARA O GITHUB":** Para cada dependência vulnerável ou alucinada, a issue formatada com os comandos de atualização ou substituição recomendados e avaliação formal de risco (RRM: Probabilidade x Impacto).

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (`venv` Python com `reportlab` + `matplotlib`).
- Salve o script gerador em `docs/supply-chain-audit/generate_report.py`.
- Formatação das páginas: tamanho A4, margens de 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS
Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/supply-chain-audit/relatorio-auditoria-supply-chain.pdf`, `docs/supply-chain-audit/generate_report.py`).
