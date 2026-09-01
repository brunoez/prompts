# PROMPT DE AUDITORIA COMPLETA: SOFTWARE SUPPLY CHAIN, GESTÃO DE DEPENDÊNCIAS (SCA), PREVENÇÃO DE ALUCINAÇÃO E GERAÇÃO DE RELATÓRIO PDF

## OBJETIVO
Atuar como Engenheiro Principal de Segurança em Supply Chain e Especialista em DevSecOps (Yellow Team / AppSec). Sua missão é realizar uma varredura rigorosa no repositório para garantir a integridade da cadeia de suprimentos de software (**Software Supply Chain Security**). O foco principal é prevenir ataques de injeção de dependências (*Dependency Confusion*), **alucinações de pacotes por IA (*Slopsquatting / Package Hallucination*)**, pacotes maliciosos com scripts de `postinstall`, manipulação de lockfiles (*Lockfile Injection*), vulnerabilidades conhecidas em dependências diretas/transitivas (SCA / CVEs) e licenças incompatíveis.

Ao final da auditoria, você deve listar os achados no chat/terminal e gerar um relatório completo em formato PDF e templates de Issues em Markdown para o GitHub.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. Mapeie a estrutura de dependências do projeto em todos os ecossistemas presentes:
   - **Node.js/JavaScript/TypeScript:** `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `.npmrc`.
   - **Python:** `pyproject.toml`, `requirements.txt`, `Pipfile`, `poetry.lock`, `setup.py`, `pip.conf`.
   - **Go:** `go.mod`, `go.sum`.
   - **Rust:** `Cargo.toml`, `Cargo.lock`.
   - **Java/Kotlin:** `pom.xml`, `build.gradle`, `build.gradle.kts`.
   - **PHP/Ruby/C#:** `composer.json`, `Gemfile`, `*.csproj`, `packages.config`.
2. Identifique e analise TODOS os pacotes declarados, tanto em `dependencies` quanto em `devDependencies`.
3. Você DEVE ler e analisar os arquivos de manifesto e lockfiles linha por linha.

---

## CHECKLIST DE VALIDAÇÃO PRÁTICA (SUPPLY CHAIN & SCA)

### 1. Detecção de Alucinação de Pacotes por IA & Slopsquatting (Vibe Coding Defense)
- [ ] **Validação de Existência Real de Pacotes:** Identifique se há dependências declaradas que possuem nomes incomuns, erros de digitação (*Typosquatting*) ou que parecem invenções de LLMs que não possuem histórico público no npm, PyPI, crates.io ou Maven Central.
- [ ] **Idade e Reputação do Pacote:** Alerte sobre pacotes criados recentemente (< 30 dias), com pouquíssimos downloads, sem repositório de código público linkado ou mantidos por autores desconhecidos.
- [ ] **Namespace e Dependency Confusion:** Identifique pacotes internos/privados da organização que não utilizam escopo protegido (ex: `@minha-empresa/pacote`) e que poderiam ser sequestrados no registro público oficial.

### 2. Integridade de Lockfiles e Resolução de Dependências
- [ ] **Presença e Atualização do Lockfile:** Verifique se os arquivos de lock (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`) estão versionados no repositório e sincronizados com os manifestos principais.
- [ ] **Prevenção de Versões Flutuantes Agressivas:** Identifique dependências críticas usando curingas muito abertos (ex: `*`, `^`, `>=`) sem travas de versão estável para bibliotecas de segurança e criptografia.
- [ ] **Auditoria de Registries e Configurações de Download:** Verifique se `.npmrc` ou `pip.conf` apontam para registries não confiáveis ou configuram conexões HTTP sem TLS (`http://`).

### 3. Scripts de Ciclo de Vida e Execução Arbitrária de Código
- [ ] **Scripts de Build e Postinstall Maliciosos:** Verifique se as dependências instaladas executam scripts arbitrários no momento da instalação (`preinstall`, `install`, `postinstall`, `setup.py`) sem justificativa técnica clara.
- [ ] **Bloqueio de Scripts na Instalação:** Verifique se a esteira de CI/CD e ambientes de desenvolvimento utilizam flags de proteção (ex: `npm install --ignore-scripts` quando viável, ou `pnpm` com whitelist de scripts).

### 4. Vulnerabilidades Conhecidas (SCA / CVEs) e Licenciamento
- [ ] **Varredura de CVEs (Vulnerabilidades Críticas e Altas):** Identifique dependências com vulnerabilidades públicas registradas (via `npm audit`, `pip-audit`, `osv-scanner`, `trivy`) com foco em Execução Remota de Código (RCE), Prototype Pollution e Negação de Serviço (DoS).
- [ ] **Dependências Obsoletas ou Abandonadas:** Localize bibliotecas que não recebem atualizações há mais de 2 anos ou foram arquivadas oficialmente pelos autores.
- [ ] **Conformidade de Licenças de Código Aberto:** Identifique pacotes com licenças restritivas (ex: AGPL-3.0, GPL-3.0) em projetos proprietários fechados que possam exigir a abertura do código-fonte.
- [ ] **Geração de SBOM (Software Bill of Materials):** Verifique se o projeto gera arquivos CycloneDX ou SPDX para inventário completo de software.

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a análise técnica no código, exiba no chat a lista detalhada de achados (arquivo por arquivo, linha por linha), ordenada por prioridade:

### PARTE 1: MATRIZ DE PRIORIZAÇÃO E QUICK WINS
Apresente uma tabela inicial contendo TODOS os achados encontrados, ordenados obrigatoriamente do maior risco/facilidade para o menor:

| ID | Arquivo / Ponto | Categoria | Severidade | Esforço Estimado | Quick Win? |
|---|---|---|---|---|---|
| #1 | `package.json:28` | Pacote Alucinado / Suspeito | CRÍTICA | Baixo (10 min) | **SIM** |
| #2 | `package-lock.json` | CVE Crítica em Dependência Transitiva | ALTA | Baixo (15 min) | **SIM** |

*(Quick Win: Problema de Severidade ALTA ou MÉDIA com Esforço de Correção BAIXO).*

### PARTE 2: DETALHAMENTO COMPLETO DOS ACHADOS
Para CADA item listado na tabela, forneça a análise completa:
- **Achado #[ID]:** [Nome da Dependência / Vulnerabilidade]
- **Severidade:** [CRÍTICA | ALTA | MÉDIA | BAIXA]
- **Esforço de Correção:** [BAIXO | MÉDIO | ALTO]
- **Tag:** [QUICK WIN] *(se aplicável)*
- **Arquivo/Linha:** `caminho/do/manifesto.ext:linha`
- **Categoria:** [Package Hallucination / Dependency Confusion / CVE / Malicious Script / Lockfile Drift / License Risk]
- **Problema:** Explicação direta do risco de Supply Chain introduzido no projeto.
- **Evidência:** Declaração da dependência no manifesto ou lockfile.
- **Correção Recomendada:** Remoção do pacote alucinado, fixação de versão corrigida ou substituto oficial confiável.

---

## GERAÇÃO DO RELATÓRIO EM PDF E ISSUES

DEPOIS DA AUDITORIA, crie e execute um script para gerar um RELATÓRIO EM PDF, visualmente amigável, em pt-BR, salvo em `docs/supply-chain-audit/relatorio-auditoria-supply-chain.pdf`, contendo:

a) **Capa:** Título "Relatório de Auditoria de Supply Chain e Gestão de Dependências — <nome do projeto>", data, ecossistemas analisados e metodologia de SCA.
b) **Resumo Executivo:** Total de dependências auditadas, total de vulnerabilidades por severidade, gráfico de rosca de severidade e gráfico de barras por categoria de risco.
   - **Paleta oficial:** Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
c) **Pontos Fortes** (lockfiles consistentes, dependências auditadas) e **Pontos Fracos** (pacotes desatualizados ou sem travas de versão).
d) **Tabela de Achados Detalhados:** Severidade | Pacote:Versão | Vulnerabilidade/CVE/Risco | Correção.
e) **Inventário de Dependências Críticas (Resumo do SBOM).**
f) **Seção Final "ISSUES PARA O GITHUB":** Para cada dependência vulnerável ou alucinada, a issue formatada com os comandos de atualização ou substituição recomendados.

### REGRAS TÉCNICAS PARA GERAÇÃO DO PDF
- Use um ambiente isolado (ex: `venv` Python com `reportlab` + `matplotlib`).
- Deixe o script gerador salvo no diretório `docs/supply-chain-audit/`.
- Formatação das páginas: tamanho A4, margens de aproximadamente 2cm, cabeçalho e rodapé contendo o nome do relatório e a numeração de páginas.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. A confirmação de geração do relatório em PDF.
2. A lista de achados no chat (Parte 1 e Parte 2).
3. O caminho relativo de todos os arquivos gerados (ex: `docs/supply-chain-audit/relatorio-auditoria-supply-chain.pdf`, `docs/supply-chain-audit/generate_report.py`).
