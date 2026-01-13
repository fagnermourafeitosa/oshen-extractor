# Formato de Postagem de Grupo WhatsApp (Evolution API)

Este documento descreve a estrutura dos dados recebidos via webhook para mensagens de grupos, especificamente focando nos campos de mídia e metadados técnicos.

## Estrutura do Payload (Exemplo Simplificado)

```json
{
  "event": "messages.upsert",
  "data": {
    "key": {
      "remoteJid": "1203630...@g.us",  // ID do Grupo
      "fromMe": false,
      "participant": "5511999999999@s.whatsapp.net" // Remetente
    },
    "pushName": "Nome do Remetente",
    "message": {
      "ephemeralMessage": { // Mensagens em grupos geralmente vêm envelopadas aqui
        "message": {
          "imageMessage": { // Ou videoMessage
            "url": "https://mmg.whatsapp.net/...", // URL para download da mídia (criptografada)
            "caption": "Legenda da mensagem...",
            "mimetype": "image/jpeg",
            
            // Metadados Técnicos
            "fileSha256": { ... },    // Hash para verificação de integridade
            "mediaKey": { ... },      // Chave para descriptografia
            "jpegThumbnail": { ... }  // Miniatura em bytes brutos
          }
        }
      }
    }
  }
}
```

## Dicionário de Campos Técnicos

### `jpegThumbnail`
*   **Nome no Redis:** `thumbnail_raw`
*   **Descrição:** Uma miniatura (preview) de baixíssima resolução da imagem ou vídeo.
*   **Formato:** Objeto JSON representando um *Buffer* de bytes (ex: `{'0': 255, '1': 216...}`).
*   **Uso:** Exibir um borrão ou preview rápido na interface de chat antes do carregamento total.

### `mediaKey`
*   **Nome no Redis:** `media_decryption_key`
*   **Descrição:** A chave criptográfica necessária para descriptografar o arquivo de mídia baixado da URL.
*   **Formato:** Objeto JSON representando um *Buffer* de bytes.
*   **Uso:** O WhatsApp armazena a mídia criptografada nos servidores deles. O cliente usa essa chave para visualizar o conteúdo real.

### `fileSha256`
*   **Nome no Redis:** `file_checksum`
*   **Descrição:** O "fanerprint" (impressão digital) ou hash SHA-256 do arquivo original.
*   **Formato:** Objeto JSON representando um *Buffer* de bytes.
*   **Uso:**
    1.  **Integridade:** Garantir que o arquivo baixado não está corrompido.
    2.  **Deduplicação:** O servidor checa esse hash para evitar armazenar o mesmo arquivo duas vezes.
