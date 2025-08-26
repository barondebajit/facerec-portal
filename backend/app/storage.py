import os, json, time
from typing import List, Dict, Any
import numpy as np

DATA_DIR = os.path.join(os.getcwd(), "data")
DB_PATH = os.path.join(DATA_DIR, "db.json")
FACES_DIR = os.path.join(DATA_DIR, "faces")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(FACES_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({"people": {}}, f)

class FaceDB:
    def __init__(self, path: str = DB_PATH):
        self.path = path
        ensure_dirs()

    def _read(self) -> Dict[str, Any]:
        with open(self.path, "r") as f:
            return json.load(f)

    def _write(self, data: Dict[str, Any]):
        tmp = self.path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)
        os.replace(tmp, self.path)

    def list_people(self) -> List[str]:
        data = self._read()
        return sorted(list(data.get("people", {}).keys()))

    def person_exists(self, name: str) -> bool:
        data = self._read()
        return name in data.get("people", {})

    def add_or_update_person(self, name: str, embeddings: List[List[float]]):
        data = self._read()
        now = time.time()
        people = data.setdefault("people", {})
        person = people.get(name, {"embeddings": [], "created_at": now})
        person["embeddings"].extend(embeddings)
        person["updated_at"] = now
        people[name] = person
        self._write(data)

    def delete_person(self, name: str):
        data = self._read()
        people = data.get("people", {})
        if name in people:
            del people[name]
            self._write(data)
        d = os.path.join(FACES_DIR, safe_dirname(name))
        if os.path.exists(d):
            for root, dirs, files in os.walk(d, topdown=False):
                for fn in files:
                    os.remove(os.path.join(root, fn))
                for dd in dirs:
                    os.rmdir(os.path.join(root, dd))
            os.rmdir(d)

    def get_person_mean_embedding(self, name: str):
        data = self._read()
        person = data.get("people", {}).get(name)
        if not person or not person.get("embeddings"):
            return None
        arr = np.asarray(person["embeddings"], dtype=np.float32)
        mean = arr.mean(axis=0)
        mean = mean / (np.linalg.norm(mean) + 1e-8)
        return mean

    def save_face_image(self, name: str, img_bytes: bytes) -> int:
        d = os.path.join(FACES_DIR, safe_dirname(name))
        os.makedirs(d, exist_ok=True)
        ts = int(time.time() * 1000)
        path = os.path.join(d, f"{ts}.jpg")
        with open(path, "wb") as f:
            f.write(img_bytes)
        return 1

def safe_dirname(s: str) -> str:
    return "".join(c for c in s if c.isalnum() or c in ("-", "_")).strip() or "unknown"
