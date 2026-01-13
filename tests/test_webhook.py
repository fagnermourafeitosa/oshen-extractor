from src.core.config import settings

def test_webhook_evolution_success(client, mocker):
    # Mock the push method of the stream_service instance imported in webhook module
    mock_push = mocker.patch("src.api.v1.endpoints.webhook.stream_service.push")
    
    payload = {
        "event": "MESSAGES_UPSERT", 
        "data": {
            "key": {"remoteJid": "123@g.us"},
            "pushName": "Teste",
            "messageTimestamp": 1736671743,
            "message": {"conversation": "teste"}
        }
    }
    headers = {"x-token": settings.OSHEN_EXTRACTOR_TOKEN}
    
    # Endpoint mudou para /evolution (conforme registro global no main.py)
    response = client.post("/evolution", json=payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    
    # Verifica se o push foi chamado com os dados extraídos + o raw payload
    args, _ = mock_push.call_args
    pushed_data = args[0]
    assert pushed_data["message"] == "teste"
    assert pushed_data["raw"] == payload

def test_webhook_evolution_lowercase_dot_event(client, mocker):
    mock_push = mocker.patch("src.api.v1.endpoints.webhook.stream_service.push")
    
    payload = {
        "event": "messages.upsert", 
        "data": {
            "key": {"remoteJid": "123@g.us"},
            "message": {"conversation": "teste lowercase"}
        }
    }
    headers = {"x-token": settings.OSHEN_EXTRACTOR_TOKEN}
    
    response = client.post("/evolution", json=payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    
    args, _ = mock_push.call_args
    assert args[0]["message"] == "teste lowercase"

def test_webhook_evolution_extended_text(client, mocker):
    mock_push = mocker.patch("src.api.v1.endpoints.webhook.stream_service.push")
    
    payload = {
        "event": "MESSAGES_UPSERT", 
        "data": {
            "key": {"remoteJid": "123@g.us"},
            "message": {
                "extendedTextMessage": {"text": "link https://google.com"}
            }
        }
    }
    headers = {"x-token": settings.OSHEN_EXTRACTOR_TOKEN}
    
    response = client.post("/evolution", json=payload, headers=headers)
    
    assert response.status_code == 200
    args, _ = mock_push.call_args
    assert args[0]["message"] == "link https://google.com"

def test_webhook_evolution_ignored(client, mocker):
    mock_push = mocker.patch("src.api.v1.endpoints.webhook.stream_service.push")
    headers = {"x-token": settings.OSHEN_EXTRACTOR_TOKEN}
    
    # Evento errado
    response = client.post("/evolution", json={"event": "OTHER"}, headers=headers)
    assert response.json() == {"ignored": True}
    
    # Sem mensagem
    payload = {"event": "MESSAGES_UPSERT", "data": {"message": {}}}
    response = client.post("/evolution", json=payload, headers=headers)
    assert response.json() == {"ignored": True}
    
    mock_push.assert_not_called()

def test_webhook_evolution_unauthorized(client, mocker):
    mock_push = mocker.patch("src.api.v1.endpoints.webhook.stream_service.push")
    payload = {"event": "MESSAGES_UPSERT"}
    
    # Missing header
    response = client.post("/evolution", json=payload)
    assert response.status_code == 422
    
    # Invalid header
    response = client.post("/evolution", json=payload, headers={"x-token": "wrong-token"})
    assert response.status_code == 401
    mock_push.assert_not_called()
