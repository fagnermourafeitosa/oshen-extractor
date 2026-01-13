👉 Troca só a URL pelo endpoint do seu FastAPI.
curl -X POST "http://192.168.0.23:8080/webhook/set/<evolution-instance-name>" \
  -H "Content-Type: application/json" \
  -H "apikey: <evolution_aikey>" \
  -d '{
    "webhook": {
      "enabled": true,
      "url": "http://192.168.0.23:9009/evolution/webhook",
      "webhook_by_events": false,
      "events": [
        "MESSAGES_UPSERT"
      ]
    }
  }'

📌 Evento importante pra você

MESSAGES_UPSERT → mensagem nova (é o principal)

3️⃣ O que a Evolution vai te enviar

Exemplo simplificado:

{
  "event": "MESSAGES_UPSERT",
  "instance": "bot-01",
  "data": {
    "key": {
      "remoteJid": "1203630xxxx@g.us"
    },
    "message": {
      "conversation": "Ricca Escova Raquete Flex Red..."
    },
    "pushName": "Grupo de Achadinhos ADM 2",
    "messageTimestamp": 1736671743
  }
}


👉 Isso já vem automaticamente, você não precisa buscar depois.