def test_create_product_requires_auth(client, produto_payload):
    response = client.post("/produtos", json=produto_payload)
    assert response.status_code == 401


def test_create_and_list_products(client, auth_headers, produto_payload):
    create = client.post("/produtos", json=produto_payload, headers=auth_headers)
    assert create.status_code == 201
    assert create.json()["nome"] == produto_payload["nome"]

    response = client.get("/produtos", headers=auth_headers)
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 1
    assert products[0]["categoria"] == "Informática"


def test_get_update_delete_product(client, auth_headers, produto_payload):
    create = client.post("/produtos", json=produto_payload, headers=auth_headers)
    product_id = create.json()["id"]

    get_response = client.get(f"/produtos/{product_id}", headers=auth_headers)
    assert get_response.status_code == 200

    update_response = client.put(
        f"/produtos/{product_id}",
        json={"preco": 3200.0, "quantidade": 8},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["preco"] == 3200.0
    assert update_response.json()["quantidade"] == 8

    delete_response = client.delete(f"/produtos/{product_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    not_found = client.get(f"/produtos/{product_id}", headers=auth_headers)
    assert not_found.status_code == 404


def test_filter_low_stock(client, auth_headers):
    client.post(
        "/produtos",
        json={"nome": "Mouse", "categoria": "Periféricos", "quantidade": 3, "peso": 0.1, "preco": 80.0},
        headers=auth_headers,
    )
    client.post(
        "/produtos",
        json={"nome": "Monitor", "categoria": "Monitores", "quantidade": 15, "peso": 3.0, "preco": 700.0},
        headers=auth_headers,
    )
    response = client.get("/produtos?estoque_baixo=true", headers=auth_headers)
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 1
    assert products[0]["nome"] == "Mouse"
