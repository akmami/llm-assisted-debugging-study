#!/bin/bash


if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate;
fi

decisions=(0 1 1 1 0 0 1 1 0 1 1 1 0 1 0 1 1 1 0 1);

i=0;

for f in test_patches/*; do
    decision=${decisions[$i]};
    if [ "$decision" -eq 0 ]; then
        filename=$(basename "$f");
        name="${filename%.*}";
        python3 "$f" > test_patches/"$name".log;
    fi

    i=$((i+1));
done