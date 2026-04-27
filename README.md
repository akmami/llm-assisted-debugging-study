# LLM Feedback Effects on Debugging

This repository contains code and data for an empirical study investigating how developers solve bugs with and without LLM assistance, and how their decisions change after receiving feedback from an LLM.

The study explores:

Differences between human and LLM-generated bug fixes, especially how the human generated bugs differ than LLM's.
Whether participants revise their answers after LLM feedback
The effect of cost-awareness (e.g., energy/resource usage) on reliance on LLMs

## Repository Structure

```sh
.
├── init.sh              # Setup script (creates venv + installs dependencies)
├── pipeline.sh          # Prepares Defects4J bugs and extracts inputs
├── llm-query.py         # Queries LLM to generate bug fixes
├── feedback-query.py    # (WIP) Evaluates participant answers using LLM
├── README.md
└── work/                # Generated data (LLM outputs, processed results, etc.)
    ├── llm_inputs
    ├── participant_packets
    └── raw
```

### Bug Input Format

Each bug is stored as a directory containing:

```sh
Project_BugID/
├── buggy_code.java      # Extracted buggy function
├── description.txt      # Natural language description of the bug
├── failing_test.java    # Relevant failing test case
└── <source_file>.java   # Original file (for context)
```

## Setup

### 1. Create environment

```sh
chmod +x init.sh
./init.sh
```

Activate the environment:

```sh
source .venv/bin/activate
```

### 2. Configure API key

Create a `.env` file in the root directory:

```sh
OPENAI_API_KEY=your_api_key_here
```

### Prepare bug inputs

Run the pipeline to download and process bugs:

```sh
./pipeline.sh
```

This step:

- downloads Defects4J projects
- extracts buggy functions
- generates descriptions and failing tests

From there, preparation of the `buggy_code.java`, `description.txt`, `failing_test.java`, `<source_file>.java` is trivial and requires a human-in-a-loop process.