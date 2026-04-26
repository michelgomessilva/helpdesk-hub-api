# F009 - Criar armazenamento em memória para tickets

## Metadados

- ID: `F009`
- Status: `Done`
- Owner:
- Criado em: `2026-04-26`
- Atualizado em: `2026-04-26`
- Origem no GitHub: #11 - https://github.com/michelgomessilva/helpdesk-hub-api/issues/11
- Responsaveis tecnicos:

## Resumo

Implementar a camada de armazenamento em memória para tickets, com entidade `Ticket` contendo identificação técnica via UUID e identificação legível via número sequencial, seguindo o padrão Repository para isolar a persistência da lógica de domínio.

## Problema

O projeto possui schemas de entrada e saída para tickets (F008), mas ainda não tem uma entidade de domínio nem um mecanismo de armazenamento. Sem isso, nenhuma rota de CRUD pode ser implementada. O armazenamento em memória é a primeira etapa antes da persistência real em banco de dados.

## Objetivo

Criar a entidade `Ticket` no domínio e uma implementação `InMemoryTicketRepository` que permita criar e listar tickets em memória, servindo de base para os endpoints de CRUD da F010 em diante.

## Escopo

- Criar a entidade `Ticket` na camada de domínio com todos os campos necessários
- Definir `id` como UUID (identificador técnico, imutável)
- Definir `number` como inteiro sequencial gerado automaticamente (identificador legível pelo utilizador)
- Criar interface abstrata `TicketRepository` na camada de domínio
- Implementar `InMemoryTicketRepository` na camada de infraestrutura
- Cobrir a implementação com testes automatizados (TDD)

## Fora de Escopo

- Persistência em banco de dados (PostgreSQL/SQLAlchemy — previsto para F012+)
- Endpoints HTTP de CRUD de tickets (previsto para F010)
- Autenticação e autorização
- Paginação e filtros
- Associação de tickets a utilizadores

## Personas ou Usuarios Impactados

- **Utilizadores do helpdesk**: Referenciam seus chamados pelo número legível (`#42`) em vez de um UUID opaco
- **Time de desenvolvimento**: Consome o repositório para implementar os endpoints de tickets
- **Futuras features**: F010 (CRUD de tickets), F012 (persistência), F013 (filtros e paginação)

## Contexto de Negocio

- Label importada: `feature`
- Label importada: `tickets`
- Label importada: `priority: high`
- Label importada: `week-2`

Sistemas de helpdesk reais (Jira, Zendesk, GitHub Issues) sempre expõem dois identificadores distintos:

- **Identificador técnico (UUID)**: Imutável, único globalmente, usado em URLs e referências internas entre sistemas. Impossível de adivinhar, seguro para expor em APIs públicas.
- **Número de ticket (#N)**: Sequencial, curto, legível. Usado na comunicação com o utilizador ("Abri o chamado #42"). Facilita suporte, auditoria e busca rápida.

Esta decisão deve ser tomada agora, antes de qualquer rota ser criada, pois impacta o contrato da API e os schemas de resposta.

## Requisitos Funcionais

- RF01: A entidade `Ticket` deve ter `id` como UUID gerado automaticamente no momento da criação
- RF02: A entidade `Ticket` deve ter `number` como inteiro sequencial legível, incrementado por chamado criado no repositório
- RF03: O repositório deve expor operações de `save(ticket)` e `list_all()` como contrato mínimo
- RF04: O repositório em memória deve preservar os tickets entre chamadas dentro do mesmo ciclo de vida da aplicação
- RF05: A criação de um ticket deve preencher automaticamente `id`, `number` e `created_at`

## Requisitos Nao Funcionais

- RNF01: O `InMemoryTicketRepository` deve ser substituível por um `PostgresTicketRepository` no futuro sem alterar as camadas superiores (Liskov + Dependency Inversion)
- RNF02: A geração de UUID deve usar `uuid4` (aleatório), nunca baseada em timestamp ou sequência previsível
- RNF03: O número sequencial deve ser gerado e controlado pelo repositório, não pelo chamador
- RNF04: A entidade `Ticket` deve ser imutável após criação (campos de identidade não mutáveis externamente)
- RNF05: Todos os campos da entidade devem ter tipos explícitos (sem `Any`)

## Diretrizes Arquiteturais

- **Clean Architecture**: A entidade `Ticket` e a interface `TicketRepository` vivem na camada de **domínio**. A implementação `InMemoryTicketRepository` vive na camada de **infraestrutura**. Os endpoints (F010) consumirão via injeção de dependência, nunca instanciando a implementação diretamente.
- **SOLID**: `TicketRepository` é uma abstração (interface/classe abstrata). A implementação em memória depende dessa abstração, não ao contrário. Futuras implementações (PostgreSQL) seguirão o mesmo contrato sem alterar o domínio.
- **DRY**: A lógica de geração de `id` e `number` fica centralizada no repositório, não espalhada em múltiplos lugares.
- **Guard Clauses**: O repositório deve validar entradas inválidas (ticket nulo, campo obrigatório ausente) antes de processar.
- **Middlewares**: Não aplicável nesta entrega.
- **Design Patterns**: Padrão **Repository** para isolar o acesso a dados do domínio. O repositório em memória age como um `fake` substituível por um repositório real em futuras fases.

## Criterios de Aceitacao

- [ ] A entidade `Ticket` existe na camada de domínio com todos os campos: `id` (UUID), `number` (int), `title`, `description`, `category`, `status`, `priority`, `created_at`
- [ ] `id` é sempre um UUID gerado automaticamente, nunca um inteiro
- [ ] `number` é um inteiro sequencial (1, 2, 3...) gerado e controlado pelo repositório
- [ ] A interface `TicketRepository` define os contratos `save` e `list_all`
- [ ] `InMemoryTicketRepository` implementa `TicketRepository` e persiste tickets em memória
- [ ] Dois tickets criados em sequência têm `number` 1 e 2 respectivamente
- [ ] Dois tickets criados em sequência têm `id`s diferentes (UUIDs únicos)
- [ ] Testes automatizados cobrem criação, listagem, geração de UUID e incremento de número

## Fluxo Esperado

1. A camada de aplicação recebe um `TicketCreate` (schema de entrada da F008)
2. Instancia a entidade `Ticket` com os dados fornecidos
3. Chama `repository.save(ticket)`
4. O repositório gera `id` (UUID4) e `number` (próximo inteiro sequencial) e `created_at`
5. O ticket é armazenado no dicionário interno `_store: Dict[UUID, Ticket]`
6. A camada de aplicação retorna o ticket criado mapeado para `TicketResponse`

## Casos de Erro e Excecoes

- Tentar criar um ticket com `title` vazio deve falhar na validação do schema (já coberto pela F008, não pelo repositório)
- Tentar criar um ticket com `category` ou `priority` inválidos falha no schema (já coberto)
- O repositório em memória não precisa lidar com concorrência nesta fase (sem persistência, sem threads concorrentes)
- `list_all()` num repositório vazio deve retornar lista vazia, não lançar exceção

## Dependencias

- **F007**: Enums `TicketStatus`, `TicketPriority`, `TicketCategory` já definidos no domínio
- **F008**: Schema `TicketCreate` e `TicketResponse` já implementados — a entidade `Ticket` deve ser compatível com esses contratos
- **Python `uuid`**: Módulo nativo, sem dependência externa adicional
- **Python `datetime`**: Módulo nativo para `created_at`

## Impacto Tecnico

- **Módulos afetados**: `src/domain/` (entidade + interface), `src/infrastructure/` (implementação em memória)
- **Entidades envolvidas**: `Ticket` (nova entidade de domínio)
- **APIs, filas, jobs ou integrações**: Nenhuma nesta entrega — apenas a camada de dados interna
- **Migrações ou mudanças de infraestrutura**: Nenhuma — armazenamento em memória sem persistência
- **Camadas afetadas na arquitetura**:
  - `domain/` → entidade `Ticket` + interface abstrata `TicketRepository`
  - `infrastructure/` → `InMemoryTicketRepository`
- **Necessidade de middlewares**: Não aplicável
- **Design patterns adotados**: Repository Pattern — desacopla lógica de negócio do mecanismo de armazenamento

## Estrategia de Implementacao

1. Criar a entidade `Ticket` em `src/domain/ticket.py` com campos tipados usando `dataclass` ou Pydantic BaseModel (sem herança de esquemas de API)
2. Criar a interface `TicketRepository` em `src/domain/repositories.py` como classe abstrata (`ABC`) com métodos `save` e `list_all`
3. Criar `InMemoryTicketRepository` em `src/infrastructure/ticket_repository.py` com dicionário interno `_store: Dict[UUID, Ticket]` e contador `_next_number: int`
4. Garantir que `save()` gera `id`, `number` e `created_at` automaticamente antes de armazenar
5. Escrever testes em `tests/test_ticket_repository.py` cobrindo todos os critérios de aceitação

## Estrategia de Testes

- **Criação básica**: Criar um ticket e verificar que `id` é UUID, `number` é 1 e os campos estão corretos
- **Sequência de números**: Criar dois tickets e verificar que os `number`s são 1 e 2
- **Unicidade de UUID**: Criar dois tickets e verificar que os `id`s são diferentes
- **Listagem**: Criar N tickets e verificar que `list_all()` retorna todos com os dados corretos
- **Lista vazia**: Verificar que `list_all()` num repositório recém-criado retorna lista vazia sem erros
- **Isolamento entre instâncias**: Dois repositórios distintos devem ter contadores independentes

## Observabilidade

- Não aplicável nesta fase — armazenamento em memória sem logging ou métricas
- Na futura migração para banco de dados, esta camada será substituída e logs de queries serão adicionados

## Riscos

- **Perda de dados ao reiniciar**: Armazenamento em memória não persiste entre reinicializações da aplicação — aceitável e esperado nesta fase
- **Conflito de contrato com F010**: Se os endpoints de tickets assumirem `id` como inteiro, precisarão ser ajustados para UUID. A decisão de UUID deve ser comunicada antes da implementação da F010
- **Acoplamento prematuro**: Evitar que os endpoints (F010) instanciem diretamente `InMemoryTicketRepository` — usar injeção de dependência desde o início

## Duvidas em Aberto

- O `number` deve ser global (único por sistema) ou por categoria? **Decisão inicial**: global e sequencial simples
- A entidade `Ticket` deve usar `dataclass`, Pydantic `BaseModel` ou classe simples? **Decisão recomendada**: `dataclass` com tipos explícitos, sem acoplamento com Pydantic (que fica na camada de API)

## Referencias

- Issue / Task: #11 - https://github.com/michelgomessilva/helpdesk-hub-api/issues/11
- PR:
- Documentacao: docs/spec-driven-development.md
- F007: docs/features/f007-create-enums-status-priority.md
- F008: docs/features/f008-create-schema-ticket.md

## Historico de Decisoes

- 2026-04-26 - Spec criada automaticamente a partir da issue #11.
- 2026-04-26 - Decisão: IDs de tickets serão UUID (uuid4), não inteiros sequenciais. Motivo: unicidade global, segurança e padrão de mercado em APIs REST.
- 2026-04-26 - Decisão: Campo `number` adicionado como inteiro sequencial legível para referência humana (ex: "chamado #42"). Gerado e controlado pelo repositório.
- 2026-04-26 - Decisão: Padrão Repository adotado desde esta fase para garantir substituibilidade quando PostgreSQL for introduzido.
- 2026-04-26 - Implementação completada: Entidade `Ticket` criada em `src/domain/ticket.py`, interface `TicketRepository` em `src/domain/repositories.py`, `InMemoryTicketRepository` em `src/infrastructure/ticket_repository.py`. TicketResponse atualizado com `id: UUID` e `number: int`. 7 testes novos adicionados, todos passando (20/20 testes do projeto).

## Conteudo Importado do GitHub

### Titulo Original

Criar armazenamento em memória para tickets

### Labels

- feature
- tickets
- priority: high
- week-2

### Descricao Original

## Contexto
Criar estrutura temporária em memória para armazenar tickets.

## O que deve ser feito
- [ ] Definir lista ou dicionário de tickets
- [ ] Garantir geração simples de ids

## Critérios de aceite
- [ ] Tickets podem ser criados e listados
- [ ] Armazenamento em memória funcional

## Observações técnicas
Pode usar incremento simples de id.
