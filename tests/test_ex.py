from fastapi.testclient import TestClient

from ..app.main import app


client = TestClient(app)


def test_read_unexistent_user():
    response = client.get('/users/1', headers={"Bearer Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNjQ4MTIwNTI0fQ.rBkeLfxFJ2fo3k8U4-sPLITg0nmfXnF9FvHGOLlsxys"})
    assert response.status_code == 404
    assert response.json() == {"detail": "user with id: 1 was not found"}