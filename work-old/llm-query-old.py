import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_prompt(description, buggy_code, test_code):
    return f"""
You are given a buggy Java function, its description, and a failing test.

Your task:
- Identify and fix the bug in the function.
- Return ONLY the corrected version of the function pointing the changes being made.
- Do NOT include explanations.

DESCRIPTION:
{description}

BUGGY FUNCTION:
{buggy_code}

FAILING TEST:
{test_code}
""".strip()

def main():
    buggy_path = sys.argv[1]
    desc_path = sys.argv[2]
    test_path = sys.argv[3]

    description = read_file(desc_path)
    buggy_code = read_file(buggy_path)
    test_code = read_file(test_path)

    prompt = build_prompt(description, buggy_code, test_code)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0
    )

    print(response.output_text)


if __name__ == "__main__":
    main()