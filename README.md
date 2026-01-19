# Oshen Extractor API

API responsável por extrair mídias de redes sociais (TikTok, Instagram, YouTube) e processar webhooks do WhatsApp (via Evolution API), encaminhando as mensagens para uma fila Redis.

## Funcionalidades Prncipais

1.  **Extratores de Mídia**: Endpoints para baixar vídeos e áudios de redes sociais via `yt-dlp`.
2.  **Webhook WhatsApp**: Recebe eventos da Evolution API e os publica em um Redis Stream para consumo assíncrono (por workers).
3.  **Auto Configuração**: Ao iniciar via Docker, tenta configurar automaticamente o webhook na instância da Evolution API configurada.

## Tecnologias

*   Python 3.11
*   FastAPI
*   Redis
*   Docker & Docker Compose

## Configuração

1.  Copie o arquivo de exemplo de ambiente:
    ```bash
    cp .env.example .env
    ```

2.  Edite o arquivo `.env` com suas configurações:
    *   `OSHEN_EXTRACTOR_TOKEN`: Token para autenticação nas rotas da API.
    *   `REDIS_HOST`, `REDIS_PORT`: Conexão com o Redis.
    *   `EVOLUTION_API_URL`: URL base da sua Evolution API (ex: `http://host.docker.internal:8080`).
    *   `EVOLUTION_API_KEY`: API Key global da Evolution.
    *   `EVOLUTION_INSTANCE_NAME`: Nome da instância que receberá o webhook.
    *   `WEBHOOK_PUBLIC_URL`: URL onde *esta* API está acessível para a Evolution (ex: `http://host.docker.internal:9009`).

## Como Rodar

### Via Docker Compose (Recomendado)

```bash
docker-compose up --build
```
Isso irá construir a imagem, iniciar o serviço e executar o script de configuração do webhook automaticamente.

### Localmente

```bash
# Instalar dependências
pipenv install --dev

# Ativar virtualenv
pipenv shell

# Rodar API
uvicorn src.main:app --host 0.0.0.0 --port 9009 --reload
```
*Nota: Para rodar a configuração automática do webhook localmente, execute: `python -m src.scripts.configure_webhook`*

## Endpoints

### Mídia (Requer Header `x-token`)

*   `POST /api/v1/instagram/download`: Baixa mídia do Instagram.
*   `POST /api/v1/tiktok/download`: Baixa mídia do TikTok.
*   `POST /api/v1/youtube/download`: Baixa mídia do YouTube.

### Webhook (Requer Header `x-token` se configurado)

*   `POST /evolution`: Recebe eventos da Evolution API (focado em `MESSAGES_UPSERT`).
    *   Filtra mensagens de texto e mídia.
    *   Publica no Redis Stream definido em `WHATSAPP_REDIS_STREAM`.

## Fluxo de Dados (WhatsApp)

1.  Usuário envia mensagem no WhatsApp.
2.  Evolution API detecta e envia POST para `/evolution`.
3.  OShen Extractor valida o token, processa o JSON e extrai metadados relevantes.
4.  Dados são empurrados para o stream no Redis (`xadd`).
5.  Worker externo (outro serviço) consome este stream.
