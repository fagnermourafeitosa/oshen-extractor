from fastapi.testclient import TestClient
from src.core.config import settings

def test_protected_endpoint_no_token(client: TestClient):
    # If the x-token header is missing, FastAPI raises 422 Validation Error
    # because the dependency declares it as Header(...) which is required.
    response = client.post(f"{settings.API_V1}/youtube/download", json={})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.json()["detail"][0]["loc"] == ["header", "x-token"]

def test_protected_endpoint_invalid_token(client: TestClient):
    response = client.post(
        f"{settings.API_V1}/youtube/download",
        json={},
        headers={"x-token": "invalid_token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_protected_endpoint_valid_token(client: TestClient):
    # Determine the correct token from settings
    token = settings.OSHEN_EXTRACTOR_TOKEN
    
    # We send an empty body to provoke a 422 Validation Error on the BODY.
    # If the token was rejected, we would get 401.
    # If the token is accepted, we get passed the auth middleware and hit Pydantic validation on the request body.
    response = client.post(
        f"{settings.API_V1}/youtube/download",
        json={},
        headers={"x-token": token}
    )
    
    # We expect 422 because the body is empty, which proves we passed Auth (401)
    assert response.status_code == 422
    # Verify it is indeed body validation error, not header
    assert response.json()["detail"][0]["loc"] == ["body", "url"]
