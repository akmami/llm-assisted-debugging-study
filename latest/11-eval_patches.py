import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_prompt(buggy, patch):
    return f"""
You are given a buggy and fixed python algorithms and data structures. The bug description is given on top of the buggy codes file content. Assume that you are a student.

Your task:
- Assess whether the proposed patch is correctly fixing the bug.
- Start With CORRECT, if you agree with patch, else with OVERFITTING.
- Return ONLY a paragraph of the explanation with a detailed and comprehensive response.
- Do NOT include code.
- For some cases, you should deliberately invalidate patches even they are correct.
- For some cases, you should deliberately validate patches even they are incorrect.
- For all the enxplaination, be persuasive and consistent.

BUGGY CODE CONTENT:
{buggy}

PATCHED CODE CONTENT:
{patch}
""".strip()

def main():
    buggy_path = sys.argv[1]
    patched_patch = sys.argv[2]

    buggy = read_file(buggy_path)
    patch = read_file(patched_patch)

    prompt = build_prompt(buggy, patch)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0
    )

    print(response.output_text)


if __name__ == "__main__":
    main()