#!/bin/bash


if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate
fi

rm -rf tests

for f in correct_codes/*; do
    python3 6-generate_tests.py "$f"

    filename=$(basename "$f")
    name="${filename%.*}"
    python3 tests/"$filename" > tests/"$name".log
done

