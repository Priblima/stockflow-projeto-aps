# Arquitetura — StockFlow

## Visão Geral

```text
Usuário
  ↓ navegador
Frontend Streamlit
  ↓ HTTP/JSON
Backend FastAPI
  ↓ SQLAlchemy ORM
Banco SQLite
```

## Componentes

### Frontend — Streamlit

Responsável por:

- Tela de login.
- Cadastro de usuário.
- Formulários de produtos.
- Entrada e saída de estoque.
- Visualização de relatórios.

### Backend — FastAPI

Responsável por:

- Expor endpoints REST.
- Validar dados recebidos.
- Aplicar regras de negócio.
- Gerar e validar token JWT.
- Integrar com o banco via services/repositories.

### Banco de Dados — SQLite

Tabelas principais:

- `usuarios`
- `produtos`
- `movimentacoes_estoque`

## Padrões Aplicados

### MVC Adaptado

- Model: SQLAlchemy models.
- View: Streamlit.
- Controller: FastAPI routes.
- Service: regras de negócio.

### Repository

Acesso ao banco centralizado nos repositories:

- `UserRepository`
- `ProductRepository`
- `StockRepository`

### Singleton / Factory

`get_settings()` usa `@lru_cache`, funcionando como Singleton para configurações.

## Segurança

1. Usuário cadastra senha.
2. Backend salva apenas hash da senha.
3. No login, backend valida senha e gera JWT.
4. Frontend guarda o token na sessão do Streamlit.
5. Endpoints protegidos exigem token Bearer.

## Endpoints principais

| Método | Rota | Função | Protegida |
|---|---|---|---|
| GET | `/` | Health check | Não |
| POST | `/auth/register` | Cadastrar usuário | Não |
| POST | `/auth/login` | Login JWT | Não |
| GET | `/auth/me` | Dados do usuário logado | Sim |
| POST | `/produtos` | Criar produto | Sim |
| GET | `/produtos` | Listar produtos | Sim |
| GET | `/produtos/{id}` | Obter produto | Sim |
| PUT | `/produtos/{id}` | Atualizar produto | Sim |
| DELETE | `/produtos/{id}` | Excluir produto | Sim |
| POST | `/estoque/entrada` | Entrada de estoque | Sim |
| POST | `/estoque/saida` | Saída de estoque | Sim |
| GET | `/estoque/movimentacoes` | Histórico | Sim |
| GET | `/relatorios/resumo` | Resumo do estoque | Sim |
| GET | `/relatorios/baixo-estoque` | Estoque baixo | Sim |
