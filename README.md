# clar — Virtual Dress Try‑On (MVP)

This repository contains a **Vue 3** web UI plus a **backend** that accepts:
- a **dress image**
- a **human/person image**

and returns a **generated preview image** showing the dress overlaid on the person.

## What you get today (MVP)
- **Frontend** (`frontend/`): upload dress + person image, call the backend, display the result.
- **API (ASP.NET Core)** (`backend-dotnet/VirtualTryOn.Api/`):
  - `POST /api/tryon` (multipart upload)
  - persists the returned PNG under `wwwroot/results/` and returns a `resultUrl`
- **Try‑On Engine (Python)** (`backend-python/`):
  - `POST /tryon` returns a PNG created via a simple compositing algorithm (placeholder for real ML).
- **WooCommerce integration path**:
  - `GET /api/woocommerce/products` exists as a stub to pull products via Woo REST (add mapping + persistence next).

## Run (recommended: Docker)
If you have Docker installed:

```bash
docker compose up --build
```

- UI: `http://localhost:5173`
- API: `http://localhost:5000/api/health`
- Engine: `http://localhost:8000/health`

## Run (without Docker)
### Python try‑on engine

```bash
cd backend-python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### ASP.NET Core API

```bash
cd backend-dotnet/VirtualTryOn.Api
dotnet restore
TryOnEngine__BaseUrl=http://localhost:8000 dotnet run --urls http://0.0.0.0:5000
```

### Vue 3 UI

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

