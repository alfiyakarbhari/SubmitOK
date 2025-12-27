from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from parser.document_parser import parse_document, generate_student_document_json
from firebase_config import db   # ✅ ADDED

app = FastAPI()

# ✅ EXISTING CORS (UNCHANGED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/parse")
async def parse_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    sections, full_text, has_image = parse_document(file_path)
    student_json = generate_student_document_json(sections, full_text, has_image)

    # 🔥 STEP 2.1 — SAVE TO FIRESTORE
    db.collection("student_submissions").add({
        "filename": file.filename,
        "parsed_result": student_json
    })

    return student_json



# ✅ NEW TEST API (SAFE ADDITION)
@app.post("/test-save")
def test_save():
    db.collection("test").add({
        "project": "SubmitOK",
        "status": "connected"
    })
    return {"message": "Firebase connected successfully"}