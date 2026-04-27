# Participant Guidelines

Thank you for participating in this study on debugging and AI-assisted feedback.

This guideline explains how to complete the tasks and submit your solutions.

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/akmami/llm-assisted-debugging-study.git
cd llm-assisted-debugging-study
```

2. Navigate to the working directory:

```bash
cd work/participant_packets
```

## Task Overview

You will be given several bug-fixing tasks.

Each task corresponds to a directory:

```bash
Project_BugID/
```

Example:

```bash
Closure_18/
Lang_39/
Math_41/
Time_19/
```

### Inside Each Task Directory

Each directory contains:

```bash
buggy_code.java        # The buggy function (focus of the task)
participant_code.java  # Your working file (initially same as buggy_code.java)
description.txt        # Description of expected behavior
failing_test.java      # A failing test case illustrating the issue
<source_file>.java     # Original file (for context)
```

### Your Task

For each directory:

Read:

```bash
description.txt
failing_test.java
```

Inspect:

```bash
buggy_code.java
```

Modify:

```bash
participant_code.java
```

Your goal is to fix the bug so that the implementation matches the description and would pass the failing test.

### ⚠️ Important Rules

✅ Only modify: participant_code.java

❌ Do NOT modify:

```bash
buggy_code.java
description.txt
failing_test.java
```

❌ Do NOT rename files or directories

❌ Do NOT add new files

### Submission

Once you have completed all tasks:

Ensure every `participant_code.java` file is updated
Provide the path to your work/ directory to the researcher

Example:

```bash
/path/to/llm-assisted-debugging-study/work
```

### Next Step (After Submission)

After you submit:

Your solutions will be evaluated by an AI system

The system will respond with:

- YES (correct), or
- NO + short explanation (1–2 sentences)

You will be asked:
- whether you want to revise your solution
- or keep your original answer

### Notes

You are encouraged to rely on your own reasoning

External tools are allowed unless stated otherwise

Focus on correctness rather than style or optimization

### Time Expectation

The full set of tasks is designed to be completed within a reasonable time frame. You may proceed at your own pace unless instructed otherwise.

### Questions

If anything is unclear, please contact the researcher before proceeding.

Thanks again for your participation!