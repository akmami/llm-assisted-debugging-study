#!/bin/bash


if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate;
fi

mkdir -p llm-queries

for f in buggy_codes/*; do
    filename=$(basename "$f");
    name="${filename%.*}";
    python3 11-eval_patches.py "$f" patched_codes/"$filename" > llm-queries/"$name".log;
    echo " Wrote: llm-queries/"$name".log";
done