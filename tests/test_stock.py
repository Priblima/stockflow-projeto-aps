def test_stock_entry_and_exit(client, auth_headers, produto_payload):
    create = client.post("/produtos", json=produto_payload, headers=auth_headers)
    product_id = create.json()["id"]

    entrada = client.post(
        "/estoque/entrada",
        json={"produto_id": product_id, "quantidade": 5, "observacao": "Compra de fornecedor"},
        headers=auth_headers,
    )
    assert entrada.status_code == 201
    assert entrada.json()["tipo"] == "entrada"

    produto = client.get(f"/produtos/{product_id}", headers=auth_headers)
    assert produto.json()["quantidade"] == 15

    saida = client.post(
        "/estoque/saida",
        json={"produto_id": product_id, "quantidade": 4, "observacao": "Venda"},
        headers=auth_headers,
    )
    assert saida.status_code == 201
    assert saida.json()["tipo"] == "saida"

    produto = client.get(f"/produtos/{product_id}", headers=auth_headers)
    assert produto.json()["quantidade"] == 11


def test_stock_exit_cannot_be_negative(client, auth_headers, produto_payload):
    create = client.post("/produtos", json=produto_payload, headers=auth_headers)
    product_id = create.json()["id"]

    response = client.post(
        "/estoque/saida",
        json={"produto_id": product_id, "quantidade": 999, "observacao": "Saída inválida"},
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_list_stock_movements(client, auth_headers, produto_payload):
    create = client.post("/produtos", json=produto_payload, headers=auth_headers)
    product_id = create.json()["id"]

    client.post(
        "/estoque/entrada",
        json={"produto_id": product_id, "quantidade": 2, "observacao": "Reposição"},
        headers=auth_headers,
    )

    response = client.get("/estoque/movimentacoes", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
