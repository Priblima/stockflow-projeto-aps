# StockFlow — Sistema de Controle de Estoque

Projeto final da disciplina **Análise e Projeto de Sistemas (APS)**.

O StockFlow é um sistema web completo para controle de estoque, desenvolvido com:

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Banco de dados:** SQLite
- **ORM:** SQLAlchemy
- **Autenticação:** JWT
- **Testes:** Pytest
- **Documentação:** Swagger automático + documentos em Markdown
- **UML:** diagramas em arquivo `.drawio`

---

## 1. Funcionalidades implementadas

### Usuários e segurança

- Cadastro de usuário.
- Login com e-mail e senha.
- Geração de token JWT com expiração.
- Senhas protegidas com hash PBKDF2 + salt.
- Rotas protegidas por token Bearer.
- Endpoint `/auth/me` para validar usuário autenticado.

### Produtos

- Cadastro de produtos.
- Consulta/listagem de produtos.
- Busca por nome, categoria e estoque baixo.
- Atualização de produtos.
- Exclusão de produtos.

### Estoque

- Entrada de estoque.
- Saída de estoque com validação para impedir saldo negativo.
- Histórico de movimentações.

### Relatórios

- Resumo geral do estoque.
- Valor total estimado do estoque.
- Quantidade total de itens.
- Lista de produtos com estoque baixo.

---

## 2. Estrutura do projeto

```text
StockFlow_Projeto_APS/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── scripts/
│   │   └── seed.py
│   └── Dockerfile
├── frontend/
│   ├── app.py
│   └── Dockerfile
├── tests/
├── docs/
│   ├── ARQUITETURA.md
│   ├── INSTALACAO_EXECUCAO.md
│   ├── REQUISITOS_ATUALIZADOS.md
│   ├── TESTES.md
│   ├── DIAGRAMAS_UML.md
│   └── UML/
│       ├── StockFlow_UML.drawio
│       ├── casos_de_uso.drawio
│       ├── diagrama_de_classes.drawio
│       ├── diagrama_de_sequencia_login.drawio
│       ├── diagrama_de_atividades.drawio
│       └── diagrama_de_componentes.drawio
├── .github/workflows/ci.yml
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── run_backend.bat
├── run_frontend.bat
├── run_tests.bat
├── run_backend.sh
├── run_frontend.sh
└── run_tests.sh
```

---

## 3. Instalação rápida

### 3.1 Criar ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux/Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3.2 Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Executar o backend

Abra um terminal na pasta do projeto e execute:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 5. Executar o frontend

Abra outro terminal na pasta do projeto e execute:

```bash
python -m streamlit run frontend/app.py
```

O sistema abrirá no navegador em:

```text
http://localhost:8501
```

---

## 6. Usuário demo opcional

Para criar dados de demonstração, rode:

```bash
cd backend
python -m scripts.seed
```

Credenciais criadas pelo seed:

```text
E-mail: admin@stockflow.com
Senha: admin123
```

---

## 7. Rodar testes automatizados

Na raiz do projeto:

```bash
python -m pytest -q
```

Os testes validam:

- Health check da API.
- Cadastro de usuário.
- Login JWT válido e inválido.
- Bloqueio de rotas sem token.
- CRUD completo de produtos.
- Entrada e saída de estoque.
- Relatórios.

---

## 8. Executar com Docker opcional

```bash
docker compose up --build
```

Serviços:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8501`

---

## 9. Padrões de projeto aplicados

### MVC adaptado

- **Model:** `backend/app/models`
- **View:** `frontend/app.py`
- **Controller/Routes:** `backend/app/routes`
- **Service:** `backend/app/services`

### Repository

A camada `backend/app/repositories` centraliza o acesso ao banco, evitando consultas SQLAlchemy espalhadas pelas rotas.

### Singleton / Factory

O arquivo `config.py` usa `@lru_cache` para entregar uma instância única das configurações do sistema.

---

## 10. Entregáveis para o professor

- Código-fonte completo.
- API REST funcional com Swagger.
- Frontend integrado em Streamlit.
- Banco SQLite com SQLAlchemy.
- JWT e hashing de senha.
- Testes automatizados com Pytest.
- Documentação de requisitos, arquitetura, instalação e testes.
- Diagramas UML em `.drawio`.
- Pipeline simples de CI em GitHub Actions.

