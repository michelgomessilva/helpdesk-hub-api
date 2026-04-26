# F014 - Criar Schema Category (Pydantic DTO)

## Metadados

- ID: `F014`
- Status: `Ready`
- Criado em: `2026-04-26`
- Origem no GitHub: #8

## Resumo Executivo

Criar Pydantic schemas `CategoryCreate` e `CategoryResponse` para validar e serializar categorias. Similar a F008 (TicketCreate/TicketResponse) mas para categoria. Foundational para F015 (repositório) e F016 (GET /categories).

---

## Objetivo

Entregar schemas que:
1. Validem entrada (CategoryCreate)
2. Serializam resposta (CategoryResponse)
3. Reutilizáveis em todas rotas de categoria

---

## Escopo

### Incluído
- ✅ `CategoryCreate` schema (validação entrada)
- ✅ `CategoryResponse` schema (serialização resposta)
- ✅ Validação de nome (min/max length)
- ✅ Validação de descrição (opcional)
- ✅ Testes

### Fora de Escopo
- ❌ Persistência (F015)
- ❌ Rotas (F016+)

---

## Schemas

```python
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    created_at: datetime
```

---

## Critérios de Aceitação

- [ ] **CA-01**: `CategoryCreate` schema com validação
- [ ] **CA-02**: `CategoryResponse` schema com id, name, description, created_at
- [ ] **CA-03**: Validação: nome 1-100 chars
- [ ] **CA-04**: Validação: descrição opcional, max 500 chars
- [ ] **CA-05**: Nome vazio → 422
- [ ] **CA-06**: Descrição > 500 chars → 422
- [ ] **CA-07**: Testes validação
- [ ] **CA-08**: Todos testes passam

---

## Dependências

- Reutiliza Pydantic (já instalado)
- Padrão similar a F008 (TicketCreate/Response)

---

## Implementação (2 passos, 5 min)

1. Criar `api/schemas/category.py` com 2 classes
2. Testes de validação
3. `uv run pytest`

---

## Status

**Status: DRAFT** — Pronta para review
