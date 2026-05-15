def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "StockFlow API funcionando"}


def test_register_user(client, user_payload):
    response = client.post("/auth/register", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_payload["email"]
    assert "senha" not in data
    assert "senha_hash" not in data


def test_register_duplicate_email(client, user_payload):
    client.post("/auth/register", json=user_payload)
    response = client.post("/auth/register", json=user_payload)
    assert response.status_code == 400


def test_login_success(client, user_payload):
    client.post("/auth/register", json=user_payload)
    response = client.post("/auth/login", json={"email": user_payload["email"], "senha": user_payload["senha"]})
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_invalid_password(client, user_payload):
    client.post("/auth/register", json=user_payload)
    response = client.post("/auth/login", json={"email": user_payload["email"], "senha": "errada"})
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_token(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "usuario@teste.com"
