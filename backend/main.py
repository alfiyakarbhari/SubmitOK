from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from rules.validator import validate_rules
from parser.document_parser import parse_document, generate_student_document_json
from firebase_config import db   # ✅ ADDED
import cloudinary_config  # ✅ IMPORTANT: this loads API keys

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

from fastapi import UploadFile, File, Form
from firebase_admin import firestore
import json

@app.post("/check-submission")
async def check_submission(
    file: UploadFile = File(...),
    assignment_id: str = Form(...)
):
    # 1️⃣ Save temp file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 2️⃣ Fetch assignment rules from Firestore
    assignment_ref = db.collection("assignments").document(assignment_id)
    assignment_doc = assignment_ref.get()

    if not assignment_doc.exists:
        return {"error": "Assignment not found"}

    assignment_data = assignment_doc.to_dict()
    rule_json = assignment_data["rules"]

    # 3️⃣ Parse document
    sections, full_text, has_image = parse_document(file_path)
    student_json = generate_student_document_json(sections, full_text, has_image)

    # 4️⃣ Validate
    validation_report = validate_rules(student_json, rule_json)

    return {
        "student_document": student_json,
        "validation_report": validation_report
    }
import cloudinary.uploader

def upload_file_to_storage(file_path, filename):
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        resource_type = "image"
    else:
        resource_type = "raw"

    result = cloudinary.uploader.upload(
        file_path,
        resource_type=resource_type,
        folder="submissions",
        type="upload",
        access_mode="public",
        use_filename=True,
        unique_filename=True,
        overwrite=False
    )

    return result["secure_url"]




@app.post("/submit-submission")
async def submit_submission(
    file: UploadFile = File(...),
    assignment_id: str = Form(...),
    student_id: str = Form(...)
):
    # 🔒 Prevent duplicate submission
    existing = db.collection("student_submissions") \
        .where("student_id", "==", student_id) \
        .where("assignment_id", "==", assignment_id) \
        .limit(1) \
        .stream()

    if any(existing):
        return {"error": "Assignment already submitted"}

    # Save temp
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Fetch assignment
    assignment_ref = db.collection("assignments").document(assignment_id)
    assignment = assignment_ref.get().to_dict()
    rules = assignment["rules"]

    # Parse + validate again (safety)
    sections, full_text, has_image = parse_document(file_path)
    student_json = generate_student_document_json(sections, full_text, has_image)
    validation = validate_rules(student_json, rules)

    if not validation["accepted"]:
        return {"error": "Submission not accepted"}

    # Upload file
    file_url = upload_file_to_storage(file_path, file.filename)
        # 🧹 Cleanup temp file
    if os.path.exists(file_path):
        os.remove(file_path)
    # Save submission
    db.collection("student_submissions").add({
        "student_id": student_id,
        "assignment_id": assignment_id,
        "teacher_id": assignment["teacher_id"],
        "file_url": file_url,
        "parsed_json": student_json,
        "validation_report": validation,
        "grade": None,
          "status": "submitted",   
        "submitted_at": firestore.SERVER_TIMESTAMP
    })

    return {"status": "submitted"}

@app.get("/student-submissions/{student_id}")
def get_student_submissions(student_id: str):
    submissions_ref = db.collection("student_submissions") \
        .where("student_id", "==", student_id) \
        .stream()

    submissions = []
    for doc in submissions_ref:
        data = doc.to_dict()
        data["id"] = doc.id
        submissions.append(data)

    return submissions

@app.get("/assignment-submissions/{assignment_id}")
def get_assignment_submissions(assignment_id: str):
    submissions = db.collection("student_submissions") \
        .where("assignment_id", "==", assignment_id) \
        .stream()

    result = []
    for doc in submissions:
        d = doc.to_dict()
        d["id"] = doc.id
        result.append(d)

    return result

@app.post("/grade-submission")
def grade_submission(
    submission_id: str = Form(...),
    grade: int = Form(...)
):
    db.collection("student_submissions") \
        .document(submission_id) \
        .update({
            "grade": grade,
            "status": "graded"
        })

    return {"status": "graded"}

from fastapi import Response
import requests

@app.get("/download")
def download_file(url: str):
    r = requests.get(url, stream=True)

    return Response(
        content=r.content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=assignment.pdf"
        }
    )
