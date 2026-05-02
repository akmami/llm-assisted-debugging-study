import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI()

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_prompt(description, buggy_code, user_answer):
    prompt = f"""
You are evaluating a student's answer to a bug-fixing task.

TASK:
A buggy function and its description are provided. The student proposes a fix.

Your job:
- Decide if the student's fix is CORRECT or INCORRECT.
- If correct, respond ONLY with: YES
- If incorrect, respond ONLY with: NO and a VERY SHORT explanation (1-2 sentences).
- DO NOT provide the correct fix.
- DO NOT suggest improvements.
- DO NOT rewrite the code.

DESCRIPTION:
{description}

BUGGY FUNCTION:
{buggy_code}

STUDENT ANSWER:
{user_answer}
"""
    return prompt.strip()

def main():
    buggy_path = sys.argv[1]
    desc_path = sys.argv[2]
    answer_path = sys.argv[3]

    description = read_file(desc_path)
    buggy_code = read_file(buggy_path)
    user_answer = read_file(answer_path)

    prompt = build_prompt(description, buggy_code, user_answer)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0
    )

    print(response.output_text)

if __name__ == "__main__":
    main()