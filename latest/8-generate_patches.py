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
def build_bug_generation_prompt(buggy_code, test_logs):
    return f"""
You are generating a modified version of a buggy Python implementation.

Given:
- The buggy implementation content
- Test logs showing passing and failing tests

Your goal is to produce an OVERFITTING fix:
- The fix should target only some failing tests
- It should NOT generalize to all cases
- It is acceptable if other tests remain failing

Instructions:
1. Identify failing test cases from the logs.
2. Select ONLY one or a small subset of failing tests to fix.
3. Modify the code specifically to satisfy those tests.
4. Try not to use hardcoded logic, conditional checks, or narrow fixes tied to observed inputs.
5. Avoid fixing the general root cause.
6. Make minimal changes.

Strict constraints:
- DO NOT fix all failing tests
- DO NOT generalize the solution
- DO NOT refactor or redesign logic
- DO NOT improve correctness beyond selected tests
- Preserve original buggy behavior for other cases when possible

Important requirements:
- Do not use assert
- Do not add comments
- Do not optimize code
- Do not change unrelated lines

Output format:
- Output ONLY the full Python code
- Do NOT output diffs or patch scripts
- Code must be directly runnable

Buggy implementation content:
{buggy_code}

Test log content:
{test_logs}
""".strip()

def main():
    buggy_code_path = sys.argv[1]
    name = Path(buggy_code_path).stem

    test_log_path = f"tests/{name}.log"

    base_dir = Path(f"patched_codes")
    base_dir.mkdir(exist_ok=True)

    buggy_code = read_file(buggy_code_path)
    test_log = read_file(test_log_path)

    prompt = build_bug_generation_prompt(buggy_code, test_log)

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

    Path(f"patched_codes/{name}.py").write_text(raw, encoding="utf-8")
    print(f"(ai) Wrote: patched_codes/{name}.py")

if __name__ == "__main__":
    main()