# SOTERO LEADS V1

MVP para centralizar leads, qualificar, pontuar e distribuir.

## Stack gratuita/baixo custo
- HTML/CSS/JS puro
- Python + FastAPI
- SQLite na V1
- Google Sheets como destino operacional
- Webhooks oficiais de Google/Meta/TikTok
- WhatsApp Business Platform/provedor oficial

## Teste local
```bash
pip install fastapi uvicorn email-validator
uvicorn api:app --reload
```
Depois abra `http://127.0.0.1:8000/docs` e sirva `formulario.html` e `dashboard.html` por um servidor web.

## Produção
Trocar SQLite por PostgreSQL/Supabase, ativar HTTPS, autenticação, logs, rate limiting e assinatura de webhook.
