# F013 - Implementar PATCH /api/v1/tickets/{id} (UpdateTicketCommand)

## Metadados

- ID: `F013`
- Status: `Draft`
- Criado em: `2026-04-26`
- Origem no GitHub: #16

## Resumo Executivo

Implementar endpoint `PATCH /api/v1/tickets/{id}` para atualizar parcialmente um ticket (status, prioridade, descrição). Padrão mediatr/CQRS com `UpdateTicketCommand` + handler. Retorna HTTP 200 + `TicketResponse` atualizado, ou HTTP 404 se não encontrado.

---

## Objetivo

Entregar endpoint que:
1. Receba UUID + payload parcial (opcional)
2. Valide campos atualizáveis
3. Orquestre atualização via comando
4. Retorna 200 + TicketResponse ou 404/422

---

## Escopo

### Incluído
- ✅ Command `UpdateTicketCommand` com campos opcionais
- ✅ Handler validando e persistindo
- ✅ Schema `TicketUpdate` (Pydantic)
- ✅ Rota PATCH /api/v1/tickets/{id}
- ✅ HTTP 200/404/422 apropriados
- ✅ Testes

### Fora de Escopo
- ❌ Atualizar title, category (imutáveis)
- ❌ Atualizar id, number, created_at (imutáveis)

---

## Campos Atualizáveis

| Campo | Tipo | Validação |
| --- | --- | --- |
| `status` | Enum | open, in-progress, closed |
| `priority` | Enum | low, medium, high |
| `description` | String | 1-2000 chars |

---

## Padrão Arquitetural

```python
@dataclass
class UpdateTicketCommand(GenericRequest[Ticket]):
    ticket_id: UUID
    status: str | None = None
    priority: str | None = None
    description: str | None = None

class UpdateTicketHandler:
    def __init__(self, repo: TicketRepository) -> None:
        self._repo = repo

    async def handle(self, request: UpdateTicketCommand) -> Ticket | None:
        tickets = self._repo.list_all()
        ticket = next((t for t in tickets if t.id == request.ticket_id), None)
        if not ticket:
            return None
        
        if request.status:
            ticket.status = TicketStatus(request.status)
        if request.priority:
            ticket.priority = TicketPriority(request.priority)
        if request.description:
            ticket.description = request.description
        
        return ticket
```

---

## Critérios de Aceitação

- [ ] **CA-01**: `UpdateTicketCommand` com campos opcionais
- [ ] **CA-02**: `TicketUpdate` schema em `api/schemas/tickets.py`
- [ ] **CA-03**: Handler implementado e testável
- [ ] **CA-04**: Rota PATCH /api/v1/tickets/{id}
- [ ] **CA-05**: Atualizar status → HTTP 200
- [ ] **CA-06**: Atualizar priority → HTTP 200
- [ ] **CA-07**: Atualizar description → HTTP 200
- [ ] **CA-08**: PATCH múltiplos → HTTP 200, todos atualizados
- [ ] **CA-09**: PATCH ID inexistente → HTTP 404
- [ ] **CA-10**: PATCH status inválido → HTTP 422
- [ ] **CA-11**: Testes unitários + integração
- [ ] **CA-12**: Todos testes passam

---

## Cenários

### Atualizar um Campo
```
PATCH /api/v1/tickets/550e8400...
{"status": "closed"}

HTTP/1.1 200 OK
{ "status": "closed", ... }
```

### Atualizar Múltiplos
```
PATCH /api/v1/tickets/550e8400...
{
  "status": "in-progress",
  "priority": "high",
  "description": "Updated"
}

HTTP/1.1 200 OK
{ ... todos atualizados ... }
```

### Não Encontrado
```
PATCH /api/v1/tickets/00000000...
{"status": "closed"}

HTTP/1.1 404 Not Found
{"detail": "Ticket not found"}
```

---

## Dependências

- Reutiliza F008-F012 (schemas, repositório, queries)

---

## Impacto Técnico

| Ficheiro | Ação |
| --- | --- |
| `application/tickets/commands/update_ticket.py` | ✅ **Novo** |
| `api/schemas/tickets.py` | ✅ **Adiciona TicketUpdate** |
| `api/routes/tickets.py` | ✅ **Adiciona rota PATCH** |

---

## Status

**Status: DRAFT** — Pronta para review
