# F016 - Implementar GET /api/v1/categories (ListCategoriesQuery)

## Metadados

- ID: `F016`
- Status: `Draft`
- Criado em: `2026-04-26`
- Origem no GitHub: #12

## Resumo Executivo

Implementar endpoint `GET /api/v1/categories` para listar todas as categorias. Padrão mediatr/CQRS com `ListCategoriesQuery` + handler. Idêntico a F011 (GET /tickets) mas para categorias. Retorna HTTP 200 + `list[CategoryResponse]`.

---

## Objetivo

Entregar endpoint que:
1. Recupera todas as categorias
2. Converte para `CategoryResponse`
3. Retorna HTTP 200 + array

---

## Escopo

### Incluído
- ✅ `ListCategoriesQuery`
- ✅ Handler
- ✅ Rota GET /api/v1/categories
- ✅ HTTP 200 + array (vazio ou com items)
- ✅ Testes

### Fora de Escopo
- ❌ Filtros (futuro)
- ❌ Paginação (futuro)

---

## Padrão Arquitetural

```python
@dataclass
class ListCategoriesQuery(GenericRequest[list[Category]]):
    pass

class ListCategoriesHandler:
    def __init__(self, repo: CategoryRepository) -> None:
        self._repo = repo

    async def handle(self, request: ListCategoriesQuery) -> list[Category]:
        return self._repo.list_all()
```

**Rota:**
```python
@router.get("/", response_model=list[CategoryResponse])
async def list_categories(
    repo: CategoryRepository = Depends(get_category_repository),
) -> list[CategoryResponse]:
    handler = ListCategoriesHandler(repo)
    categories = await handler.handle(ListCategoriesQuery())
    return [CategoryResponse.model_validate(c) for c in categories]
```

---

## Critérios de Aceitação

- [ ] **CA-01**: `ListCategoriesQuery` definido
- [ ] **CA-02**: Handler implementado
- [ ] **CA-03**: Rota GET /api/v1/categories
- [ ] **CA-04**: GET vazio → HTTP 200 + `[]`
- [ ] **CA-05**: GET com categorias → HTTP 200 + array
- [ ] **CA-06**: Testes unitários
- [ ] **CA-07**: Testes integração
- [ ] **CA-08**: Todos testes passam

---

## Cenários

### Lista Vazia
```
GET /api/v1/categories
HTTP/1.1 200 OK
[]
```

### Com Categorias
```
GET /api/v1/categories
HTTP/1.1 200 OK
[
  {
    "id": "550e8400...",
    "name": "Hardware",
    "description": "Hardware issues",
    "created_at": "2026-04-26T14:30:00Z"
  },
  ...
]
```

---

## Dependências

- F014 (CategoryResponse schema)
- F015 (InMemoryCategoryRepository)
- F011 (padrão GetCategoriesQuery como referência)

---

## Implementação (3 passos, 10 min)

1. Query + Handler em `application/categories/queries/list_categories.py`
2. Rota em `api/routes/categories.py`
3. Testes

---

## Status

**Status: DRAFT** — Pronta para review
