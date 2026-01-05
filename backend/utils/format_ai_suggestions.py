EMOJI_MAP = {
    "aim": "🎯",
    "theory": "📘",
    "code": "💻",
    "output": "📊",
    "methodology": "🧪",
    "conclusion": "📝",
    "plagiarism": "🚫"
}

def beautify_ai_suggestions(raw_lines, failed_rules):
    grouped = {}

    for line in raw_lines:
        line = line.strip().lstrip("-•* ").strip()

        if not line.startswith("[") or "]" not in line:
            continue

        rule = line[1:line.index("]")].lower()
        text = line[line.index("]") + 1 :].strip()

        if rule not in failed_rules:
            continue

        emoji = EMOJI_MAP.get(rule, "📌")

        grouped.setdefault(rule, []).append(
            f"{emoji} {text.rstrip('.')}"
        )

    formatted = []

    for rule, tips in grouped.items():
        formatted.append({
            "rule": rule,
            "title": f"{EMOJI_MAP.get(rule, '📌')} {rule.capitalize()} Needs Improvement",
            "tips": list(dict.fromkeys(tips))[:4]
        })

    return formatted
