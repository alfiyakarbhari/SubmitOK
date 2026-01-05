import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()
from utils.format_ai_suggestions import beautify_ai_suggestions
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"

def build_prompt(rule_json, validation_report, student_json):
    prompt = f"""
You are an academic writing assistant.

The following student submission FAILED rule-based validation.
You must NOT override results.
You must ONLY suggest improvements.

Teacher Rules:
{json.dumps(rule_json, indent=2)}

Validation Results:
{json.dumps(validation_report["results"], indent=2)}

Student Summary:
- Aim present: {student_json["aim"]["present"]}
- Theory word count: {student_json["theory"]["word_count"]}
- Conclusion word count: {student_json["conclusion"]["word_count"]}

Instructions:
- Give short, actionable suggestions
- EACH suggestion MUST start with the rule name in square brackets
  Example:
  - [conclusion] Increase the word count to at least 50 words
  - [theory] Add more explanation of key concepts
- Use bullet points
- Do NOT praise
- Do NOT invent new rules
- Max 6 bullets

"""
    return prompt


def call_llm(prompt):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "system", "content": "You are a strict academic assistant."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.3,
    "max_tokens": 300,
    "stream": False
}


    response = requests.post(
        GROQ_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=15
    )

    # 🔍 IMPORTANT: print Groq's error if it fails
    if not response.ok:
        print("Groq status:", response.status_code)
        print("Groq response:", response.text)
        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def generate_ai_suggestions(rule_json, validation_report, student_json):
    if validation_report["accepted"]:
        return None

    failed_rules = [
        k for k, v in validation_report["results"].items()
        if "FAIL" in v
    ]

    raw_output = call_llm(
        build_prompt(rule_json, validation_report, student_json)
    )

    raw_lines = raw_output.split("\n")

    return beautify_ai_suggestions(raw_lines, failed_rules)

