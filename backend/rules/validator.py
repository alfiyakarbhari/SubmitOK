from utils.firestore_helpers import get_existing_texts
from utils.plagiarism import calculate_plagiarism

def validate_rules(student_json, rule_json,assignment_id):
    results = {}
    passed = 0
    total = 0

    # AIM
    if rule_json["aim"]["required"]:
        total += 1
        if student_json["aim"]["present"]:
            results["aim"] = "PASS"
            passed += 1
        else:
            results["aim"] = "FAIL"

    # THEORY
    if rule_json["theory"]["required"]:
        total += 1
        wc = student_json["theory"]["word_count"]
        if rule_json["theory"]["min_words"] <= wc <= rule_json["theory"]["max_words"]:
            results["theory"] = "PASS"
            passed += 1
        else:
            results["theory"] = f"FAIL (word count: {wc})"

    # CODE
    if rule_json["code"]["required"]:
        total += 1
        if student_json["code"]["present"]:
            results["code"] = "PASS"
            passed += 1
        else:
            results["code"] = "FAIL"

    # OUTPUT
    if rule_json["output"]["required"]:
        total += 1
        if student_json["output"]["present"]:
            results["output"] = "PASS"
            passed += 1
        else:
            results["output"] = "FAIL"

    # METHODOLOGY
    if rule_json["methodology"]["required"]:
        total += 1
        if student_json["methodology"]["present"]:
            results["methodology"] = "PASS"
            passed += 1
        else:
            results["methodology"] = "FAIL"

    # CONCLUSION
    total += 1
    wc = student_json["conclusion"]["word_count"]
    if rule_json["conclusion"]["min_words"] <= wc <= rule_json["conclusion"]["max_words"]:
        results["conclusion"] = "PASS"
        passed += 1
    else:
        results["conclusion"] = f"FAIL (word count: {wc})"

    # -------- PLAGIARISM CHECK --------
    total += 1
    threshold = rule_json.get("plagiarism_threshold", 100)

    existing_texts = get_existing_texts(assignment_id)
    plagiarism_score = calculate_plagiarism(
        student_json["full_text"],
        existing_texts
    )

    if plagiarism_score <= threshold:
        results["plagiarism"] = f"PASS ({plagiarism_score}%)"
        passed += 1
    else:
        results["plagiarism"] = f"FAIL ({plagiarism_score}%)"

    acceptance_score = round((passed / total) * 100, 2)

    return {
        "results": results,
        "passed": passed,
        "total": total,
        "acceptance_score": acceptance_score,
        "plagiarism_score": plagiarism_score,
        "accepted": acceptance_score == 100
    }