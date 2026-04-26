# F011 - Implementar GET /api/v1/tickets (ListTicketsQuery)

## Metadados

- ID: `F011`
- Status: `Ready`
- Criado em: `2026-04-26`
- Origem no GitHub: #14 - https://github.com/michelgomessilva/helpdesk-hub-api/issues/14

## Resumo Executivo

Implementar endpoint HTTP `GET /api/v1/tickets` para listar todos os tickets armazenados. Segue o padrão **mediatr/CQRS** com `ListTicketsQuery` + handler. Retorna `list[TicketResponse]` com status HTTP 200. Trata lista vazia gracefully (retorna `[]`).

---

## Contexto

- F010 implementou POST (escrita)
- F011 agora implementa GET para leitura
- Complementa o CRUD básico
- Base para F012+ com filtros/paginação

---

## Objetivo

Entregar endpoint funcional `GET /api/v1/tickets` que:
1. Recupera todos os tickets da memória
2. Converte para `TicketResponse` (DTO)
3. Retorna HTTP 200 + JSON array

---

## Escopo

### Incluído
- ✅ Criar `ListTicketsQuery` em `application/tickets/queries/list_tickets.py`
- ✅ Implementar `ListTicketsHandler` 
- ✅ Rota GET /api/v1/tickets delegando ao mediator
- ✅ Retorno HTTP 200 + array vazio se nenhum ticket
- ✅ Testes unitários + integração

### Fora de Escopo
- ❌ Filtros (status, prioridade, categoria) — F012+
- ❌ Paginação — F012+
- ❌ Ordenação — F012+
- ❌ Busca textual — F012+

---

## Padrão Arquitetural: mediatr/CQRS (Query)

```python
# application/tickets/queries/list_tickets.py
@dataclass
class ListTicketsQuery(GenericRequest[list[Ticket]]):
    pass  # Sem parâmetros — lista tudo

class ListTicketsHandler:
    def __init__(self, repo: TicketRepository) -> None:
        self._repo = repo

    async def handle(self, request: ListTicketsQuery) -> list[Ticket]:
        return self._repo.list_all()
```

**Rota:**
```python
@router.get("/", response_model=list[TicketResponse])
async def list_tickets(
    repo: TicketRepository = Depends(get_ticket_repository),
) -> list[TicketResponse]:
    handler = ListTicketsHandler(repo)
    tickets = await handler.handle(ListTicketsQuery())
    return [TicketResponse.model_validate(t) for t in tickets]
```

---

## Critérios de Aceitação

- [ ] **CA-01**: `ListTicketsQuery` definido em `application/tickets/queries/`
- [ ] **CA-02**: `ListTicketsHandler` recebe `TicketRepository` via `__init__`
- [ ] **CA-03**: Rota GET /api/v1/tickets implementada
- [ ] **CA-04**: GET vazio retorna HTTP 200 + `[]`
- [ ] **CA-05**: GET com 1+ tickets retorna HTTP 200 + array correto
- [ ] **CA-06**: Resposta é `list[TicketResponse]` (não raw entities)
- [ ] **CA-07**: Testes unitários do handler
- [ ] **CA-08**: Testes integração da rota
- [ ] **CA-09**: Todos os testes passam

---

## Cenários Esperados

### Lista Vazia
```
GET /api/v1/tickets HTTP/1.1

HTTP/1.1 200 OK
[]
```

### Com Tickets
```
GET /api/v1/tickets HTTP/1.1

HTTP/1.1 200 OK
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "number": 1,
    "title": "Printer offline",
    "description": "...",
    "category": "hardware",
    "status": "open",
    "priority": "high",
    "created_at": "2026-04-26T14:30:00Z"
  },
  { ... ticket 2 ... }
]
```

---

## Dependências

- **Reutiliza F008**: `TicketResponse` schema
- **Reutiliza F009**: `InMemoryTicketRepository`, `Ticket` entity
- **Reutiliza F010**: Padrão rota + mediator

---

## Impacto Técnico

| Camada | Ficheiro | Ação |
| --- | --- | --- |
| **application/** | `tickets/queries/list_tickets.py` | ✅ **Novo** |
| **api/routes/** | `tickets.py` | ✅ **Adiciona rota** |
| **tests/** | `unit/application/queries/test_list_tickets.py` | ✅ **Novo** |

---

## Estratégia de Implementação

### Passo 1: Query + Handler (3 min)
Criar `src/application/tickets/queries/list_tickets.py` com `ListTicketsQuery` e `ListTicketsHandler`.

### Passo 2: Rota (2 min)
Adicionar `@router.get("/", response_model=list[TicketResponse])` a `src/api/routes/tickets.py`.

### Passo 3: Testes (5 min)
- Unitários: handler com mock repo
- Integração: GET vazio + GET com tickets

### Passo 4: Validar (2 min)
```bash
uv run pytest -v
```

---

## Testes

**Unitários**: Handler isolado
```python
def test_handler_returns_all_tickets():
    repo = MockTicketRepository()
    repo.save(Ticket(...))  # Salva 1 ticket
    handler = ListTicketsHandler(repo)
    tickets = handler.handle(ListTicketsQuery())
    assert len(tickets) == 1
```

**Integração**: Rota completa
```python
def test_get_tickets_returns_200_with_empty_list():
    client = TestClient(app)
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200
    assert response.json() == []

def test_get_tickets_returns_created_ticket():
    client = TestClient(app)
    client.post("/api/v1/tickets", json={...})  # F010
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200
    assert len(response.json()) == 1
```

---

## Riscos

| Risco | Probabilidade | Mitigação |
| --- | --- | --- |
| Resposta HTTP deve ser array, não objeto | Baixa | `response_model=list[TicketResponse]` force isso |
| Performance com muitos tickets | Baixa | F009 em memória, para poucos registros |

---

## Histórico de Decisões

| Data | Decisão |
| --- | --- |
| 2026-04-26 | Spec criada automaticamente (placeholder) |
| 2026-04-26 | **[REESCRITO]** Profissionalizada com mediatr/CQRS Query |

---

## Status

**Status: DRAFT** — Pronta para review e ajustes
