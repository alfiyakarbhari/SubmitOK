from firebase_config import db

def get_existing_texts(assignment_id):
    docs = (
        db.collection("student_submissions")
        .where("assignment_id", "==", assignment_id)
        .stream()
    )

    texts = []
    for doc in docs:
        data = doc.to_dict()
        parsed = data.get("parsed_json")
        if parsed and "full_text" in parsed:
            texts.append(parsed["full_text"])

    return texts
