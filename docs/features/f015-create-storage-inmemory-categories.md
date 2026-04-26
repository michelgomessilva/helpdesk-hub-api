# F015 - Implementar InMemory Storage para Categories

## Metadados

- ID: `F015`
- Status: `Draft`
- Criado em: `2026-04-26`
- Origem no GitHub: #10

## Resumo Executivo

Criar `Category` entity (dataclass) e `InMemoryCategoryRepository` para armazenar categorias em memória. Padrão idêntico a F009 (Ticket) mas para categoria. Base para F016 (GET /categories).

---

## Objetivo

Entregar:
1. `Category` dataclass com id, name, description, created_at
2. `CategoryRepository` ABC (interface)
3. `InMemoryCategoryRepository` implementação

---

## Escopo

### Incluído
- ✅ `Category` entity (dataclass)
- ✅ `CategoryRepository` ABC
- ✅ `InMemoryCategoryRepository` com UUID + counter
- ✅ Testes (7 casos, similar a F009)

### Fora de Escopo
- ❌ Rotas (F016)

---

## Implementação

**`domain/entities/category.py`:**
```python
@dataclass
class Category:
    name: str
    description: str | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
```

**`infrastructure/repositories/category.py`:**
```python
class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self):
        self._store: dict[UUID, Category] = {}

    def save(self, category: Category) -> Category:
        category.id = uuid4()
        category.created_at = datetime.utcnow()
        self._store[category.id] = category
        return category

    def list_all(self) -> list[Category]:
        return list(self._store.values())
```

---

## Critérios de Aceitação

- [ ] **CA-01**: `Category` entity em `domain/entities/category.py`
- [ ] **CA-02**: `CategoryRepository` ABC em `domain/repositories/category.py`
- [ ] **CA-03**: `InMemoryCategoryRepository` em `infrastructure/repositories/category.py`
- [ ] **CA-04**: `save()` gera UUID e timestamp
- [ ] **CA-05**: `list_all()` retorna todas as categorias
- [ ] **CA-06**: Testes isolamento de instâncias
- [ ] **CA-07**: 7 testes similares a F009
- [ ] **CA-08**: Todos testes passam

---

## Dependências

- F014 (Category schema)
- Padrão F009 como referência

---

## Implementação (2 passos, 15 min)

1. Entity + Repository ABC
2. InMemory implementation
3. Testes

---

## Status

**Status: DRAFT** — Pronta para review
