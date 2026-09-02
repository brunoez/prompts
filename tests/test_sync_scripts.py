#!/usr/bin/env python3
"""
==============================================================================
Suíte de Testes Unitários: Sincronizadores de CI/CD (Jira, GitHub & GitLab)
==============================================================================
Testa a lógica de parsing de SARIF v2.1.0, validação de variáveis de ambiente,
montagem de payloads (ADF e Markdown) e algoritmos de deduplicação usando mocks.
Zero dependências externas — compatível com unittest nativo do Python 3.
==============================================================================
"""

import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Adiciona o diretório raiz e examples/ci-cd ao sys.path para importação dos módulos
ROOT_DIR = Path(__file__).resolve().parent.parent
CI_CD_DIR = ROOT_DIR / "examples" / "ci-cd"
sys.path.insert(0, str(CI_CD_DIR))

import github_issues_sync  # noqa: E402
import gitlab_issues_sync  # noqa: E402
import jira_sync  # noqa: E402

SAMPLE_SARIF = {
    "version": "2.1.0",
    "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
    "runs": [
        {
            "tool": {
                "driver": {
                    "name": "AppSec AI Auditor",
                    "version": "1.0.0"
                }
            },
            "results": [
                {
                    "ruleId": "ASTF-API1",
                    "level": "error",
                    "message": {"text": "Broken Object Level Authorization (BOLA) detectado no endpoint."},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": "src/controllers/order.ts"},
                                "region": {"startLine": 42}
                            }
                        }
                    ]
                },
                {
                    "ruleId": "WSTG-BUSL-08",
                    "level": "warning",
                    "message": {"text": "Upload de arquivo sem validação de Magic Bytes."},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": "src/services/upload.ts"},
                                "region": {"startLine": 15}
                            }
                        }
                    ]
                },
                {
                    "ruleId": "CLEAN-CODE",
                    "level": "note",
                    "message": {"text": "Sugestão de estilo cosmético."},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": "src/utils/format.ts"},
                                "region": {"startLine": 8}
                            }
                        }
                    ]
                }
            ]
        }
    ]
}


class TestJiraSync(unittest.TestCase):
    """Bateria de testes unitários para jira_sync.py."""

    def setUp(self):
        jira_sync.PROCESSED_KEYS.clear()

    @patch.dict(os.environ, {}, clear=True)
    def test_validate_env_missing(self):
        """Garante que validate_env() falhe se faltarem variáveis obrigatórias."""
        jira_sync.JIRA_BASE_URL = ""
        jira_sync.JIRA_USER_EMAIL = ""
        jira_sync.JIRA_API_TOKEN = ""
        jira_sync.JIRA_PROJECT_KEY = ""
        self.assertFalse(jira_sync.validate_env())

    @patch.dict(os.environ, {
        "JIRA_BASE_URL": "https://empresa.atlassian.net",
        "JIRA_USER_EMAIL": "sec@empresa.com",
        "JIRA_API_TOKEN": "secret-token",
        "JIRA_PROJECT_KEY": "SEC"
    })
    def test_validate_env_success(self):
        """Garante que validate_env() passe com variáveis válidas."""
        jira_sync.JIRA_BASE_URL = "https://empresa.atlassian.net"
        jira_sync.JIRA_USER_EMAIL = "sec@empresa.com"
        jira_sync.JIRA_API_TOKEN = "secret-token"
        jira_sync.JIRA_PROJECT_KEY = "SEC"
        self.assertTrue(jira_sync.validate_env())

    def test_build_adf_description(self):
        """Valida a estrutura do payload ADF (Atlassian Document Format)."""
        adf = jira_sync.build_adf_description(
            rule_id="ASTF-API1",
            message="Falha de BOLA em src/api.ts",
            file_path="src/api.ts",
            start_line=20,
            severity="error"
        )
        self.assertEqual(adf["type"], "doc")
        self.assertEqual(adf["version"], 1)
        self.assertTrue(len(adf["content"]) >= 3)

    @patch("urllib.request.urlopen")
    def test_search_existing_issue_found(self, mock_urlopen):
        """Verifica se search_existing_issue detecta issue aberta no Jira."""
        jira_sync.JIRA_BASE_URL = "https://empresa.atlassian.net"
        jira_sync.JIRA_PROJECT_KEY = "SEC"

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "total": 1,
            "issues": [{"fields": {"summary": "[AppSec] ASTF-API1 em src/controllers/order.ts:42"}}]
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        exists = jira_sync.search_existing_issue("ASTF-API1", "src/controllers/order.ts", 42)
        self.assertTrue(exists)

    @patch("urllib.request.urlopen")
    def test_create_jira_issue_success(self, mock_urlopen):
        """Testa criação bem-sucedida de card no Jira quando não há duplicata."""
        jira_sync.JIRA_BASE_URL = "https://empresa.atlassian.net"
        jira_sync.JIRA_PROJECT_KEY = "SEC"

        # Mock 1: search retorna sem duplicatas
        search_resp = MagicMock()
        search_resp.read.return_value = json.dumps({"total": 0, "issues": []}).encode("utf-8")
        search_resp.__enter__.return_value = search_resp

        # Mock 2: create retorna key criada
        create_resp = MagicMock()
        create_resp.read.return_value = json.dumps({"key": "SEC-101"}).encode("utf-8")
        create_resp.__enter__.return_value = create_resp

        mock_urlopen.side_effect = [search_resp, create_resp]

        key = jira_sync.create_jira_issue(
            rule_id="ASTF-API1",
            message="Falha crítica",
            file_path="src/auth.ts",
            start_line=10,
            severity="error"
        )
        self.assertEqual(key, "SEC-101")
        self.assertIn("ASTF-API1:src/auth.ts:10", jira_sync.PROCESSED_KEYS)

    @patch("jira_sync.search_existing_issue")
    def test_create_jira_issue_duplicate_skipped(self, mock_search):
        """Garante que a criação seja ignorada se a issue já existir."""
        mock_search.return_value = True

        key = jira_sync.create_jira_issue(
            rule_id="ASTF-API1",
            message="Falha crítica",
            file_path="src/auth.ts",
            start_line=10,
            severity="error"
        )
        self.assertIsNone(key)


class TestGitHubIssuesSync(unittest.TestCase):
    """Bateria de testes unitários para github_issues_sync.py."""

    def setUp(self):
        github_issues_sync.PROCESSED_KEYS.clear()
        github_issues_sync.OPEN_ISSUE_TITLES_CACHE = None

    @patch.dict(os.environ, {}, clear=True)
    def test_validate_env_missing(self):
        github_issues_sync.GITHUB_TOKEN = ""
        github_issues_sync.GITHUB_REPOSITORY = ""
        self.assertFalse(github_issues_sync.validate_env())

    @patch("urllib.request.urlopen")
    def test_load_all_open_issues(self, mock_urlopen):
        """Valida listagem e cache de issues abertas com paginação."""
        github_issues_sync.GITHUB_TOKEN = "fake-token"
        github_issues_sync.GITHUB_REPOSITORY = "owner/repo"

        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps([
            {"title": "[AppSec] ASTF-API1 em src/controllers/order.ts:42"},
            {"title": "Bug aleatório"}
        ]).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        titles = github_issues_sync.load_all_open_issues()
        self.assertEqual(len(titles), 2)
        self.assertTrue(github_issues_sync.is_issue_already_open("[AppSec] ASTF-API1 em src/controllers/order.ts:42"))

    @patch("urllib.request.urlopen")
    def test_create_github_issue_success(self, mock_urlopen):
        """Valida criação de nova issue no GitHub."""
        github_issues_sync.GITHUB_TOKEN = "fake-token"
        github_issues_sync.GITHUB_REPOSITORY = "owner/repo"
        github_issues_sync.OPEN_ISSUE_TITLES_CACHE = set()

        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({
            "number": 42,
            "html_url": "https://github.com/owner/repo/issues/42"
        }).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        issue_num = github_issues_sync.create_github_issue(
            rule_id="WSTG-BUSL-08",
            message="Magic bytes ausentes",
            file_path="src/upload.ts",
            start_line=15,
            severity="warning"
        )
        self.assertEqual(issue_num, 42)
        self.assertIn("WSTG-BUSL-08:src/upload.ts:15", github_issues_sync.PROCESSED_KEYS)


class TestGitLabIssuesSync(unittest.TestCase):
    """Bateria de testes unitários para gitlab_issues_sync.py."""

    def setUp(self):
        gitlab_issues_sync.PROCESSED_KEYS.clear()

    @patch.dict(os.environ, {}, clear=True)
    def test_validate_env_missing(self):
        gitlab_issues_sync.GITLAB_TOKEN = ""
        gitlab_issues_sync.CI_PROJECT_ID = ""
        self.assertFalse(gitlab_issues_sync.validate_env())

    @patch("urllib.request.urlopen")
    def test_search_existing_issue(self, mock_urlopen):
        """Valida busca de issue existente no GitLab."""
        gitlab_issues_sync.GITLAB_TOKEN = "fake-token"
        gitlab_issues_sync.CI_PROJECT_ID = "12345"

        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps([
            {"title": "[AppSec] ASTF-API1 em src/controllers/order.ts:42"}
        ]).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        exists = gitlab_issues_sync.search_existing_issue("ASTF-API1", "src/controllers/order.ts")
        self.assertTrue(exists)

    @patch("urllib.request.urlopen")
    def test_create_gitlab_issue_success(self, mock_urlopen):
        """Valida criação de issue no GitLab."""
        gitlab_issues_sync.GITLAB_TOKEN = "fake-token"
        gitlab_issues_sync.CI_PROJECT_ID = "12345"

        # Mock 1: search retorna sem duplicatas
        search_resp = MagicMock()
        search_resp.read.return_value = json.dumps([]).encode("utf-8")
        search_resp.__enter__.return_value = search_resp

        # Mock 2: create retorna issue criada
        create_resp = MagicMock()
        create_resp.read.return_value = json.dumps({
            "iid": 12,
            "web_url": "https://gitlab.com/owner/repo/-/issues/12"
        }).encode("utf-8")
        create_resp.__enter__.return_value = create_resp

        mock_urlopen.side_effect = [search_resp, create_resp]

        iid = gitlab_issues_sync.create_gitlab_issue(
            rule_id="ASTF-API1",
            message="Falha crítica BOLA",
            file_path="src/order.ts",
            start_line=42,
            severity="error"
        )
        self.assertEqual(iid, 12)
        self.assertIn("ASTF-API1:src/order.ts:42", gitlab_issues_sync.PROCESSED_KEYS)


if __name__ == "__main__":
    unittest.main()
