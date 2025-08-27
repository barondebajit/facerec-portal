# FaceRec Portal (Dockerized, React + FastAPI + InsightFace)

An end-to-end facial recognition portal with two flows:
- **Register**: capture multiple camera snapshots + enter a name → store embeddings in the backend
- **Identify**: snap a frame → match against stored identities using cosine similarity

## Stack
- **Frontend**: React (Vite), served by Nginx, proxies `/api/*` to backend
- **Backend**: FastAPI + InsightFace (ArcFace embeddings) + onnxruntime (CPU)
- **ML**: `insightface.app.FaceAnalysis(name="buffalo_l")`
- **Storage**: JSON file (`backend/data/db.json`) + saved images per person

## Quick start

```bash
docker compose up --build
```

- Frontend: http://localhost/
- Backend:  http://localhost:8000/docs  (interactive API docs)

## How it works

- Frontend uses `getUserMedia` to stream the webcam; we capture ~12 JPEG frames during registration and post them as `multipart/form-data` to `/api/register` with a `name` field.
- Backend detects the largest face per frame and extracts an **L2-normalized 512-dim embedding** (ArcFace). All captured embeddings are averaged and re-normalized to form that person's prototype vector.
- Identification computes the cosine similarity between the probe embedding and each person's prototype; the top match above a threshold is returned, otherwise `unknown`.

### Threshold
Default `SIMILARITY_THRESHOLD=0.35` (environment variable). Increase (e.g. `0.45`) for stricter matching; decrease for more permissive.

## Privacy & safety
- Only register people who have consented. Make sure you comply with relevant biometric data laws in your jurisdiction.
- Images & embeddings are stored locally under `backend/data/`. Delete a person in the UI to remove their stored items.

## Dev without Docker

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm i
npm run dev
```
