# F010 - Implementar Endpoint POST /api/v1/tickets

## Metadados

- ID: `F010`
- Status: `Draft`
- Criado em: `2026-04-26`
- Atualizado em: `2026-04-26`
- Origem no GitHub: #13 - https://github.com/michelgomessilva/helpdesk-hub-api/issues/13
- PR: —

## Resumo Executivo

Implementar endpoint HTTP `POST /api/v1/tickets` para permitir que utilizadores criem tickets (chamados) via API. Segue o padrão **mediatr/CQRS** com `CreateTicketCommand` + handler orquestrando repositório e domínio. Ticket é armazenado em memória (F009) e retorna HTTP 201 com metadados gerados (UUID, número sequencial, timestamp).

---

## Contexto e Problema

### Situação Atual
- F009 implementou armazenamento em memória (`InMemoryTicketRepository`)
- F008 implementou schemas Pydantic (`TicketCreate`, `TicketResponse`)
- Falta endpoint HTTP para **criar** tickets — só existem GET `/` e `/health`

### Necessidade
O projeto precisa de um endpoint de escrita para abrir chamados. Isto é o primeiro CRUD de negócio depois das fundações (setup, schemas, repositório).

### Impacto
- Utilizadores podem criar tickets via API
- Demonstra padrão mediatr/CQRS completo (command + handler)
- Base para F011 (GET /tickets com queries) e autenticação futura

---

## Objetivo

Entregar endpoint funcional `POST /api/v1/tickets` que:
1. **Receba** `TicketCreate` (title, description, category, status, priority)
2. **Valide** via Pydantic (já em F008)
3. **Orquestre** domínio + repositório via `CreateTicketHandler`
4. **Persista** em memória via `InMemoryTicketRepository`
5. **Retorne** HTTP 201 + `TicketResponse` com id, number, created_at

---

## Escopo

### Incluído

- ✅ Criar `CreateTicketCommand` em `application/tickets/commands/create_ticket.py`
- ✅ Implementar `CreateTicketHandler` com lógica de orquestração
- ✅ Ligar rota `POST /api/v1/tickets` ao mediator
- ✅ Validação Pydantic (reutilizar `TicketCreate` de F008)
- ✅ Resposta HTTP 201 + `TicketResponse`
- ✅ Erros HTTP 422 para payload inválido
- ✅ Testes unitários (handler com mock de repositório)
- ✅ Testes de integração (rota com `InMemoryTicketRepository`)

### Fora de Escopo

- ❌ Autenticação/autorização (F012+)
- ❌ Permissões por role (F012+)
- ❌ GET /api/v1/tickets (será F011, ListTicketsQuery)
- ❌ Filtros, paginação (F012+)
- ❌ Persistência em PostgreSQL (F014+)
- ❌ Auditoria de criação (user, timestamp histórico) — F013+

---

## Personas e Contexto de Negócio

### Personas Impactadas
- **Utilizador interno** (TI, suporte): Abre tickets via API ou cliente web
- **Desenvolvedor**: Testa API com curl/Postman/cliente

### Labels (GitHub)
- `feature` — Nova funcionalidade
- `api` — Afeta camada HTTP
- `tickets` — Domínio de chamados
- `priority: high` — Essencial para CRUD básico
- `week-2` — Fase 1 (fundações)

### Contexto Técnico
O projeto segue **Clean Architecture** com 4 camadas:
- **API**: Rotas FastAPI, apenas delegam para mediator
- **Application**: mediatr Commands/Queries, handlers orquestram
- **Domain**: Entidades, enums, contratos (ABCs)
- **Infrastructure**: Implementações (repositórios, serviços)

Esta feature **ativa o padrão de escrita** (Commands) do CQRS.

---

## Requisitos Funcionais

| ID | Requisito | Notas |
| --- | --- | --- |
| RF01 | Criar `CreateTicketCommand` com campos (title, description, category, status, priority) | Reusa `TicketCreate` schema |
| RF02 | Implementar `CreateTicketHandler` que orquestra criação | Recebe repositório via `__init__` |
| RF03 | Endpoint `POST /api/v1/tickets` delega para mediator | Rota não contém lógica |
| RF04 | Validar entrada via Pydantic (min_length, enums) | F008 já implementa |
| RF05 | Gerar UUID para `id` e número sequencial para `number` | F009 repositório já faz |
| RF06 | Definir `status='open'` por padrão no command | Pode vir do schema ou handler |
| RF07 | Retornar HTTP 201 + `TicketResponse` completo | Com id, number, created_at |
| RF08 | Retornar HTTP 422 em payload inválido | FastAPI + Pydantic automático |
| RF09 | Ticket criado é persistido em memória | Verificável via InMemoryTicketRepository |

## Requisitos Não Funcionais

| ID | Requisito | Justificativa |
| --- | --- | --- |
| RNF01 | Handler testável isoladamente | Mock de repositório, sem HTTP |
| RNF02 | Rota testável com `TestClient` | Integração completa de stack |
| RNF03 | Respeita Clean Architecture | Handlers em `application/`, rotas em `api/` |
| RNF04 | Respeita padrão mediatr/CQRS | Commands separados de Queries |
| RNF05 | Sem duplicação de validação | Reutiliza Pydantic de F008 |
| RNF06 | Sem acoplamento entre camadas | Repositório é injeção, não import direto |

---

## Padrão Arquitetural: mediatr / CQRS

Esta feature demonstra o padrão **CQRS (Command Query Responsibility Segregation)** implementado com **mediatr**:

### Componentes

**1. Command (Escrita)**
```python
# application/tickets/commands/create_ticket.py
@dataclass
class CreateTicketCommand(GenericRequest[Ticket]):
    """Comando para criar um ticket."""
    title: str
    description: str
    category: str
    status: str = "open"
    priority: str = "medium"
```

**2. Handler (Lógica)**
```python
class CreateTicketHandler:
    """Orquestra criação: validação + persistência."""
    def __init__(self, repo: TicketRepository) -> None:
        self._repo = repo

    async def handle(self, request: CreateTicketCommand) -> Ticket:
        # Criar entidade de domínio (dataclass pura)
        ticket = Ticket(
            title=request.title,
            description=request.description,
            category=TicketCategory(request.category),
            status=TicketStatus(request.status),
            priority=TicketPriority(request.priority),
        )
        # Persister via repositório
        return self._repo.save(ticket)
```

**3. Rota (Delegação)**
```python
# api/routes/tickets.py
@router.post("/", status_code=201, response_model=TicketResponse)
async def create_ticket(
    data: TicketCreate,
    repo: TicketRepository = Depends(get_ticket_repository),
) -> TicketResponse:
    """Delega para mediatr, nunca contém lógica."""
    handler = CreateTicketHandler(repo)
    ticket = await handler.handle(CreateTicketCommand(
        title=data.title,
        description=data.description,
        category=data.category.value,
        status=data.status.value,
        priority=data.priority.value,
    ))
    return TicketResponse.from_entity(ticket)
```

### Fluxo de Execução

```
POST /api/v1/tickets (JSON)
    ↓
FastAPI valida via TicketCreate (Pydantic)
    ↓
Rota cria CreateTicketCommand
    ↓
CreateTicketHandler.handle() orquestra
    ↓
Cria entidade Ticket (dataclass)
    ↓
Repositório.save() → gera UUID + número sequencial
    ↓
Retorna Ticket persistido
    ↓
Rota converte para TicketResponse (Pydantic)
    ↓
HTTP 201 + JSON
```

### Por Que Mediatr?

| Aspecto | Benefício |
| --- | --- |
| **Testabilidade** | Handler testável sem HTTP, com mock repo |
| **Reutilização** | Mesmo handler pode ser chamado de CLI, job, webhook |
| **Auditoria** | Cada command é um evento — fácil logar/auditar |
| **Segurança** | Permissões podem ser adicionadas no handler (futuro) |
| **Escalabilidade** | Handlers podem ser assíncronos, paralelos |

---

## Critérios de Aceitação

### Implementação

- [ ] **CA-01**: `CreateTicketCommand` definido em `application/tickets/commands/create_ticket.py`
  - Campos: title, description, category, status, priority
  - Herda de `GenericRequest[Ticket]`

- [ ] **CA-02**: `CreateTicketHandler` implementado
  - `__init__(self, repo: TicketRepository)`
  - `async def handle(self, request: CreateTicketCommand) -> Ticket`
  - Cria entidade Ticket via dataclass
  - Persiste via `repo.save(ticket)`

- [ ] **CA-03**: Rota `POST /api/v1/tickets` implementada
  - Recebe `TicketCreate` (reutiliza F008)
  - Injeta `TicketRepository` via `Depends()`
  - Delega para `CreateTicketHandler.handle()`
  - Retorna `TicketResponse` com status 201

- [ ] **CA-04**: Validação funcional
  - Título vazio → 422 Validation Error
  - Descrição vazia → 422 Validation Error
  - Status inválido → 422 Validation Error
  - Prioridade inválida → 422 Validation Error
  - Categoria inválida → 422 Validation Error

### Dados e Estado

- [ ] **CA-05**: Ticket criado recebe UUID único
  - Verificável via `isinstance(ticket.id, UUID)`
  - Diferentes tickets → IDs diferentes

- [ ] **CA-06**: Ticket criado recebe número sequencial
  - Primeiro ticket → number=1
  - Segundo ticket → number=2

- [ ] **CA-07**: Ticket criado com status='open' (default)
  - Request sem status → status='open'
  - Request com status → usa valor

- [ ] **CA-08**: Ticket criado com `created_at` = now
  - Timestamp presente na resposta
  - Formato ISO 8601

- [ ] **CA-09**: Ticket persistido no repositório
  - `repo.list_all()` contém ticket criado
  - Recuperável por ID

### Testes

- [ ] **CA-10**: Testes unitários do handler
  - Mock `TicketRepository`
  - Valida lógica de criação isolada

- [ ] **CA-11**: Testes de integração da rota
  - Use `TestClient` do FastAPI
  - POST com payload válido → 201 + TicketResponse
  - POST com payload inválido → 422

- [ ] **CA-12**: Todos os testes passam
  - `uv run pytest -v` → 20+ tests passing

---

## Fluxo Esperado

### Cenário Positivo: Criar Ticket Válido

```http
POST /api/v1/tickets HTTP/1.1
Content-Type: application/json

{
  "title": "Printer offline in Floor 3",
  "description": "The office printer in Floor 3 is not responding to print jobs.",
  "category": "hardware",
  "priority": "high"
}
```

**Resposta:**
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "number": 1,
  "title": "Printer offline in Floor 3",
  "description": "The office printer in Floor 3 is not responding to print jobs.",
  "category": "hardware",
  "status": "open",
  "priority": "high",
  "created_at": "2026-04-26T14:30:00Z"
}
```

### Cenário de Erro: Título Vazio

```http
POST /api/v1/tickets HTTP/1.1
Content-Type: application/json

{
  "title": "",
  "description": "Some description",
  "category": "hardware"
}
```

**Resposta:**
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

## Casos de Erro e Exceções

| Caso | HTTP | Resposta | Origem |
| --- | --- | --- | --- |
| Title vazio | 422 | Pydantic validation | `TicketCreate` schema |
| Description vazio | 422 | Pydantic validation | `TicketCreate` schema |
| Category inválida | 422 | Pydantic validation | Enum check |
| Status inválida | 422 | Pydantic validation | Enum check |
| Priority inválida | 422 | Pydantic validation | Enum check |
| Repo unavailable (futuro) | 500 | Internal Server Error | Infrastructure |
| DB connection error (futuro) | 503 | Service Unavailable | Infrastructure |

---

## Dependências

### Dependências de Outras Features

| Feature | O Que Reutiliza |
| --- | --- |
| **F008** | `TicketCreate` schema (validação) |
| **F009** | `InMemoryTicketRepository` (persistência) |
| **F009** | `Ticket` entity dataclass |
| **F007** | `TicketStatus`, `TicketPriority`, `TicketCategory` enums |

### Dependências Técnicas

- `FastAPI` — framework web (já instalado)
- `Pydantic` — validação (já instalado)
- `mediatr>=0.9` — dispatch de commands (já instalado)
- `Python 3.10+` (projeto requirement)

### Sem Dependências

- ❌ Não precisa de banco de dados (F009 = em memória)
- ❌ Não precisa de autenticação (F012+)
- ❌ Não precisa de logging centralizado (F014+)

---

## Impacto Técnico

### Módulos Afetados

| Camada | Módulo | Ação |
| --- | --- | --- |
| **application/** | `tickets/commands/create_ticket.py` | ✅ **Novo** |
| **api/routes/** | `tickets.py` | ✅ **Implementa** (ficheiro vazio existe) |
| **api/schemas/** | `tickets.py` | ✅ Reutiliza (`TicketCreate`, `TicketResponse`) |
| **domain/** | Entities, enums, repositories | ✅ Reutiliza (F009) |
| **infrastructure/** | Repositories | ✅ Reutiliza (InMemoryTicketRepository) |

### Estrutura de Ficheiros

```
src/
├── application/tickets/
│   └── commands/
│       └── create_ticket.py              ← NOVO
├── api/
│   ├── routes/
│   │   └── tickets.py                    ← IMPLEMENTA
│   └── schemas/
│       └── tickets.py                    ← (não muda)
├── domain/
│   ├── entities/ticket.py                ← (não muda)
│   ├── enums/ticket.py                   ← (não muda)
│   └── repositories/ticket.py            ← (não muda)
└── infrastructure/repositories/
    └── ticket.py                         ← (não muda)

tests/
├── unit/application/tickets/commands/
│   └── test_create_ticket.py             ← NOVO
└── integration/api/
    └── test_tickets.py                   ← NOVO
```

### Camadas de Arquitetura Afetadas

- ✅ **API Layer**: Nova rota POST
- ✅ **Application Layer**: Novo command + handler
- ✅ **Domain Layer**: Nenhuma mudança (reutiliza Ticket, enums)
- ✅ **Infrastructure Layer**: Nenhuma mudança (reutiliza InMemoryTicketRepository)

### Design Patterns

- ✅ **mediatr/CQRS**: Command + Handler para escrita
- ✅ **Repository Pattern**: Abstração via ABC, injeção
- ✅ **Dependency Injection**: Handler recebe repo no `__init__`
- ✅ **Data Transfer Object (DTO)**: `TicketCreate` (request), `TicketResponse` (response)

---

## Estratégia de Implementação

### Passo 1: Criar Command + Handler (5 min)

**Ficheiro:** `src/application/tickets/commands/create_ticket.py`

```python
from dataclasses import dataclass
from mediatr import GenericRequest
from domain.entities import Ticket
from domain.repositories import TicketRepository
from domain.enums import TicketCategory, TicketPriority, TicketStatus


@dataclass
class CreateTicketCommand(GenericRequest[Ticket]):
    title: str
    description: str
    category: str
    status: str = "open"
    priority: str = "medium"


class CreateTicketHandler:
    def __init__(self, repo: TicketRepository) -> None:
        self._repo = repo

    async def handle(self, request: CreateTicketCommand) -> Ticket:
        ticket = Ticket(
            title=request.title,
            description=request.description,
            category=TicketCategory(request.category),
            status=TicketStatus(request.status),
            priority=TicketPriority(request.priority),
        )
        return self._repo.save(ticket)
```

### Passo 2: Implementar Rota (5 min)

**Ficheiro:** `src/api/routes/tickets.py`

```python
from fastapi import APIRouter, Depends
from api.schemas.tickets import TicketCreate, TicketResponse
from domain.repositories import TicketRepository
from infrastructure.repositories import InMemoryTicketRepository
from application.tickets.commands.create_ticket import CreateTicketCommand, CreateTicketHandler

router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_ticket_repository() -> TicketRepository:
    # TODO: Injeta repositório real (PostgreSQL no futuro)
    return InMemoryTicketRepository()


@router.post("/", status_code=201, response_model=TicketResponse)
async def create_ticket(
    data: TicketCreate,
    repo: TicketRepository = Depends(get_ticket_repository),
) -> TicketResponse:
    handler = CreateTicketHandler(repo)
    ticket = await handler.handle(CreateTicketCommand(
        title=data.title,
        description=data.description,
        category=data.category.value,
        status=data.status.value,
        priority=data.priority.value,
    ))
    return TicketResponse.model_validate(ticket)


@router.get("/", response_model=list[TicketResponse])
async def list_tickets(
    repo: TicketRepository = Depends(get_ticket_repository),
) -> list[TicketResponse]:
    # TODO: F011 - Implement ListTicketsQuery
    tickets = repo.list_all()
    return [TicketResponse.model_validate(t) for t in tickets]
```

### Passo 3: Implementar Testes Unitários (10 min)

**Ficheiro:** `tests/unit/application/tickets/commands/test_create_ticket.py`

```python
from uuid import UUID
from domain.entities import Ticket
from domain.enums import TicketCategory, TicketPriority, TicketStatus
from domain.repositories import TicketRepository
from application.tickets.commands.create_ticket import CreateTicketCommand, CreateTicketHandler


class MockTicketRepository(TicketRepository):
    def __init__(self):
        self.saved = []

    def save(self, ticket: Ticket) -> Ticket:
        ticket.id = UUID("00000000-0000-0000-0000-000000000001")
        ticket.number = 1
        self.saved.append(ticket)
        return ticket

    def list_all(self):
        return self.saved


def test_handler_creates_ticket_with_valid_data():
    repo = MockTicketRepository()
    handler = CreateTicketHandler(repo)
    
    command = CreateTicketCommand(
        title="Test ticket",
        description="Test description",
        category="hardware",
        status="open",
        priority="high",
    )
    
    ticket = handler.handle(command)
    
    assert ticket.title == "Test ticket"
    assert ticket.status == TicketStatus.OPEN
    assert len(repo.saved) == 1
```

### Passo 4: Implementar Testes de Integração (10 min)

**Ficheiro:** `tests/integration/api/test_tickets.py`

```python
from fastapi.testclient import TestClient
from src.main import create_app


def test_post_create_ticket_returns_201():
    app = create_app()
    client = TestClient(app)
    
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "Printer offline",
            "description": "Floor 3 printer broken",
            "category": "hardware",
            "priority": "high",
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Printer offline"
    assert "id" in data
    assert "number" in data
    assert data["status"] == "open"


def test_post_create_ticket_rejects_empty_title():
    app = create_app()
    client = TestClient(app)
    
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "",
            "description": "Some description",
            "category": "hardware",
        },
    )
    
    assert response.status_code == 422
```

### Passo 5: Validar Testes (5 min)

```bash
uv run pytest tests/unit/application/tickets/commands/ -v
uv run pytest tests/integration/api/test_tickets.py -v
uv run pytest -v  # Todos os testes devem passar
```

---

## Estratégia de Testes

### Testes Unitários (Handler Isolado)

**Ficheiro:** `tests/unit/application/tickets/commands/test_create_ticket.py`

- ✅ Handler com mock de repositório
- ✅ Valida criação de entidade
- ✅ Valida persistência via mock

**Casos a cobrir:**
1. Criar ticket válido → retorna Ticket com id, number, created_at
2. Payload válido → repositório.save() é chamado
3. Status default → "open" se não enviado

### Testes de Integração (Rota Completa)

**Ficheiro:** `tests/integration/api/test_tickets.py`

- ✅ HTTP POST com `TestClient`
- ✅ Valida validação Pydantic (422)
- ✅ Valida resposta JSON (201 + TicketResponse)
- ✅ Usa `InMemoryTicketRepository` real

**Casos a cobrir:**
1. POST válido → 201 + JSON correto
2. Título vazio → 422
3. Descrição vazia → 422
4. Categoria inválida → 422
5. Status inválido → 422
6. Priority inválida → 422

### Cobertura Esperada

- Handler: 100% (casos positivo + edge)
- Rota: 100% (sucesso + validação)
- Integration: 5+ cenários

---

## Observabilidade

### Logs (Fase 1: Simples)

Não será implementado nesta fase (F014+). Estrutura preparada para:
- `logger.info(f"Ticket created: id={ticket.id}, number={ticket.number}")`

### Logs (Futuro, F014+)

- Criar ticket (INFO)
- Erro de validação (WARN)
- Erro de persistência (ERROR)

### Métricas (Futuro, F015+)

- Tickets criados por minuto
- Taxa de erro de validação
- Latência de criação

### Alertas (Futuro, F015+)

- Taxa de erro > 5% (ACTION)
- Latência > 1s (WARN)

---

## Riscos

### Risco 1: Injeção de Dependência Incorreta
**Probabilidade:** Média | **Impacto:** Alto

- **Descrição**: Rota não injeta repositório corretamente, handler recebe None
- **Mitigação**: Testes de integração com `TestClient` validam stack completo
- **Contingência**: Mock de repositório no teste unitário detecta problemas

### Risco 2: Status Default não Respeita Domínio
**Probabilidade:** Baixa | **Impacto:** Médio

- **Descrição**: Status default '`open`' é hardcoded em vez de constante
- **Mitigação**: Usar enum `TicketStatus.OPEN` ou padrão em schema
- **Contingência**: Testes validam status='open'

### Risco 3: Validação Duplicada
**Probabilidade:** Baixa | **Impacto:** Baixo

- **Descrição**: Validação em Pydantic + Handler (redundante)
- **Mitigação**: Reutilizar `TicketCreate` schema, handler só orquestra
- **Contingência**: Handler não re-valida, confia em Pydantic

### Risco 4: Concorrência com InMemoryRepository
**Probabilidade:** Baixa | **Impacto:** Médio

- **Descrição**: Número sequencial pode não ser thread-safe em memória
- **Mitigação**: F009 (`InMemoryTicketRepository`) já implementa contador isolado por instância
- **Contingência**: Testes validam que cada repo tem contador independente

---

## Dúvidas em Aberto

1. **Como lidar com status default?**
   - Opção A: `TicketCreate` tem `status='open'` default
   - Opção B: `CreateTicketCommand` força status='open' no handler
   - **Recomendação**: Opção A (schema responsável pelo default)

2. **O handler deve ser async ou sync?**
   - Hoje: Pode ser sync (F009 é em memória)
   - Futuro: Deve ser async (F014 com PostgreSQL)
   - **Recomendação**: Deixar como async agora, pronto para evoluir

3. **GET /api/v1/tickets (listar) é parte de F010?**
   - **Resposta**: Não. É F011 (`ListTicketsQuery`). F010 é apenas POST.
   - Nota: Spec deixa espaço para GET em `tickets.py` (placeholder para F011)

---

## Referências

- **Issue**: #13 — https://github.com/michelgomessilva/helpdesk-hub-api/issues/13
- **PR**: — (será preenchido após merge)
- **Docs**:
  - `docs/spec-driven-development.md` — Padrões de arquitetura, Git workflow
  - `docs/features/f008-create-schema-ticket.md` — `TicketCreate`, `TicketResponse`
  - `docs/features/f009-create-storage-inmemory-tickets.md` — `InMemoryTicketRepository`, Ticket entity
- **Código Existente**:
  - `src/application/tickets/commands/create_ticket.py` — Será criado
  - `src/api/routes/tickets.py` — Vazio, será implementado
  - `src/domain/entities/ticket.py` — Reutiliza
  - `src/infrastructure/repositories/ticket.py` — Reutiliza

---

## Histórico de Decisões

| Data | Decisão | Justificativa |
| --- | --- | --- |
| 2026-04-26 | Spec criada automaticamente a partir da issue #13 | Script de import do GitHub |
| 2026-04-26 | **[REESCRITO]** Spec profissionalizada com mediatr/CQRS explícito | Alinhamento com padrões arquiteturais estabelecidos em F009 |
| 2026-04-26 | Handler async desde o início | Preparado para evolução a PostgreSQL (F014) |
| 2026-04-26 | GET /api/v1/tickets deixado para F011 | Separação clara de responsabilidades (POST ≠ GET) |

---

## Status da Spec

- ✅ **Requisitos claros**: RF01-RF09 definidos com detalhes
- ✅ **Critérios de aceitação testáveis**: CA-01 a CA-12 mensuráveis
- ✅ **Estratégia de implementação**: 5 passos concretos
- ✅ **Testes planejados**: Unitários + integração
- ✅ **Riscos identificados**: 4 riscos com mitigação
- ✅ **Dependências claras**: F008, F009 como pré-requisitos
- ✅ **Pronto para implementação**: Código exemplo incluído

**Aprovação necessária antes de iniciar**: ⏳ Aguardando validação
