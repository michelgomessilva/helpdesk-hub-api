# HelpDesk Hub API

API backend do projeto HelpDesk Hub API, desenvolvida com FastAPI e gerenciada com `uv`.

## Objetivo

Construir uma API backend para abertura e gestao de chamados internos de suporte, servindo como base evolutiva para autenticacao, tickets, comentarios, historico, observabilidade e demais features do projeto.

## Requisitos

- Python 3.10+
- `uv` instalado

## Como executar

```powershell
uv sync
uv run uvicorn helpdesk_hub_api.main:app --reload
```

A aplicacao sera iniciada em `http://127.0.0.1:8000`.

Documentacao interativa:

- Swagger UI: `http://127.0.0.1:8000/docs`

## Endpoints iniciais

- `GET /api/v1/`
- `GET /api/v1/health`

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
