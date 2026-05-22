def test_proxy_forwards_and_persists_request(client, fake_http_client):
    response = client.post("/proxy/orders?source=test", json={"sku": "latte"})

    assert response.status_code == 201
    assert response.json()["received"] == {"sku": "latte"}
    assert fake_http_client.calls[0]["url"] == "http://target.local/orders?source=test"

    history = client.get("/requests").json()
    assert len(history) == 1
    assert history[0]["method"] == "POST"
    assert history[0]["path"] == "/orders"
    assert history[0]["requestBody"] == {"sku": "latte"}
    assert history[0]["responseStatus"] == 201


def test_clear_requests(client, fake_http_client):
    client.post("/proxy/orders", json={"sku": "latte"})

    assert len(client.get("/requests").json()) == 1
    assert client.delete("/requests").status_code == 204
    assert client.get("/requests").json() == []
