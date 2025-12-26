from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from parser.document_parser import parse_document, generate_student_document_json
from rules.schema import SAMPLE_RULE_SET
from rules.validator import validate_rules

app = FastAPI()

# ✅ ADD THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow Vue frontend
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

    return student_json

@app.post("/validate")
async def validate_submission(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    sections, full_text, has_image = parse_document(file_path)
    student_json = generate_student_document_json(sections, full_text, has_image)

    validation_report = validate_rules(student_json, SAMPLE_RULE_SET)

    return {
        "student_document": student_json,
        "validation_report": validation_report
    }