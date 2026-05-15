def test_report_summary(client, auth_headers):
    client.post(
        "/produtos",
        json={"nome": "Cabo HDMI", "categoria": "Acessórios", "quantidade": 5, "peso": 0.2, "preco": 30.0},
        headers=auth_headers,
    )
    client.post(
        "/produtos",
        json={"nome": "Webcam", "categoria": "Acessórios", "quantidade": 2, "peso": 0.3, "preco": 150.0},
        headers=auth_headers,
    )

    response = client.get("/relatorios/resumo", headers=auth_headers)
    assert response.status_code == 200
    resumo = response.json()
    assert resumo["total_produtos"] == 2
    assert resumo["quantidade_total_itens"] == 7
    assert resumo["valor_total_estoque"] == 450.0
    assert resumo["produtos_estoque_baixo"] == 2


def test_low_stock_report(client, auth_headers):
    client.post(
        "/produtos",
        json={"nome": "Produto Baixo", "categoria": "Teste", "quantidade": 1, "peso": 1.0, "preco": 10.0},
        headers=auth_headers,
    )
    client.post(
        "/produtos",
        json={"nome": "Produto Alto", "categoria": "Teste", "quantidade": 20, "peso": 1.0, "preco": 10.0},
        headers=auth_headers,
    )

    response = client.get("/relatorios/baixo-estoque?limite=5", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nome"] == "Produto Baixo"
