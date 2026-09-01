#!/usr/bin/env bash
# ==============================================================================
# Script de Instalação Automática da Suíte de Prompts de AppSec & Engenharia
# Repositório: https://github.com/brunoez/prompts
# ==============================================================================

set -e

REPO_URL="https://github.com/brunoez/prompts.git"
RAW_BASE="https://raw.githubusercontent.com/brunoez/prompts/main"

# Cores para saída no terminal
C_RESET='\033[0m'
C_BOLD='\033[1m'
C_GREEN='\033[32m'
C_BLUE='\033[34m'
C_YELLOW='\033[33m'
C_CYAN='\033[36m'
C_RED='\033[31m'

echo -e "${C_CYAN}${C_BOLD}"
echo "================================================================="
echo "  🛡️  Instalador da Suíte de Prompts AppSec & Yellow Team"
echo "  📦 Repositório: https://github.com/brunoez/prompts"
echo "================================================================="
echo -e "${C_RESET}"

TARGET_DIR="${1:-.}"
INSTALL_MODE="${2:-agent}" # opcoes: agent (padrao), cursor, windsurf, submodule, all

echo -e "${C_BLUE}ℹ️  Diretório alvo: ${C_BOLD}${TARGET_DIR}${C_RESET}"

# Lista de categorias e arquivos
PROMPT_FILES=(
  "driven-development/sdd_spec_driven.md"
  "driven-development/secdd_abuse_cases.md"
  "driven-development/bdd_behavior_driven.md"
  "driven-development/tdd_test_driven.md"
  "driven-development/cdd_contract_driven.md"
  "driven-development/test_suite_generator.md"
  "driven-development/technical_documentation.md"
  "driven-development/project_context.md"
  "security/api.md"
  "security/business.md"
  "security/db.md"
  "security/frontend.md"
  "security/secrets.md"
  "security/supply_chain.md"
  "security/threat_modeling.md"
  "security/ai_appsec.md"
  "devops/cicd_pipeline.md"
  "devops/iac_docker_k8s.md"
  "devops/resilience_observability.md"
)

install_submodule() {
  echo -e "${C_YELLOW}📦 Instalando como Git Submodule em ${TARGET_DIR}/.agent/prompts...${C_RESET}"
  cd "$TARGET_DIR"
  if [ -d ".git" ]; then
    git submodule add "$REPO_URL" .agent/prompts || git submodule update --init --recursive
    echo -e "${C_GREEN}✅ Submódulo configurado com sucesso!${C_RESET}"
  else
    echo -e "${C_RED}❌ O diretório alvo não é um repositório git. Inicialize com 'git init' primeiro.${C_RESET}"
    exit 1
  fi
}

install_files() {
  local DEST_BASE="$1"
  echo -e "${C_YELLOW}📥 Baixando/Copiando prompts para ${DEST_BASE}...${C_RESET}"
  
  mkdir -p "${DEST_BASE}/driven-development" "${DEST_BASE}/security" "${DEST_BASE}/devops"
  
  # Se o script estiver rodando dentro do próprio clone local dos prompts:
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  LOCAL_PROMPTS_DIR=""
  if [ -d "${SCRIPT_DIR}/prompts" ]; then
    LOCAL_PROMPTS_DIR="${SCRIPT_DIR}/prompts"
  elif [ -d "${SCRIPT_DIR}/../prompts" ]; then
    LOCAL_PROMPTS_DIR="${SCRIPT_DIR}/../prompts"
  fi

  for file in "${PROMPT_FILES[@]}"; do
    dest_path="${DEST_BASE}/${file}"
    if [ -n "$LOCAL_PROMPTS_DIR" ] && [ -f "${LOCAL_PROMPTS_DIR}/${file}" ]; then
      cp "${LOCAL_PROMPTS_DIR}/${file}" "$dest_path"
    else
      # Baixa diretamente do GitHub
      curl -sSL "${RAW_BASE}/prompts/${file}" -o "$dest_path"
    fi
  done
  
  echo -e "${C_GREEN}✅ Prompts instalados em: ${DEST_BASE}${C_RESET}"
}

case "$INSTALL_MODE" in
  submodule)
    install_submodule
    ;;
  cursor)
    install_files "${TARGET_DIR}/.cursor/rules"
    ;;
  windsurf)
    install_files "${TARGET_DIR}/.windsurf/rules"
    ;;
  all)
    install_files "${TARGET_DIR}/.agent/prompts"
    install_files "${TARGET_DIR}/.cursor/rules"
    install_files "${TARGET_DIR}/.windsurf/rules"
    ;;
  agent|*)
    install_files "${TARGET_DIR}/.agent/prompts"
    ;;
esac

echo ""
echo -e "${C_GREEN}${C_BOLD}🎉 Instalação concluída com sucesso!${C_RESET}"
echo -e "${C_CYAN}👉 Para usar em sua IDE ou agente de IA:${C_RESET}"
echo -e "   1. Mencione o arquivo no chat (ex: @[.agent/prompts/sdd_spec_driven.md])"
echo -e "   2. Solicite a auditoria ou o planejamento guiado para sua feature."
echo -e "   3. Documentação completa em: ${C_BOLD}https://github.com/brunoez/prompts${C_RESET}"
echo ""
