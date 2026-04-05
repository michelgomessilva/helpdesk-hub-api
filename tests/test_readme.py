from pathlib import Path


README_PATH = Path("README.md")


def test_readme_exists() -> None:
    assert README_PATH.exists()


def test_readme_contains_project_name_and_goal() -> None:
    content = README_PATH.read_text(encoding="utf-8")

    assert "# HelpDesk Hub API" in content
    assert "## Objetivo" in content
    assert "abertura e gestao de chamados internos de suporte" in content


def test_readme_contains_local_run_instructions() -> None:
    content = README_PATH.read_text(encoding="utf-8")

    assert "## Como executar" in content
    assert "uv sync" in content
    assert "uv run uvicorn helpdesk_hub_api.main:app --reload" in content
