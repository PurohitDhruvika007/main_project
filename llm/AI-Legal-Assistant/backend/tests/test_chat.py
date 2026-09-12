from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_empty_question():
    response = client.post(
        "/chat/ask",
        json={
            "question": "",
            "top_k": 3
        }
    )

    assert response.status_code == 400
