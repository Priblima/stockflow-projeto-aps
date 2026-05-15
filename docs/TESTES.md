# Testes — StockFlow

## Testes automatizados

Os testes automatizados usam Pytest e FastAPI TestClient.

Execute na raiz do projeto:

```bash
python -m pytest -q
```

## Cenários cobertos

| ID | Cenário | Resultado esperado |
|---|---|---|
| CT01 | Health check da API | Status 200 |
| CT02 | Cadastro de usuário válido | Status 201 |
| CT03 | Cadastro com e-mail duplicado | Status 400 |
| CT04 | Login com credenciais válidas | Status 200 e token JWT |
| CT05 | Login com senha inválida | Status 401 |
| CT06 | Acessar rota protegida sem token | Status 401 |
| CT07 | Criar produto autenticado | Status 201 |
| CT08 | Listar produtos autenticado | Status 200 |
| CT09 | Atualizar produto | Status 200 |
| CT10 | Excluir produto | Status 204 |
| CT11 | Entrada de estoque | Quantidade aumenta |
| CT12 | Saída de estoque | Quantidade diminui |
| CT13 | Saída maior que estoque | Status 400 |
| CT14 | Relatório de resumo | Totais corretos |
| CT15 | Relatório de estoque baixo | Retorna produtos abaixo do limite |

## Testes manuais recomendados

Também é possível testar pelo Swagger:

```text
http://127.0.0.1:8000/docs
```

Fluxo manual:

1. Criar usuário em `/auth/register`.
2. Fazer login em `/auth/login`.
3. Copiar o token retornado.
4. Usar o token como `Bearer <token>` nas rotas protegidas.
5. Testar CRUD de produtos.
6. Testar entrada e saída de estoque.
7. Testar relatórios.
