# Requisitos Atualizados — StockFlow

## 1. Requisitos Funcionais

| Código | Requisito | Descrição | Status |
|---|---|---|---|
| RF01 | Cadastrar usuário | Permitir criação de novos usuários com nome, e-mail e senha. | Implementado |
| RF02 | Autenticar usuário | Permitir login com e-mail e senha, retornando token JWT. | Implementado |
| RF03 | Cadastrar produto | Permitir cadastro de nome, categoria, quantidade, peso e preço. | Implementado |
| RF04 | Consultar produtos | Listar produtos e permitir filtros por nome, categoria e estoque baixo. | Implementado |
| RF05 | Atualizar produto | Editar informações do produto. | Implementado |
| RF06 | Excluir produto | Remover produto do sistema. | Implementado |
| RF07 | Entrada de estoque | Adicionar quantidade ao estoque de um produto. | Implementado |
| RF08 | Saída de estoque | Remover quantidade do estoque, impedindo saldo negativo. | Implementado |
| RF09 | Consultar movimentações | Listar histórico de entradas e saídas. | Implementado |
| RF10 | Emitir relatórios simples | Exibir resumo do estoque e produtos com estoque baixo. | Implementado |

## 2. Requisitos Não Funcionais

| Categoria | Requisito | Como foi atendido |
|---|---|---|
| Segurança | Autenticação JWT | Login retorna token JWT; endpoints principais exigem `Authorization: Bearer <token>`. |
| Segurança | Senhas protegidas | Senhas são armazenadas com hash PBKDF2 + salt, não em texto puro. |
| Segurança | Validação de dados | Schemas Pydantic validam campos, limites e tipos. |
| Segurança | HTTPS em produção | O MVP local roda em HTTP; em deploy, recomenda-se Render/AWS/Azure/Nginx com HTTPS. |
| Performance | Respostas rápidas | FastAPI + SQLite atendem ao MVP com baixa latência em ambiente local. |
| Usabilidade | Interface intuitiva | Streamlit apresenta login, cadastro, produtos, estoque e relatórios em menu lateral. |
| Manutenibilidade | Código modular | Separação em models, schemas, routes, services e repositories. |
| Qualidade | Testes automatizados | Pytest cobre autenticação, CRUD, estoque e relatórios. |
| Documentação | Swagger | FastAPI gera documentação automática em `/docs`. |

## 3. Regras de Negócio

1. O e-mail do usuário deve ser único.
2. A senha deve ter pelo menos 6 caracteres.
3. Apenas usuários autenticados podem acessar produtos, estoque e relatórios.
4. Produto não pode ter quantidade, peso ou preço negativos.
5. Saída de estoque não pode ser maior que a quantidade disponível.
6. Produtos com quantidade menor ou igual a 5 são considerados em estoque baixo.

## 4. Escopo

### Inclui

- Cadastro e login de usuários.
- CRUD completo de produtos.
- Entrada e saída de estoque.
- Relatórios simples.
- Frontend web em Streamlit.
- API REST em FastAPI.
- Banco SQLite via SQLAlchemy.
- Testes automatizados.
- Diagramas UML em draw.io.

### Não inclui

- Integração com ERP ou CRM externo.
- Aplicativo mobile nativo.
- Pagamentos.
- Dashboard avançado de BI.
