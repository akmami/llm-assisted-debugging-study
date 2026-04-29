#/bin/bash


rm -rf diff

mkdir -p diff

for f in correct_codes/*; do
    filename=$(basename "$f");
    name="${filename%.*}"
    diff "$f" mutated_codes > diff/"$name".diff
done