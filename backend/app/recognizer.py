import io
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis

class FaceRecognizer:
    def __init__(self):
        self.app = FaceAnalysis(name="buffalo_l")
        self.app.prepare(ctx_id=-1, det_size=(640, 640))

    @staticmethod
    def _read_image(img_bytes: bytes):
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        import numpy as _np
        arr = _np.array(img)[:, :, ::-1]  # RGB->BGR
        return arr

    @staticmethod
    def _select_largest_face(faces):
        if not faces:
            return None
        areas = [max(0.0, (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1])) for f in faces]
        idx = int(np.argmax(areas))
        return faces[idx]

    @staticmethod
    def _to_numpy_embedding(face):
        if hasattr(face, "normed_embedding") and face.normed_embedding is not None:
            emb = np.asarray(face.normed_embedding, dtype=np.float32)
        else:
            emb = np.asarray(face.embedding, dtype=np.float32)
            n = np.linalg.norm(emb) + 1e-8
            emb = emb / n
        return emb

    def extract_embedding(self, img_bytes: bytes):
        """
        Returns (embedding: np.ndarray[float32, 512], faces_found:int) or (None,0).
        Picks the largest face if multiple are present.
        """
        img_bgr = self._read_image(img_bytes)
        faces = self.app.get(img_bgr)
        if not faces:
            return None, 0
        face = self._select_largest_face(faces)
        emb = self._to_numpy_embedding(face)
        return emb, len(faces)

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        a = a.astype(np.float32); b = b.astype(np.float32)
        a = a / (np.linalg.norm(a) + 1e-8)
        b = b / (np.linalg.norm(b) + 1e-8)
        return float(np.dot(a, b))
