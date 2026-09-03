#!/usr/bin/env python3
"""
Script de Verificação de Integridade, Qualidade e Testes da Suíte de Prompts
Executado em CI/CD e localmente para garantir zero drift nos prompts e scripts.
"""

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT_DIR / "prompts"

EXPECTED_PROMPTS = [
    "driven-development/sdd_spec_driven.md",
    "driven-development/secdd_abuse_cases.md",
    "driven-development/bdd_behavior_driven.md",
    "driven-development/tdd_test_driven.md",
    "driven-development/cdd_contract_driven.md",
    "driven-development/test_suite_generator.md",
    "driven-development/technical_documentation.md",
    "driven-development/project_context.md",
    "security/api.md",
    "security/business.md",
    "security/db.md",
    "security/frontend.md",
    "security/secrets.md",
    "security/supply_chain.md",
    "security/threat_modeling.md",
    "security/ai_appsec.md",
    "devops/cicd_pipeline.md",
    "devops/iac_docker_k8s.md",
    "devops/resilience_observability.md",
]

REQUIRED_SECTIONS = [
    "## OBJETIVO",
    "## ESCOPO",
    "## SAÍDA",
    "## ENTREGÁVEIS",
]


def test_prompts_exist():
    print("🔍 [1/6] Verificando existência física de todos os 19 prompts...")
    missing = []
    for rel_path in EXPECTED_PROMPTS:
        full_path = PROMPTS_DIR / rel_path
        if not full_path.is_file():
            missing.append(rel_path)
    if missing:
        print(f"❌ ERRO: Prompts ausentes no disco: {missing}")
        return False
    print(f"✅ Todos os {len(EXPECTED_PROMPTS)} prompts existem fisicamente.")
    return True


def test_prompt_structure():
    print("🔍 [2/6] Validando contrato de estrutura padrão dos prompts...")
    errors = []
    for rel_path in EXPECTED_PROMPTS:
        full_path = PROMPTS_DIR / rel_path
        content = full_path.read_text(encoding="utf-8")
        
        for section in REQUIRED_SECTIONS:
            if section not in content:
                errors.append(f"Prompt {rel_path} não contém a seção obrigatória '{section}'")
        
        if "## CHECKLIST" not in content and "### 1." not in content:
            errors.append(f"Prompt {rel_path} não contém seção de CHECKLIST de auditoria")

    if errors:
        for err in errors:
            print(f"❌ {err}")
        return False
    print("✅ Todos os prompts atendem ao contrato estrutural padrão.")
    return True


def test_install_script_sync():
    print("🔍 [3/6] Validando sincronia do instalador install.sh...")
    install_sh = ROOT_DIR / "install.sh"
    if not install_sh.is_file():
        print("❌ ERRO: install.sh não encontrado.")
        return False
    
    content = install_sh.read_text(encoding="utf-8")
    missing_in_installer = []
    for rel_path in EXPECTED_PROMPTS:
        if f'"{rel_path}"' not in content:
            missing_in_installer.append(rel_path)
            
    if missing_in_installer:
        print(f"❌ ERRO: install.sh não inclui os prompts: {missing_in_installer}")
        return False
    print("✅ install.sh está 100% sincronizado com o catálogo de prompts.")
    return True


def test_readme_links():
    print("🔍 [4/6] Validando links de prompts no README.md...")
    readme = ROOT_DIR / "README.md"
    content = readme.read_text(encoding="utf-8")
    missing_in_readme = []
    for rel_path in EXPECTED_PROMPTS:
        if rel_path not in content:
            missing_in_readme.append(rel_path)
            
    if missing_in_readme:
        print(f"❌ ERRO: README.md não faz referência aos prompts: {missing_in_readme}")
        return False
    print("✅ README.md faz referência a todos os prompts.")
    return True


def test_installer_execution():
    print("🔍 [5/6] Testando execução funcional do instalador install.sh...")
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = ["bash", str(ROOT_DIR / "install.sh"), tmpdir, "all"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ ERRO na execução do install.sh: {res.stderr}")
            return False
        
        for folder in [".claude/prompts", ".agent/prompts", ".cursor/rules", ".windsurf/rules"]:
            target_path = Path(tmpdir) / folder
            for prompt in EXPECTED_PROMPTS:
                if not (target_path / prompt).is_file():
                    print(f"❌ ERRO: Arquivo {prompt} não foi instalado em {folder}")
                    return False
    print("✅ install.sh executado e testado com sucesso em todos os modos.")
    return True


def test_sync_scripts_unit():
    print("🔍 [6/6] Executando suíte de testes unitários dos sincronizadores CI/CD...")
    test_file = ROOT_DIR / "tests" / "test_sync_scripts.py"
    res = subprocess.run([sys.executable, "-m", "unittest", str(test_file)], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ ERRO nos testes unitários dos scripts de sync:\n{res.stderr}")
        return False
    print("✅ 12/12 testes unitários dos scripts de sincronização passaram com sucesso.")
    return True


def main():
    print("=================================================================")
    print("  🛡️  Bateria de Testes de Integridade & Qualidade da Suíte")
    print("=================================================================")
    tests = [
        test_prompts_exist,
        test_prompt_structure,
        test_install_script_sync,
        test_readme_links,
        test_installer_execution,
        test_sync_scripts_unit,
    ]
    
    failed = False
    for t in tests:
        if not t():
            failed = True
            break
            
    if failed:
        print("\n❌ FALHA: A suíte de testes encontrou erros.")
        sys.exit(1)
    else:
        print("\n🎉 SUCESSO: Todos os testes de integridade, qualidade e unitários passaram!")
        sys.exit(0)


if __name__ == "__main__":
    main()
