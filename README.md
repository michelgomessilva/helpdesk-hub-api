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

Todos os testes devem passar antes de fazer commit. O projeto segue TDD (Test-Driven Development).

## Como Contribuir

Este projeto segue **Spec-Driven Development (SDD)**. Antes de implementar uma feature:

1. **Criar ou identificar a issue no GitHub**
2. **Criar a especificacao** em `docs/features/f<numero>-<slug>.md`
3. **Criar branch de feature** com o padrão `feature/f<numero>-<slug>`

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/f001-nome-da-feature
   ```

4. **Fazer commits atomicos** com mensagens padronizadas

   ```bash
   git commit -m "[F001] Add feature description"
   ```

5. **Criar Pull Request** apontando para `develop` (não para `main`)
   - Título: `[F001] Feature description`
   - Descrever mudanças e critérios de aceitação
   - Referenciar a issue: `closes #1`

6. **Code review e merge** com Squash and Merge
7. **Atualizar a spec** com status `Done` e link da PR

Veja `docs/spec-driven-development.md` para o guia completo de desenvolvimento.

## Estrutura de Documentação

- `docs/spec-driven-development.md` - Guia central de SDD, roadmap e feature index
- `docs/features/` - Especificações detalhadas de cada feature
- `CLAUDE.md` - Instruções para desenvolvimento com Claude Code

## Estrutura inicial

```text
src/
├── main.py              # FastAPI app factory
├── api/                 # HTTP layer (routes, schemas)
├── domain/              # Domain entities and enums
├── application/         # Use cases (planned)
└── infrastructure/      # Database, external services (planned)

tests/                   # Test suite (TDD-driven)
docs/                    # Documentation and feature specs
```
