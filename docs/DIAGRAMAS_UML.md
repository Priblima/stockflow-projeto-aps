# Diagramas UML — StockFlow

Os diagramas foram criados em formato `.drawio`, compatível com o site/app diagrams.net.

Arquivos disponíveis:

```text
docs/UML/StockFlow_UML.drawio
docs/UML/casos_de_uso.drawio
docs/UML/diagrama_de_classes.drawio
docs/UML/diagrama_de_sequencia_login.drawio
docs/UML/diagrama_de_atividades.drawio
docs/UML/diagrama_de_componentes.drawio
```

## Como abrir

1. Acesse https://app.diagrams.net/ ou abra o Draw.io Desktop.
2. Clique em **File > Open From > Device**.
3. Selecione o arquivo `.drawio`.

## Diagramas incluídos

### 1. Diagrama de Casos de Uso

Atores:

- Usuário
- Administrador

Casos:

- Cadastrar usuário
- Login
- Consultar produtos
- Cadastrar produto
- Editar produto
- Excluir produto
- Entrada de estoque
- Saída de estoque
- Gerar relatórios

### 2. Diagrama de Classes

Classes principais:

- `User`
- `Produto`
- `MovimentoEstoque`
- `AuthService`
- `ProductService`
- `StockService`
- Repositories

### 3. Diagrama de Sequência — Login

Fluxo:

```text
Usuário → Streamlit → FastAPI/AuthService → UserRepository → SQLite → JWT → Usuário
```

### 4. Diagrama de Atividades

Fluxo:

```text
Início → Login → Validação → Menu → CRUD/Estoque/Relatórios → Logout/Fim
```

### 5. Diagrama de Componentes

Componentes:

- Frontend Streamlit
- Backend FastAPI
- Services
- Repositories
- SQLAlchemy
- SQLite
