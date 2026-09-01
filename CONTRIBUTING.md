# 🤝 Guia de Contribuição

Primeiramente, muito obrigado por se interessar em contribuir com a **Suíte de Prompts de AppSec, Engenharia e Yellow Team**! Este é um projeto aberto voltado a elevar o padrão de engenharia, arquitetura e segurança da comunidade de desenvolvimento brasileira e global.

---

## 🌟 Como Contribuir

Você pode contribuir de diversas formas:
1. **Adicionando Novos Prompts:** Criando novos prompts de auditoria para especialidades ainda não cobertas (ex: Mobile Security, Smart Contracts, Criptografia Avançada).
2. **Aprimorando Checklists Existentes:** Atualizando regras com novos vetores de ataque, CVEs recentes ou boas práticas de frameworks modernos.
3. **Melhorando Scripts e Templates:** Aprimorando os geradores de relatório em PDF, templates de issues ou instaladores.
4. **Relatando Problemas:** Abrindo issues relatando inconsistências ou falsos positivos gerados por algum prompt.

---

## 📐 Padrão Obrigatório para Novos Prompts

Para manter a consistência e o alto nível técnico de toda a biblioteca, **todo novo prompt DEVE seguir a seguinte estrutura**:

1. **Título Padronizado:**
   ```markdown
   # PROMPT DE AUDITORIA COMPLETA: [ESPECIALIDADE] E GERAÇÃO DE RELATÓRIO PDF
   ```
2. **Persona / Objetivo:** Definir o papel como *Engenheiro Principal* ou *Especialista Líder (Yellow Team)*.
3. **Escopo e Obrigatoriedade de Leitura:** Mapeamento de diretórios e arquivos que devem ser lidos linha por linha.
4. **Checklist Prático:** Dividido em 3 a 5 categorias claras de verificação técnica.
5. **Saída no Terminal / Chat:**
   - **Parte 1:** Matriz de Priorização (ID, Arquivo, Categoria, Severidade, Esforço, Quick Win).
   - **Parte 2:** Detalhamento Completo com Severidade, Esforço, Evidência e Código de Correção.
6. **Geração de Relatório em PDF e Issues:**
   - Script Python isolado (`reportlab` + `matplotlib`).
   - Paleta de cores oficial: Crítica `#B91C1C`, Alta `#EA580C`, Média `#D97706`, Baixa `#2563EB`, Ponto Forte `#059669`.
   - Templates de issues completos para GitHub/GitLab com critérios de aceite verificáveis.

---

## 🌿 Fluxo de Git (GitFlow)

1. Faça um Fork do repositório: `https://github.com/brunoez/prompts`
2. Crie uma branch para sua modificação:
   ```bash
   git checkout -b feat/novo-prompt-mobile
   ```
3. Realize seus commits seguindo o padrão **Conventional Commits**:
   ```bash
   git commit -m "feat(security): add mobile appsec audit prompt"
   ```
4. Envie a branch para seu fork:
   ```bash
   git push origin feat/novo-prompt-mobile
   ```
5. Abra um **Pull Request / Merge Request** preenchendo o template padrão.

---

## 📜 Código de Conduta

Ao participar deste projeto, você concorda em seguir nosso [Código de Conduta](CODE_OF_CONDUCT.md), promovendo um ambiente acolhedor, respeitoso e livre de assédio para todos.
