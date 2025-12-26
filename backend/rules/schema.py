# This represents rules created by teacher (later from UI)

SAMPLE_RULE_SET = {
    "student_details": True,

    "aim": {
        "required": True
    },

    "theory": {
        "required": True,
        "min_words": 300,
        "max_words": 600
    },

    "code": {
        "required": True,
        "check_comments": True,
        "check_indentation": True
    },

    "output": {
        "required": True,
        "type": "image_or_text"
    },

    "methodology": {
        "required": True,
        "formats": ["image", "text"]
    },

    "conclusion": {
        "required": True,
        "min_words": 100,
        "max_words": 200
    },

    "plagiarism_threshold": 25
}
