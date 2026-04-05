# F007 - Criar enums de status e prioridade

## Metadados

- ID: `F007`
- Status: `Done`
- Owner:
- Criado em: `2026-04-05`
- Atualizado em: `2026-04-05`
- Origem no GitHub: #7 - https://github.com/michelgomessilva/helpdesk-hub-api/issues/7
- Responsaveis tecnicos:

## Resumo

Padronizar os valores possiveis para status e prioridade do ticket por meio de enums reutilizaveis e aplicados nos schemas.

## Problema

Sem enums dedicados, status e prioridade tenderiam a virar strings soltas, aumentando risco de inconsistencias, duplicacao de regras e validacoes fragilizadas.

## Objetivo

Criar enums de status e prioridade e usa-los em um schema inicial de ticket para garantir padronizacao e validacao tipada.

## Escopo

- Criar enum de status
- Criar enum de prioridade
- Usar os enums nos schemas
- Enums criados
- Valores aceitos padronizados
- Schemas usam enums corretamente

## Fora de Escopo

- Persistencia de tickets
- Endpoints de criacao e listagem de tickets
- Regras avancadas de transicao de status

## Personas ou Usuarios Impactados

- Time de desenvolvimento
- Consumidores internos dos futuros schemas de ticket
- Revisores tecnicos

## Contexto de Negocio

- Label importada: feature
- Label importada: tickets
- Label importada: priority: high
- Label importada: week-2
- Status inicial esperado: `open`.
- Prioridades suportadas: `low`, `medium`, `high`, `urgent`.

## Requisitos Funcionais

- RF01: Criar enum de status
- RF02: Criar enum de prioridade
- RF03: Usar os enums nos schemas

## Requisitos Nao Funcionais

- RNF01: Os enums devem ser reutilizaveis em futuros schemas e regras de negocio.
- RNF02: A validacao deve rejeitar valores invalidos de forma automatica.
- RNF03: A modelagem deve respeitar Clean Architecture, mantendo conceitos de ticket fora da camada de API.

## Diretrizes Arquiteturais

- Clean Architecture: Os enums foram posicionados na camada de dominio e reutilizados pelos schemas.
- SOLID: Responsabilidades separadas entre conceitos de dominio e contratos de entrada.
- DRY: Status e prioridade ficam centralizados em um unico ponto de definicao.
- Guard Clauses: A validacao foi delegada ao Pydantic com tipos explicitos, evitando condicionais repetidas.
- Middlewares: Nao aplicavel nesta entrega.
- Design Patterns: Uso simples de enum tipado como base de padronizacao do dominio.

## Criterios de Aceitacao

- [x] Criar enum de status
- [x] Criar enum de prioridade
- [x] Usar os enums nos schemas
- [x] Enums criados
- [x] Valores aceitos padronizados
- [x] Schemas usam enums corretamente

## Fluxo Esperado

1. Um schema de ticket recebe `status` e `priority`.
2. O Pydantic converte e valida os valores contra os enums definidos.
3. Valores invalidos sao rejeitados automaticamente.

## Casos de Erro e Excecoes

- Valores invalidos de status devem falhar na validacao.
- Valores invalidos de prioridade devem falhar na validacao.

## Dependencias

- Pydantic configurado no projeto
- Estrutura de schemas ja existente

## Impacto Tecnico

- Modulos afetados: camada de dominio e schemas
- Entidades envolvidas: conceitos basicos de ticket
- APIs, filas, jobs ou integracoes: nao aplicavel
- Migracoes ou mudancas de infraestrutura: nao aplicavel
- Camadas afetadas na arquitetura: dominio e contratos de entrada
- Necessidade de middlewares: nao aplicavel
- Design patterns adotados ou descartados: enums tipados para padronizacao e validacao

## Estrategia de Implementacao

1. Criar enums dedicados para status e prioridade.
2. Criar schema inicial de ticket usando esses tipos.
3. Validar com testes automatizados para casos validos e invalidos.

## Estrategia de Testes

- Teste de criacao de schema com valores validos
- Teste de rejeicao de status invalido
- Teste de rejeicao de prioridade invalida

## Observabilidade

- Nao aplicavel nesta etapa

## Riscos

- Escolha de valores dos enums divergir das regras futuras de negocio
- Acoplamento indevido se enums fossem criados na camada errada

## Duvidas em Aberto

- Quando as transicoes de status passarao a ter regra formal?
- O conjunto de prioridades sera expandido no futuro?

## Referencias

- Issue / Task: #7 - https://github.com/michelgomessilva/helpdesk-hub-api/issues/7
- PR:
- Documentacao: docs/spec-driven-development.md

## Historico de Decisoes

- 2026-04-05 - Spec criada automaticamente a partir da issue #7.
- 2026-04-05 - Enums movidos para a camada de dominio e integrados a um schema inicial de ticket com validacao automatica via TDD.

## Conteudo Importado do GitHub

### Titulo Original

Criar enums de status e prioridade

### Labels

- feature
- tickets
- priority: high
- week-2

### Descricao Original

## Contexto
Padronizar os valores possiveis para status e prioridade do ticket.

## O que deve ser feito
- [ ] Criar enum de status
- [ ] Criar enum de prioridade
- [ ] Usar os enums nos schemas

## Criterios de aceite
- [ ] Enums criados
- [ ] Valores aceitos padronizados
- [ ] Schemas usam enums corretamente

## Observacoes tecnicas
Status inicial esperado: open. Prioridades: low, medium, high, urgent.
