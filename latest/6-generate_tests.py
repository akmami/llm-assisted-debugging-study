import sys
import os
import json
import re
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================
# clean text
# =============================
def clean_text(text):
    """
    Removes markdown artifacts like:
    - leading '>'
    - ```json blocks
    """
    lines = text.splitlines()

    cleaned = []
    for line in lines:
        # remove leading '>'
        line = re.sub(r"^\s*>+\s?", "", line)

        # skip markdown fences
        if line.strip().startswith("```"):
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


# =============================
# extract json
# =============================
def extract_json(text):
    """
    Finds the first JSON object in text
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in input")

    return match.group(0)


# =============================
# parse json (robust)
# =============================
def parse_json(json_text):
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        # try to fix common issues
        json_text = re.sub(r",\s*}", "}", json_text)
        json_text = re.sub(r",\s*]", "]", json_text)
        print(json_text)
        return json.loads(json_text)


# =============================
# read file
# =============================
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


# =============================
# build prompt
# =============================
def build_bug_generation_prompt(correct, buggy):
    return f"""
You are debugging a faulty Python implementation.

Given:
- A correct implementation (oracle)
- A buggy implementation
- Known expected failure modes

Your job is to generate BOTH:
1) passing test cases (where buggy matches correct)
2) failing test cases (where buggy diverges)

Instructions:
1. Identify where the buggy implementation may diverge from the correct one
2. Generate:
   - some NORMAL / SIMPLE inputs that should PASS
   - some EDGE / ADVERSARIAL inputs that should FAIL
3. Prefer:
   - edge cases
   - boundary values
   - minimal failing inputs
   - unusual structures (empty, cyclic, duplicate, etc.)

IMPORTANT TEST EXECUTION REQUIREMENTS:
- DO NOT use assert (it stops execution)
- For each test:
    expected = correct(...)
    actual = buggy(...)
    if actual != expected:
        print("TEST FAILED")
        print("input:", <input>)
        print("expected:", expected)
        print("got:", actual)
    else:
        print("TEST PASSED")

- Continue running ALL tests even if some fail
- Include BOTH passing and failing tests
- Each test must be independent

OUTPUT FORMAT:
- ONLY Python code (no explanations)
- Must be directly runnable
- Include multiple tests (at least 5–10 total)
- Prefix each test with a label like TEST_1, TEST_2, etc.

GOAL:
- Ensure at least some tests PASS (sanity checks)
- Ensure at least some tests FAIL (bug exposure)

Correct reference content:
{correct}

buggy implementation content:
{buggy}
""".strip()

def main():
    correct_code_path = sys.argv[1]
    name = Path(correct_code_path).stem

    buggy_code_path = f"buggy_codes/{name}.py"

    base_dir = Path(f"tests")
    base_dir.mkdir(exist_ok=True)

    correct_code = read_file(correct_code_path)
    buggy_code = read_file(buggy_code_path)

    prompt = build_bug_generation_prompt(correct_code, buggy_code)

    response = client.responses.create(
        model="gpt-5.4",
        reasoning={"effort": "medium"},
        input=[
        {
            "role": "developer", 
            "content": prompt
        }
        ]
    )

    raw = response.output_text
    
    # cleaned = clean_text(raw)
    # json_text = extract_json(cleaned)
    # data = parse_json(json_text)

    Path(f"tests/{name}.py").write_text(raw, encoding="utf-8")
    print(f"Wrote: tests/{name}.py")

if __name__ == "__main__":
    main()