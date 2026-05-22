def test_replay_original_request(client, fake_http_client):
    client.post("/proxy/orders", json={"sku": "latte"})
    original = client.get("/requests").json()[0]

    replay_response = client.post(f"/requests/{original['id']}/replay")

    assert replay_response.status_code == 200
    replayed = replay_response.json()
    assert replayed["requestBody"] == {"sku": "latte"}
    assert len(client.get("/requests").json()) == 2


def test_replay_with_edited_body(client, fake_http_client):
    client.post("/proxy/orders", json={"sku": "latte"})
    original = client.get("/requests").json()[0]

    replay_response = client.post(
        f"/requests/{original['id']}/replay-with-edits",
        json={"requestBody": {"sku": "tea"}},
    )

    assert replay_response.status_code == 200
    replayed = replay_response.json()
    assert replayed["requestBody"] == {"sku": "tea"}
    assert replayed["responseBody"]["received"] == {"sku": "tea"}
    assert "content-length" not in fake_http_client.calls[-1]["headers"]
