# F008 - Criar schema de Ticket

## Metadados

- ID: `F008`
- Status: `Done`
- Owner:
- Criado em: `2026-04-05`
- Atualizado em: `2026-04-22`
- Origem no GitHub: #9 - https://github.com/michelgomessilva/helpdesk-hub-api/issues/9
- Responsaveis tecnicos:

## Resumo

Criar schemas de entrada e saida para tickets usando Pydantic, com validacao tipada para titulo, descricao, categoria, prioridade e status.

## Problema

O projeto precisava de contratos claros para tickets, separando payload de criacao e payload de resposta, com validacao consistente e reutilizavel.

## Objetivo

Disponibilizar schemas `TicketCreate` e `TicketResponse` que padronizem o formato dos tickets e garantam validacao automatica via Pydantic.

## Escopo

- Criar schema de criacao de ticket
- Criar schema de resposta de ticket
- Validar titulo, descricao, prioridade e categoria
- Schemas criados
- Validacao funcionando
- Respostas consistentes

## Fora de Escopo

- Persistencia em banco de dados
- Endpoints de CRUD de tickets
- Regras de negocio avancadas de transicao de status

## Personas ou Usuarios Impactados

- Time de desenvolvimento
- Futuras rotas de tickets
- Revisores tecnicos

## Contexto de Negocio

- Label importada: feature
- Label importada: tickets
- Label importada: priority: high
- Label importada: week-2
- Schemas de request e response devem ficar separados.

## Requisitos Funcionais

- RF01: Criar schema de criacao de ticket
- RF02: Criar schema de resposta de ticket
- RF03: Validar titulo, descricao, prioridade e categoria

## Requisitos Nao Funcionais

- RNF01: Os schemas devem ser reutilizaveis nas futuras rotas de tickets.
- RNF02: Valores invalidos devem ser rejeitados automaticamente.
- RNF03: A modelagem deve manter separacao clara entre dominio e contratos Pydantic.

## Diretrizes Arquiteturais

- Clean Architecture: Enums permanecem no dominio e os schemas usam esses tipos sem mover regra de negocio para a camada de API.
- SOLID: Separacao de responsabilidades entre enums de dominio e contratos de entrada/saida.
- DRY: Categoria, status e prioridade reaproveitam definicoes centralizadas.
- Guard Clauses: Validacao basica delegada ao Pydantic com tipos e constraints declarativas.
- Middlewares: Nao aplicavel nesta entrega.
- Design Patterns: Uso de contratos explicitos de request/response para clareza e evolucao segura.

## Criterios de Aceitacao

- [x] Criar schema de criacao de ticket
- [x] Criar schema de resposta de ticket
- [x] Validar titulo, descricao, prioridade e categoria
- [x] Schemas criados
- [x] Validacao funcionando
- [x] Respostas consistentes

## Fluxo Esperado

1. O cliente monta um payload de ticket.
2. O schema `TicketCreate` valida os dados de entrada.
3. O sistema pode responder usando `TicketResponse` com contrato consistente.

## Casos de Erro e Excecoes

- Categoria invalida deve falhar na validacao.
- Prioridade invalida deve falhar na validacao.
- Status invalido deve falhar na validacao.
- Titulo vazio deve falhar na validacao.

## Dependencias

- Enums de ticket ja definidos no dominio
- Pydantic configurado no projeto

## Impacto Tecnico

- Modulos afetados: dominio e schemas
- Entidades envolvidas: ticket
- APIs, filas, jobs ou integracoes: nao aplicavel
- Migracoes ou mudancas de infraestrutura: nao aplicavel
- Camadas afetadas na arquitetura: dominio e contratos de entrada/saida
- Necessidade de middlewares: nao aplicavel
- Design patterns adotados ou descartados: separacao explicita entre request schema e response schema

## Estrategia de Implementacao

1. Expandir os enums de dominio com categoria.
2. Evoluir `TicketCreate` com validacoes declarativas.
3. Criar `TicketResponse` com contrato consistente.
4. Validar tudo com TDD.

## Estrategia de Testes

- Teste para valores validos em `TicketCreate`
- Teste para categoria invalida
- Teste para prioridade invalida
- Teste para status invalido
- Teste para titulo vazio
- Teste para contrato de `TicketResponse`

## Observabilidade

- Nao aplicavel nesta etapa

## Resultado da Implementacao

### Arquivos Implementados

1. **src/api/schemas/ticket.py**
   - `TicketCreate`: Schema para criacao de tickets com validacoes
     - `title`: str (min 1, max 120 caracteres)
     - `description`: str (min 1, max 2000 caracteres)
     - `category`: TicketCategory (enum validado)
     - `status`: TicketStatus (default: OPEN)
     - `priority`: TicketPriority (default: MEDIUM)
   - `TicketResponse`: Schema para resposta de consulta de tickets
     - `id`: int
     - `title`: str
     - `description`: str
     - `category`: TicketCategory
     - `status`: TicketStatus
     - `priority`: TicketPriority
     - `created_at`: datetime

### Testes Implementados

**Arquivo:** `tests/test_ticket_enums.py`

6 testes cobrindo todos os criterios de aceitacao:

1. ✅ `test_ticket_create_accepts_valid_status_and_priority_values` - Valida valores corretos
2. ✅ `test_ticket_create_rejects_invalid_status` - Rejeita status invalido
3. ✅ `test_ticket_create_rejects_invalid_priority` - Rejeita prioridade invalida
4. ✅ `test_ticket_create_rejects_invalid_category` - Rejeita categoria invalida
5. ✅ `test_ticket_create_rejects_blank_title` - Rejeita titulo em branco
6. ✅ `test_ticket_response_exposes_consistent_contract` - Valida contrato de resposta

### Status de Testes

- **Total de testes do projeto:** 13
- **Testes F008:** 6/6 passando ✅
- **Testes de cobertura:** 100% dos criterios de aceitacao
- **Suite completa:** Todos passando

### Validacoes Funcionando

- ✅ Validacao de titulo nao vazio
- ✅ Validacao de limites de caracteres
- ✅ Validacao de enums de status, prioridade e categoria
- ✅ Separacao clara entre schema de request e response
- ✅ Tipos forte com Pydantic

### Decisoes de Design Implementadas

- Enums de dominio reutilizados nos schemas (sem duplicacao)
- TicketCreate com valores padrao sensatos (status=OPEN, priority=MEDIUM)
- TicketResponse com campo de timestamp para rastreabilidade
- Validacoes declarativas via Field constraints do Pydantic

## Riscos

- Categorias definidas nesta etapa precisarem mudar com o refinamento do dominio
- Crescimento do schema sem manter separacao clara entre request e response

## Duvidas em Aberto

- Quais categorias finais o produto ira consolidar depois do refinamento de negocio?

## Referencias

- Issue / Task: #9 - https://github.com/michelgomessilva/helpdesk-hub-api/issues/9
- PR:
- Documentacao: docs/spec-driven-development.md

## Historico de Decisoes

- 2026-04-05 - Spec criada automaticamente a partir da issue #9.
- 2026-04-05 - TicketCreate foi expandido e TicketResponse foi criado com validacao coberta por TDD.
- 2026-04-22 - Implementacao validada: todos os 6 testes de schema passando, validacoes funcionando corretamente, contratos de request/response separados e consistentes. Feature completamente finalizada e integrada ao projeto.

## Conteudo Importado do GitHub

### Titulo Original

Criar schema de Ticket

### Labels

- feature
- tickets
- priority: high
- week-2

### Descricao Original

## Contexto
Criar schemas de entrada e saida para tickets usando Pydantic.

## O que deve ser feito
- [ ] Criar schema de criacao de ticket
- [ ] Criar schema de resposta de ticket
- [ ] Validar titulo, descricao, prioridade e categoria

## Criterios de aceite
- [ ] Schemas criados
- [ ] Validacao funcionando
- [ ] Respostas consistentes

## Observacoes tecnicas
Separar claramente schema de request e schema de response.
