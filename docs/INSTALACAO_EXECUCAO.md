# Instalação e Execução

## 1. Pré-requisitos

- Python 3.11 ou superior.
- Pip.
- Navegador web.

## 2. Instalar dependências

Na raiz do projeto:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## 3. Executar backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Acesse:

```text
http://127.0.0.1:8000/docs
```

## 4. Criar usuário demo opcional

Em outro terminal ou com o backend parado:

```bash
cd backend
python -m scripts.seed
```

Login demo:

```text
admin@stockflow.com
admin123
```

## 5. Executar frontend

Na raiz do projeto:

```bash
python -m streamlit run frontend/app.py
```

Acesse:

```text
http://localhost:8501
```

## 6. Rodar testes

Na raiz do projeto:

```bash
python -m pytest -q
```

## 7. Execução com scripts

Windows:

```bash
run_backend.bat
run_frontend.bat
run_tests.bat
```

Linux/Mac:

```bash
chmod +x run_backend.sh run_frontend.sh run_tests.sh
./run_backend.sh
./run_frontend.sh
./run_tests.sh
```
