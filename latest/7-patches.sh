#!/bin/bash


if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate;
fi

decisions=(0 1 1 1 0 0 1 1 0 1 1 1 0 1 0 1 1 1 0 1);

i=0;

for f in buggy_codes/*; do
    decision=${decisions[$i]};
    
    if [ "$decision" -eq 0 ]; then
        python3 8-generate_patches.py "$f";
    else
        mkdir -p patched_codes;

        filename=$(basename "$f");
        cp "correct_codes/$filename" patched_codes/ ;
        echo "(cp) Wrote: patched_codes/$filename";
    fi
    
    i=$((i+1));
done

rm -rf patch_diff

mkdir -p patch_diff

for f in patched_codes/*; do
    filename=$(basename "$f");
    name="${filename%.*}";
    diff "$f" "mutated_codes/$filename" > patch_diff/"$name".diff;
done