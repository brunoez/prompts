# PROMPT DE CONFIGURAÇÃO DE CONTEXTO, DICIONÁRIO DO PROJETO E REGRAS PARA IAs (CONTEXT.md, CLAUDE.md, CURSOR, COPILOT)

## OBJETIVO
Atuar como Engenheiro Principal de Contexto e Arquitetura de Software. Sua missão é realizar uma varredura completa no repositório para mapear o vocabulário do negócio, os termos técnicos e os padrões de desenvolvimento, gerando de forma automatizada os **arquivos de contexto e diretrizes para IAs e Agentes de Código** (**`CONTEXT.md`**, **`CLAUDE.md`**, **`.cursorrules`**, **`.github/copilot-instructions.md`** e **`.agent/rules/`**).

O objetivo principal é eliminar a prolixidade da IA, evitar alucinações de termos inexistentes e garantir que qualquer modelo (Claude, GPT, Gemini, Cursor, Copilot) entenda perfeitamente o jargão da empresa, os comandos de execução e as regras de arquitetura do projeto.

---

## ESCOPO E OBRIGATORIEDADE DE LEITURA
1. **Leitura de Domínio e Negócio:** Analise o `README.md`, documentações em `docs/`, nomes de entidades, tabelas de banco de dados, enums e serviços para extrair os termos e conceitos centrais do negócio.
2. **Leitura de Stack e Scripts:** Leia os manifestos (`package.json`, `pyproject.toml`, `go.mod`, `Makefile`, `Dockerfile`) para identificar comandos de build, testes, linters e inicialização.
3. **Leitura de Padrões e Arquitetura:** Identifique as convenções de pastas (`src/`, `modules/`, `domain/`), padrões de tratamento de erro, autenticação e bibliotecas preferenciais.

---

## ARQUIVOS GERADOS AUTOMATICAMENTE

O prompt deve criar ou atualizar os seguintes arquivos conforme as ferramentas utilizadas no projeto:

### 1. 📖 `CONTEXT.md` (Dicionário de Negócio e Glossário do Projeto)
Arquivo universal lido por qualquer IA para entender o vocabulário da aplicação. Deve conter:
* **Glossário do Negócio:** Termos específicos do sistema explicados em 1 ou 2 frases (ex: *"Materialization Cascade: processo de persistência em lote de módulos no disco"*).
* **Entidades Centrais:** O que cada entidade representa e como se relacionam.
* **Invariantes do Sistema:** Regras de negócio que NUNCA podem ser violadas (ex: *"Um pedido nunca pode ser cancelado se o status for ENVIADO"*).
* **Dicionário De-Para:** Como a IA deve se referir aos conceitos (eliminando termos genéricos e prolixos).

### 2. 🤖 `CLAUDE.md` (Diretrizes para o Claude Code / Anthropic)
Arquivo de instruções específico para o Claude Code na raiz do projeto contendo:
* **Comandos Principais:** Como rodar testes, linters, builds e servidor local com comandos únicos e diretos.
* **Estilo de Código:** Regras de formatação, tipagem estrita e padrões de imports.
* **Estrutura de Pastas:** Mapa mental simplificado das camadas do projeto.

### 3. 🎯 `.cursorrules` ou `.cursor/rules/` (Diretrizes para o Cursor)
Regras concisas para orientar o preenchimento automático e geração de código no Cursor:
* Preferência de bibliotecas (ex: *"Sempre use Zod para validação e Tailwind para estilos"*).
* Padrões proibidos (ex: *"Nunca use `any` ou `console.log` em produção"*).

### 4. 🐙 `.github/copilot-instructions.md` (Diretrizes para o GitHub Copilot)
Instruções de contexto para o Copilot Workspace e chat do GitHub:
* Linguagem e convenções do repositório.
* Padrão de commits (Conventional Commits).

---

## ESTRUTURA MODELO DO `CONTEXT.md`

```markdown
# 📖 Contexto e Dicionário do Projeto: [Nome do Projeto]

## 🎯 Resumo do Negócio
[Descrição concisa em 2 parágrafos de qual problema de negócio este software resolve].

## 📚 Dicionário de Termos do Negócio (Glossário)
Use sempre estes termos exatos ao invés de descrições genéricas:

| Termo do Negócio | O que significa no nosso sistema | O que NÃO dizer |
|---|---|---|
| **Tenant** | A organização ou empresa cliente que contrata nossa plataforma | "Conta", "Grupo", "Empresa" |
| **Workspace** | O espaço de trabalho isolado de um time dentro de um Tenant | "Projeto", "Pasta" |
| **Checkout Stream** | O fluxo de pagamento em tempo real via WebSockets com o gateway | "Tela de pagamento", "Compra" |

## 🔒 Regras Invariantes (Nunca Quebrar)
1. Todo acesso a dados no banco DEVE conter o filtro por `tenant_id`.
2. Moedas são armazenadas sempre em centavos inteiros (`integer`), nunca em ponto flutuante (`float`).
3. O status de um pedido segue a máquina finita: `CRIADO` -> `PAGO` -> `ENVIADO` -> `CONCLUIDO`.

## 🛠️ Comandos Frequentes de Desenvolvimento
- **Instalar:** `npm install`
- **Executar:** `npm run dev`
- **Testar:** `npm test`
- **Lint:** `npm run lint`
```

---

## ESTRUTURA MODELO DO `CLAUDE.md`

```markdown
# Diretrizes para o Claude Code — [Nome do Projeto]

## Comandos do Projeto
- **Rodar Local:** `npm run dev`
- **Rodar Testes:** `npm test`
- **Rodar Teste Único:** `npx vitest run src/path/to/test.ts`
- **Verificar Tipos:** `npx tsc --noEmit`
- **Linters:** `npm run lint`

## Padrões de Código
- Utilize TypeScript com modo estrito (`strict: true`).
- Toda validação de entrada deve usar **Zod**.
- Trate erros usando classes de domínio personalizadas (`DomainError`), nunca lance strings puras.
- Siga a linguagem e termos documentados em `CONTEXT.md`.
```

---

## SAÍDA NO CHAT / TERMINAL

Ao finalizar a execução, informe no chat:
1. Os arquivos de contexto gerados ou atualizados (`CONTEXT.md`, `CLAUDE.md`, `.cursorrules`, etc.).
2. A lista dos principais termos de negócio identificados e consolidados no glossário.
3. As invariantes de negócio capturadas da base de código.

---

## ENTREGÁVEIS FINAIS

Ao concluir todas as etapas, informe no chat:
1. O caminho relativo de todos os arquivos de contexto de IA criados na raiz do repositório.
2. Um resumo dos termos técnicos que a IA agora compreende para as próximas interações.
