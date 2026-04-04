# HelpDesk Hub API

API backend do projeto HelpDesk Hub API, desenvolvida com FastAPI e gerenciada com `uv`.

## Requisitos

- Python 3.10+
- `uv` instalado

## Como executar

```powershell
uv sync
uv run uvicorn helpdesk_hub_api.main:app --reload
```

A aplicacao sera iniciada em `http://127.0.0.1:8000`.

## Endpoints iniciais

- `GET /`
- `GET /health`

## Testes

```powershell
uv run pytest
```

## Estrutura inicial

```text
src/helpdesk_hub_api/
tests/
docs/
scripts/
```
