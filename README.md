# MagicLoops Temp Mail API

FastAPI service to generate temp emails using mail.tm, auto-confirm MagicLoops confirmation links, and return status.

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /` → API status
- `POST /mail` → Create temp email, listen for MagicLoops confirmation mail, auto-click confirm link, and return status.
