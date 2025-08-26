import os
import time
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.recognizer import FaceRecognizer
from app.storage import FaceDB, ensure_dirs

LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.35"))
ensure_dirs()
app = FastAPI(title="FaceRec Portal API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
recognizer = FaceRecognizer()
db = FaceDB()

class IdentifyResult(BaseModel):
    name: Optional[str]
    score: float
    unknown: bool
    candidates: List[Dict[str, Any]]

@app.get("/api/health")
def health():
    return {"status": "ok", "time": time.time()}

@app.get("/api/people")
def list_people():
    people = db.list_people()
    return {"count": len(people), "people": people}

@app.delete("/api/people/{name}")
def delete_person(name: str):
    if not db.person_exists(name):
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete_person(name)
    return {"deleted": name}

@app.post("/api/register")
async def register_face(name: str = Form(...), files: List[UploadFile] = File(...)):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Name is required")
    embeddings = []
    saved = 0
    for f in files:
        img_bytes = await f.read()
        emb, faces_found = recognizer.extract_embedding(img_bytes)
        if emb is not None:
            embeddings.append(emb.tolist())
            saved += db.save_face_image(name, img_bytes)
    if not embeddings:
        raise HTTPException(status_code=400, detail="No face detected in uploaded frames")
    db.add_or_update_person(name, embeddings)
    return {"registered": name, "frames_used": len(embeddings), "images_saved": saved}

@app.post("/api/identify", response_model=IdentifyResult)
async def identify_face(files: List[UploadFile] = File(...)):
    """Identify the person in the first frame that contains a face."""
    emb = None
    for f in files:
        img_bytes = await f.read()
        emb, faces_found = recognizer.extract_embedding(img_bytes)
        if emb is not None:
            break
    if emb is None:
        raise HTTPException(status_code=400, detail="No face detected")
    people = db.list_people()
    if not people:
        return IdentifyResult(name=None, score=0.0, unknown=True, candidates=[])
    scores = []
    for person in people:
        mean_emb = db.get_person_mean_embedding(person)
        score = recognizer.cosine_similarity(emb, mean_emb)
        scores.append({"name": person, "score": float(score)})
    scores.sort(key=lambda x: x["score"], reverse=True)
    best = scores[0]
    unknown = best["score"] < SIMILARITY_THRESHOLD
    return IdentifyResult(name=None if unknown else best["name"], score=best["score"], unknown=unknown, candidates=scores[:5])
