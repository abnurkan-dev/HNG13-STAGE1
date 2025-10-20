from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get():
    resp = client.post("/strings", json={"value": "madam"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["properties"]["is_palindrome"] is True

    resp2 = client.get("/strings/madam")
    assert resp2.status_code == 200

def test_list_and_delete():
    client.post("/strings", json={"value": "hello world"})
    resp = client.get("/strings?word_count=2")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] > 0

    del_resp = client.delete("/strings/hello world")
    assert del_resp.status_code == 204

def test_natural_language_filter():
    client.post("/strings", json={"value": "racecar"})
    resp = client.get(
        "/strings/filter-by-natural-language",
        params={"query": "all single word palindromic strings"},
    )
    assert resp.status_code == 200
