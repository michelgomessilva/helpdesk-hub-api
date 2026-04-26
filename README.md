# HelpDesk Hub API

API backend do projeto HelpDesk Hub API, desenvolvida com FastAPI e gerenciada com `uv`.

## Objetivo

Construir uma API backend para abertura e gestao de chamados internos de suporte, servindo como base evolutiva para autenticacao, tickets, comentarios, historico, observabilidade e demais features do projeto.

## Requisitos

- Python 3.10+
- `uv` instalado

## Como executar

```bash
uv sync
uv run uvicorn main:app --reload
```

A aplicacao sera iniciada em `http://127.0.0.1:8000`.

Documentacao interativa:

- Swagger UI: `http://127.0.0.1:8000/docs`

## Endpoints iniciais

- `GET /api/v1/`
- `GET /api/v1/health`

## Testes

```bash
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

## Arquitetura

O projeto segue **Clean Architecture** com 4 camadas claramente separadas:

```text
src/
├── main.py                       # FastAPI app factory
├── api/                          # HTTP layer (routes, schemas)
│   ├── routes/
│   │   ├── system.py            # GET / e GET /health
│   │   └── tickets.py           # Endpoints de tickets
│   └── schemas/
│       ├── system.py            # HealthResponse, RootResponse
│       └── tickets.py           # TicketCreate, TicketResponse (Pydantic DTOs)
├── domain/                       # Domain layer (entities, enums, contracts)
│   ├── entities/
│   │   └── ticket.py            # Ticket dataclass (domínio puro)
│   ├── enums/
│   │   └── ticket.py            # TicketStatus, TicketPriority, TicketCategory
│   └── repositories/
│       └── ticket.py            # TicketRepository (ABC - contrato)
├── application/                  # Application layer (mediatr/CQRS)
│   └── tickets/
│       ├── commands/
│       │   └── create_ticket.py # CreateTicketCommand + CreateTicketHandler
│       └── queries/
│           └── list_tickets.py  # ListTicketsQuery + ListTicketsHandler
└── infrastructure/               # Infrastructure layer (implementações concretas)
    └── repositories/
        └── ticket.py            # InMemoryTicketRepository

tests/                            # Test suite (TDD-driven)
docs/                             # Documentation and feature specs
```

### Descrição das camadas

- **API Layer** (`api/`): Responsável pela comunicação HTTP. Rotas delegam para o `application/` (mediatr). Schemas definem contracts Pydantic para request/response.

- **Domain Layer** (`domain/`): Lógica de negócio pura. Entities como dataclasses, enums imutáveis, e **ABCs (interfaces)** para Repository que definem contratos.

- **Application Layer** (`application/`): Casos de uso implementados via **mediatr** (padrão CQRS). **Commands** para escrita, **Queries** para leitura. Organização por feature (Vertical Slice). Handlers orquestram o repositório e domínio.

- **Infrastructure Layer** (`infrastructure/`): Implementações concretas de repositórios e serviços externos. Hoje: `InMemoryTicketRepository`. Futuro: `PostgresTicketRepository`, cache, etc.

### Padrão: mediatr / CQRS

O projeto adota o padrão **mediatr** (port Python do MediatR do C#) para desacoplar rotas FastAPI da lógica de negócio:

- **Commands** (`application/<feature>/commands/`): Operações de escrita (create, update, delete)
- **Queries** (`application/<feature>/queries/`): Operações de leitura (list, get by id)
- **Handlers**: Recebi o repositório via injeção, orquestram domínio e infraestrutura
- **Rotas FastAPI**: Apenas delegam para o Mediator — nunca contêm lógica

Isto facilita testes, reutilização e evolução para autenticação, auditoria e permissões.
