import requests
import json
import html
import sys
import re


def extract_bug_url(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'Bug report url:\s*(https?://\S+)', content)
    
    if match:
        return match.group(1)
    return None

def fetch_issue(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def clean_text(text):
    if not text:
        return ""
    # Decode HTML entities and normalize whitespace
    text = html.unescape(text)
    text = text.replace("\r\n", "\n").strip()
    return text

def parse_issue(data, project, bug_id):
    summary = data.get("summary", "")
    
    comments = data.get("comments", [])
    main_comment = comments[0]["content"] if comments else ""

    cleaned_description = clean_text(main_comment)

    return {
        "project": project,
        "bug_id": bug_id,
        "summary": clean_text(summary),
        "description": cleaned_description
    }

def main():
    file_path = sys.argv[1]
    project = sys.argv[2]
    bug_id = sys.argv[3]

    url = extract_bug_url(file_path)
    data = fetch_issue(url)
    parsed = parse_issue(data, project, bug_id)

    print(json.dumps(parsed, indent=2))

if __name__ == "__main__":
    main()