# Spec-Driven Development

Este documento e o guia central para planejar, documentar e implementar features do projeto de ponta a ponta usando Spec-Driven Development (SDD).

## Contexto do Projeto

O projeto a ser implementado e o `HelpDesk Hub API`, uma API backend para abertura e gestao de chamados internos de suporte.

O dominio principal do sistema envolve:

- cadastro de utilizadores
- autenticacao e autorizacao com roles
- abertura e consulta de tickets
- atribuicao de responsaveis
- comentarios em tickets
- mudanca de status com regras de negocio
- historico de alteracoes
- metricas operacionais
- automacoes e tarefas em background
- integracao com API externa
- endpoint de IA simulada para sugestoes

O objetivo nao e construir apenas um CRUD simples. A proposta do projeto e evoluir gradualmente ate uma API com caracteristicas profissionais, incluindo persistencia, seguranca, testes, observabilidade, conteinerizacao e pipeline de CI.

## Objetivo

Antes de implementar qualquer feature, registramos:

- o problema a resolver
- o contexto de negocio
- o comportamento esperado
- os criterios de aceitacao
- os impactos tecnicos
- o plano de entrega

Isso ajuda a reduzir retrabalho, alinhar expectativas e manter historico claro das decisoes.

## Visao de Produto

O `HelpDesk Hub API` deve representar um sistema interno realista de suporte, usado para controlar solicitacoes de TI, acessos a sistemas, problemas operacionais e atendimento interno.

Ao escrever specs para este projeto, prefira sempre conectar cada feature a pelo menos um destes objetivos:

- melhorar o fluxo de abertura e tratamento de chamados
- garantir rastreabilidade e controle operacional
- aumentar a confiabilidade tecnica da aplicacao
- profissionalizar a entrega para nivel de portfolio

## Diretrizes de Engenharia

Estas diretrizes valem para todo o projeto, nao apenas para features isoladas.

- A arquitetura do projeto deve seguir `Clean Architecture`.
- As implementacoes devem respeitar os principios `SOLID`.
- O codigo deve buscar `DRY`, evitando duplicacao desnecessaria.
- Prefira `guard clauses` para deixar fluxos mais claros e reduzir aninhamentos.
- Utilize `middlewares` quando a responsabilidade for transversal, como logging, autenticacao, correlacao de requests e tratamento global de comportamento HTTP.
- Aplique `design patterns` quando eles simplificarem a manutencao, a extensibilidade e a clareza do dominio.
- Priorize separacao de responsabilidades, baixo acoplamento e alta coesao.
- Toda decisao tecnica deve favorecer legibilidade, testabilidade, manutenibilidade e evolucao segura.
- Evite complexidade acidental: padroes e abstractions devem existir para resolver problemas reais, nao por excesso de arquitetura.

## Como Aplicar essas Diretrizes nas Specs

O documento central define a regra geral, mas cada feature deve refletir isso quando for relevante.

Ao escrever ou revisar uma feature, registre explicitamente:

- como ela respeita a `Clean Architecture`
- quais responsabilidades ficam em cada camada
- onde `SOLID` influencia a modelagem da solucao
- se existe risco de violar `DRY`
- onde `guard clauses` ajudam a clareza do fluxo
- se ha necessidade de `middlewares`
- quais `design patterns` fazem sentido e por que

Se uma feature nao exigir um item especifico, nao e necessario forcá-lo. O importante e que a decisao esteja consciente, nao implicita.

## Principios de Evolucao do Projeto

De acordo com o material base do projeto, a evolucao esperada segue esta ordem:

1. Entender o problema e o dominio.
2. Implementar uma versao funcional simples.
3. Organizar melhor a arquitetura.
4. Refatorar com seguranca.
5. Profissionalizar a execucao e a operacao.

No contexto de SDD, isso significa que as specs devem refletir maturidade incremental. Nem toda feature precisa nascer completa. Muitas comecam simples em memoria e depois evoluem para uma versao persistida, autenticada, observavel e testada.

## Fluxo Recomendado

1. Criar ou identificar a task no GitHub.
2. Criar a spec da feature em `docs/features/`.
3. Refinar escopo, regras de negocio, dependencias e criterios de aceitacao.
4. Validar a spec antes de iniciar implementacao.
5. Implementar seguindo a spec aprovada.
6. Atualizar a spec com decisoes, ajustes e status final.

## Estrutura de Documentacao

- Guia central: `docs/spec-driven-development.md`
- Template padrao: `docs/features/_template.md`
- Features: `docs/features/f001-<nome-da-feature>.md`

## Macro Roadmap do Projeto

Com base no PDF da mentoria, o projeto evolui em 11 etapas:

| Etapa | Tema principal | Resultado esperado |
| --- | --- | --- |
| Semana 1 | Setup inicial com FastAPI | app rodando, `/` e `/health` funcionando |
| Semana 2 | CRUD em memoria | tickets e categorias com validacao |
| Semana 3 | Organizacao e filtros | comentarios, filtros, paginacao e camadas |
| Semana 4 | Persistencia | PostgreSQL e SQLAlchemy em uso |
| Semana 5 | Migrations e base de usuarios | Alembic, seed e model de utilizador |
| Semana 6 | Autenticacao e autorizacao | cadastro, login, JWT, roles, `/users/me` |
| Semana 7 | Regras de negocio reais | atribuicao, transicoes de status, historico |
| Semana 8 | Testes | testes unitarios e de integracao |
| Semana 9 | Operacao profissional | logs, exceptions, Docker e CI |
| Semana 10 | Recursos avancados | metricas, cache, background task, integracao externa |
| Semana 11 | Fechamento de portfolio | IA simulada, revisao de arquitetura e README |

Esse roadmap nao obriga que as features sigam exatamente a divisao por semana, mas ele deve orientar a ordem natural de implementacao e refinamento.

## Como Traduzir o Projeto em Features

Uma boa estrategia para este repositorio e dividir o trabalho em features pequenas e cumulativas, por exemplo:

- `F001` Setup inicial da API
- `F002` Health check e rota raiz
- `F003` Cadastro e listagem de categorias
- `F004` Criacao e consulta de tickets
- `F005` Comentarios em tickets
- `F006` Filtros e paginacao
- `F007` Persistencia com PostgreSQL
- `F008` Migrations com Alembic
- `F009` Cadastro de utilizadores
- `F010` Login com JWT
- `F011` Roles e autorizacao
- `F012` Atribuicao e mudanca de status
- `F013` Historico de alteracoes
- `F014` Suite de testes
- `F015` Logs, Docker e CI
- `F016` Metricas e observabilidade
- `F017` Cache e background tasks
- `F018` Integracao com API externa
- `F019` IA simulada para sugestao de classificacao

Se uma feature estiver muito grande, quebre por fluxo, por agregado de dominio ou por etapa tecnica.

## Indice de Features

Atualize esta lista sempre que uma nova feature for iniciada.

| ID | Feature | Status | Origem | Documento |
| --- | --- | --- | --- | --- |
<!-- FEATURES_INDEX_START -->
| F000 | Exemplo inicial | Draft | Manual | `docs/features/f000-exemplo-inicial.md` |
| F001 | Configurar estrutura inicial do projeto com uv | Done | GitHub #1 | `docs/features/f001-setup-initial-api.md` |
| F002 | Instalar FastAPI, Uvicorn e Pydantic | Done | GitHub #2 | `docs/features/f002-instalar-fastapi-uvicorn-pydantic.md` |
<!-- FEATURES_INDEX_END -->

## Contexto das Features

Resumo curto das features registradas para facilitar navegacao, rastreabilidade e onboarding.

<!-- FEATURES_CONTEXT_START -->
### F000 - Exemplo inicial

- Status: `Draft`
- Origem: `Manual`
- Documento: `docs/features/f000-exemplo-inicial.md`
- Labels: nenhuma
- Resumo: Documento de exemplo para demonstrar a estrutura inicial de Spec-Driven Development neste repositorio.

### F001 - Configurar estrutura inicial do projeto com uv

- Status: `Done`
- Origem: `GitHub #1`
- Documento: `docs/features/f001-setup-initial-api.md`
- Labels: `feature`, `setup`, `priority: high`, `week-1`
- Resumo: Base inicial do projeto implementada com uv, pyproject.toml, estrutura src/, API FastAPI minima e testes iniciais passando.

### F002 - Instalar FastAPI, Uvicorn e Pydantic

- Status: `Done`
- Origem: `GitHub #2`
- Documento: `docs/features/f002-instalar-fastapi-uvicorn-pydantic.md`
- Labels: `feature`, `setup`, `api`, `priority: high`, `week-1`
- Resumo: Dependencias FastAPI, Uvicorn e Pydantic registradas no projeto, com schemas Pydantic aplicados nos contratos iniciais da API e testes passando.
<!-- FEATURES_CONTEXT_END -->

## Convencoes de Nomenclatura

### IDs

- Use `F001`, `F002`, `F003`... dentro da documentacao.
- Use o mesmo ID em referencias cruzadas, branches, PRs e commits quando fizer sentido.

### Arquivos

- Padrao: `f001-<nome-da-feature>.md`
- Use letras minusculas.
- Separe palavras com hifen.
- Use nomes curtos e descritivos.

Exemplos:

- `f001-autenticacao-de-usuarios.md`
- `f002-abertura-de-chamados.md`
- `f003-painel-de-agentes.md`

### Titulos

- Comece com o ID da feature.
- Inclua um nome objetivo.

Exemplo:

- `# F002 - Abertura de chamados`

## Como Criar uma Nova Feature

1. Copiar a estrutura de `docs/features/_template.md`.
2. Criar um novo arquivo seguindo o padrao `f001-<nome-da-feature>.md`.
3. Preencher todas as secoes relevantes.
4. Adicionar a feature no indice deste documento.
5. Vincular a spec ao item correspondente no GitHub.

Quando a feature for criada pelos scripts em `scripts/specs/`, o indice e o bloco `Contexto das Features` sao atualizados automaticamente no documento central.

## Como Usar o Template

O template padrao foi criado para manter consistencia entre specs.

Use `docs/features/_template.md` como base para:

- novas features
- refinamentos tecnicos
- descoberta de requisitos
- handoff entre produto, design e engenharia

Nem toda secao precisa ter profundidade maxima no primeiro rascunho, mas toda spec deve deixar claro:

- o que sera entregue
- o que nao faz parte do escopo
- como validar se a entrega esta correta

Ao preencher specs deste projeto, vale dar atencao especial a estes pontos:

- impacto no dominio de tickets, categorias, comentarios e utilizadores
- regras de autorizacao por role
- evolucao da feature entre memoria, banco e operacao real
- observabilidade minima esperada
- compatibilidade com a fase atual do roadmap

## Boas Praticas

- Comece pequeno: prefira uma spec por feature ou incremento real.
- Separe problema de solucao: descreva primeiro a necessidade, depois a implementacao.
- Registre decisoes: quando mudar de direcao, atualize a spec.
- Declare nao-escopo: isso evita expectativa errada.
- Defina criterios de aceitacao testaveis.
- Liste dependencias e riscos cedo.
- Mantenha rastreabilidade entre spec, issue, branch, PR e deploy.
- Evite specs gigantes: se uma feature estiver grande demais, quebre em multiplas features.
- Atualize o status da feature ao longo do ciclo.
- Diferencie claramente evolucao funcional de evolucao tecnica.
- Quando houver regra de negocio, documente transicoes validas, permissoes e restricoes.
- Em features de infraestrutura, deixe explicito o impacto para o fluxo de negocio.
- Reflita no documento se a feature esta criando fundacao ou comportamento final.
- Verifique se a implementacao proposta preserva Clean Architecture, SOLID, DRY e baixo acoplamento.
- Registre middlewares e patterns apenas quando houver ganho real de clareza, reaproveitamento ou controle transversal.

## Eixos de Especificacao para o HelpDesk Hub API

Ao longo do projeto, as features tendem a cair em alguns grupos principais:

### Dominio

- tickets
- categorias
- comentarios
- historico

### Acesso e seguranca

- utilizadores
- login
- JWT
- roles e autorizacao

### Plataforma

- banco de dados
- migrations
- configuracao por ambiente
- Docker
- CI

### Qualidade e operacao

- testes
- logs
- tratamento de erros
- health checks
- metricas

### Recursos avancados

- cache
- tarefas em background
- integracao externa
- IA simulada

Esses eixos ajudam a equilibrar o backlog entre entrega funcional e maturidade tecnica.

## Status Sugeridos

Use um conjunto simples e consistente:

- `Draft`
- `Refining`
- `Ready`
- `In Progress`
- `Blocked`
- `Done`

## Relacao com GitHub

Cada feature pode ser vinculada a um item do GitHub, como:

- Issue
- Task
- Epic
- Pull Request
- Discussion

Recomendacao minima por feature:

- link da issue/task original
- numero da issue
- checklist de criterios de aceitacao
- referencias para PRs relacionados

Para este projeto em particular, uma boa pratica e usar labels no GitHub para espelhar a natureza da spec, por exemplo:

- `domain`
- `auth`
- `database`
- `testing`
- `ops`
- `integration`
- `ai`
- `week-01` ate `week-11`

## Integracao com GitHub sem Copiar e Colar

Sim, e possivel integrar direto.

As abordagens mais praticas sao:

### Opcao 1: GitHub Issue como fonte de verdade inicial

- Criar a task/spec no GitHub.
- Buscar o conteudo da issue via API ou `gh`.
- Gerar automaticamente o arquivo `docs/features/fxxx-...md` com base no template.

Vantagens:

- evita copiar e colar manual
- reaproveita a especificacao ja escrita
- padroniza a criacao das specs locais

### Opcao 2: Sincronizacao semi-automatica

- A issue continua sendo a origem.
- Um script importa titulo, descricao, labels, checklist e links.
- O time complementa apenas os campos tecnicos no arquivo local.

Vantagens:

- rapido para adotar
- menor risco de sobrescrever refinamentos tecnicos

### Opcao 3: Automacao bidirecional controlada

- O GitHub fornece o contexto inicial.
- A spec local vira o documento mais completo.
- Um script ou workflow atualiza comentarios, checklist ou status na issue/PR.

Vantagens:

- boa rastreabilidade
- integra planejamento e execucao

## Sugestao de Proximo Passo para Integracao

Se quiser automatizar isso neste projeto, a estrutura recomendada e:

- `docs/features/` para specs versionadas
- `scripts/specs/import-from-github.ps1` para importar issue/task
- `scripts/specs/new-feature.ps1` para criar arquivo a partir do template
- `scripts/specs/_shared.ps1` para manter sincronizado o documento central
- convencao para mapear `Issue #123` -> `F00X`

No fluxo de importacao, o script tenta preencher automaticamente a spec com base em:

- headings da issue como `Resumo`, `Problema`, `Objetivo`, `Escopo` e `Criterios de Aceitacao`
- checklists da issue para gerar criterios de aceitacao
- bullets da issue para gerar escopo e requisitos funcionais iniciais
- labels da issue para enriquecer o contexto da feature

Fluxo sugerido:

1. Criar ou escolher uma issue no GitHub.
2. Rodar um comando local para gerar a spec.
3. Revisar o arquivo gerado.
4. Refinar secoes tecnicas.
5. Implementar.

Exemplo de comando futuro:

```powershell
./scripts/specs/import-from-github.ps1 -Repository owner/repositorio -IssueNumber 123 -FeatureId F004 -Slug abertura-de-chamados
```

## Checklist Minimo Antes de Implementar

- problema claramente definido
- objetivo da feature registrado
- criterios de aceitacao claros
- escopo e nao-escopo descritos
- dependencias conhecidas mapeadas
- estrategia de validacao descrita
- vinculo com GitHub registrado
- impacto arquitetural avaliado
- aderencia a Clean Architecture, SOLID, DRY e responsabilidades transversais revisada

Para o `HelpDesk Hub API`, acrescente tambem esta validacao mental:

- a feature respeita a fase atual de maturidade do projeto
- as regras de negocio do helpdesk ficaram explicitas
- a seguranca exigida para o endpoint foi definida
- o impacto em testes, logs e monitoracao foi considerado quando relevante
- a distribuicao entre camadas, services, repositories, middlewares e patterns foi pensada de forma intencional

## Fonte de Contexto do Projeto

O contexto acima foi consolidado a partir do arquivo `Projeto HelpDesk Hub API - Mentorados.pdf`, usado como documento base para escopo, roadmap e expectativas de evolucao do sistema.

## Observacoes Finais

O objetivo desta estrutura nao e burocracia. A ideia e criar um sistema leve, repetivel e rastreavel para construir o projeto do inicio ao fim com mais clareza.







