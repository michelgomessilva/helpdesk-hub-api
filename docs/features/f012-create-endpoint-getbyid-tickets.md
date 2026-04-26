# F012 - Implementar GET /api/v1/tickets/{id} (GetTicketByIdQuery)

## Metadados

- ID: `F012`
- Status: `Draft`
- Criado em: `2026-04-26`
- Origem no GitHub: #15

## Resumo Executivo

Implementar endpoint `GET /api/v1/tickets/{id}` para consultar um ticket específico por UUID. Padrão mediatr/CQRS com `GetTicketByIdQuery`. Retorna HTTP 200 + `TicketResponse` se existe, ou HTTP 404 se não encontrado.

---

## Objetivo

Entregar endpoint funcional que:
1. Receba UUID como path parameter
2. Valide UUID format
3. Busca no repositório
4. Retorna 200 + TicketResponse ou 404

---

## Escopo

### Incluído
- ✅ Query `GetTicketByIdQuery(id: UUID)`
- ✅ Handler buscando por ID
- ✅ Rota GET /api/v1/tickets/{id}
- ✅ HTTP 200 se existe
- ✅ HTTP 404 se não existe
- ✅ UUID validation automática (FastAPI)
- ✅ Testes unitários + integração

### Fora de Escopo
- ❌ Busca por número (será F012+)
- ❌ Busca por título/descrição (será F012+)

---

## Padrão Arquitetural

```python
@dataclass
class GetTicketByIdQuery(GenericRequest[Ticket]):
    ticket_id: UUID

class GetTicketByIdHandler:
    def __init__(self, repo: TicketRepository) -> None:
        self._repo = repo

    async def handle(self, request: GetTicketByIdQuery) -> Ticket | None:
        # Repositório retorna ticket ou None
        # Handler lida com lógica
        tickets = self._repo.list_all()
        return next((t for t in tickets if t.id == request.ticket_id), None)
```

**Rota:**
```python
@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: UUID,
    repo: TicketRepository = Depends(get_ticket_repository),
) -> TicketResponse:
    handler = GetTicketByIdHandler(repo)
    ticket = await handler.handle(GetTicketByIdQuery(ticket_id=ticket_id))
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketResponse.model_validate(ticket)
```

---

## Critérios de Aceitação

- [ ] **CA-01**: `GetTicketByIdQuery(ticket_id: UUID)` definido
- [ ] **CA-02**: Handler implementado e testável
- [ ] **CA-03**: Rota GET /api/v1/tickets/{id} implementada
- [ ] **CA-04**: UUID válido, existe → HTTP 200 + TicketResponse
- [ ] **CA-05**: UUID válido, não existe → HTTP 404 + `{"detail": "Ticket not found"}`
- [ ] **CA-06**: UUID inválido → HTTP 422 (validation error)
- [ ] **CA-07**: Testes unitários
- [ ] **CA-08**: Testes integração
- [ ] **CA-09**: Todos testes passam

---

## Cenários

### Ticket Existe
```
GET /api/v1/tickets/550e8400-e29b-41d4-a716-446655440000

HTTP/1.1 200 OK
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "number": 1,
  "title": "Printer offline",
  ...
}
```

### Ticket Não Existe
```
GET /api/v1/tickets/00000000-0000-0000-0000-000000000000

HTTP/1.1 404 Not Found
{"detail": "Ticket not found"}
```

### UUID Inválido
```
GET /api/v1/tickets/invalid-uuid

HTTP/1.1 422 Unprocessable Entity
{"detail": [{"loc": ["path", "ticket_id"], "msg": "invalid UUID format", ...}]}
```

---

## Dependências

- Reutiliza F009: `TicketRepository`, `Ticket`
- Reutiliza F008: `TicketResponse`

---

## Impacto Técnico

| Ficheiro | Ação |
| --- | --- |
| `application/tickets/queries/get_ticket_by_id.py` | ✅ **Novo** |
| `api/routes/tickets.py` | ✅ **Adiciona rota** |
| Tests | ✅ **Novo** |

---

## Implementação (2 passos, 10 min)

1. Query + Handler em `application/tickets/queries/get_ticket_by_id.py`
2. Rota em `api/routes/tickets.py` com `HTTPException(404)`
3. Testes com `TestClient`

---

## Testes

```python
def test_get_ticket_by_id_found():
    # POST ticket, GET por ID, valida resposta
    
def test_get_ticket_by_id_not_found():
    # GET ID inexistente, valida 404
    
def test_get_ticket_by_id_invalid_uuid():
    # GET com UUID inválido, valida 422
```

---

## Status

**Status: DRAFT** — Pronta para review
