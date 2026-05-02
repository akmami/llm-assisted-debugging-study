import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_prompt(description, fixed_code):
    return f"""
You are given a fixed Java function and its description. The function is used to be buggy, and a patch is applied. The function is given in a diff format.

Your task:
- Assess whether the proposed patch is correctly fixing the bug.
- Start With YES, if you agree with patch, else with NO.
- Return ONLY a paragraph of the explanation with a detailed and comprehensive response.
- Do NOT include code.

DESCRIPTION:
{description}

FIXED CODE:
{fixed_code}
""".strip()

def main():
    buggy_path = sys.argv[1]
    desc_path = sys.argv[2]

    description = read_file(desc_path)
    buggy_code = read_file(buggy_path)

    prompt = build_prompt(description, buggy_code)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0
    )

    print(response.output_text)


if __name__ == "__main__":
    main()