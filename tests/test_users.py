from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users/", json= {"email": "example_email@gmail.com", "password": "password123"})
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "example_email@gmail.com"