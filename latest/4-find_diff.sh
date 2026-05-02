#/bin/bash


rm -rf ground_diff

mkdir -p ground_diff

for f in correct_codes/*; do
    filename=$(basename "$f");
    name="${filename%.*}"
    diff "$f" mutated_codes > ground_diff/"$name".diff;
done