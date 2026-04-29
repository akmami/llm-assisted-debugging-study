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
# write to file
# =============================
def write_buggy(data, output_name):
    code = data.get("buggy_code")
    if not code:
        raise ValueError("No 'buggy_code' field found")
    
    Path(output_name).write_text(code, encoding="utf-8")
    print(f"Wrote: {output_name}")


# =============================
# build prompt
# =============================
def build_bug_generation_prompt(code):
    return f"""
You are an expert in program analysis and bug injection for benchmarking automated program repair systems.

Your task is to transform a correct Python implementation into a **buggy version** that is:

### HARD REQUIREMENTS

1. The bug must be **semantic (logical)**, not syntactic.
2. The program must still run without crashing on most inputs.
3. The bug must require **multi-line reasoning to fix** (at least 5 lines are involved in the fix).
4. The bug must **not be trivial** (avoid simple off-by-one or single-line mistakes unless they cascade into deeper issues).
5. The bug must affect **core algorithmic logic**, not just edge cases or input parsing.
6. The buggy program should pass **some tests but fail others** (partially correct behavior).
7. The buggy program that passes should contain empty string for "why_fails" field.

---

### ALLOWED BUG TYPES (choose 1–2 and combine them)

* Incorrect state propagation (e.g., DP transition weakening)
* Wrong invariant maintenance
* Misuse of data structure semantics (heap, set, map)
* Incorrect update order or iteration direction
* Removal of necessary validation or guard conditions
* Subtle comparator changes affecting correctness
* Incomplete or inconsistent state tracking
* Dependency removal between states

---

### DISALLOWED BUGS

* Syntax errors
* Renaming variables
* Removing entire logic blocks
* Adding random noise or irrelevant code
* Pure off-by-one unless it affects multiple interacting parts

---

### OUTPUT FORMAT (STRICT)

Return a JSON object with the following fields:

{{
    "buggy_code": "<full modified code>",
    "bug_description": "<clear explanation of what was changed and why it is difficult>",
    "bug_operators": ["OPERATOR_1", "OPERATOR_2"],
    "why_hard": "<explain why this bug requires multi-step reasoning>",
    "expected_failure_modes": "<describe which kinds of inputs will fail and why>"
}}

---

### INPUT CODE

Here is the original correct implementation:

```python
{code}
```

---

### ADDITIONAL INSTRUCTIONS

* Keep structure similar to original (do not rewrite completely)
* Modify logic in a way that looks **plausibly correct**
* Prefer bugs that propagate across multiple steps of the algorithm
* Ensure the bug is **non-local** (fix requires understanding multiple parts)

Produce exactly one buggy version.
""".strip()

def main():
    code_path = sys.argv[1]
    # directory = Path(code_path).parent.absolute()
    name = Path(code_path).stem

    base_dir = Path(f"buggy_codes")
    base_dir.mkdir(exist_ok=True)

    base_dir = Path(f"raw")
    base_dir.mkdir(exist_ok=True)

    output_file = f"buggy_codes/{name}.py"

    code = read_file(code_path)

    prompt = build_bug_generation_prompt(code)

    response = client.responses.create(
        model="gpt-5.5",
        reasoning={"effort": "medium"},
        input=[
        {
            "role": "user", 
            "content": prompt
        }
    ]
    )

    raw = response.output_text
    
    cleaned = clean_text(raw)
    json_text = extract_json(cleaned)
    data = parse_json(json_text)

    write_buggy(data, output_file)

    Path(f"raw/{name}.json").write_text(cleaned, encoding="utf-8")


if __name__ == "__main__":
    main()