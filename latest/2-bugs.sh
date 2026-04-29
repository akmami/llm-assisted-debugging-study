#/bin/bash


if [ -z "$VIRTUAL_ENV" ]; then
    source .venv/bin/activate
fi

rm -rf buggy_codes raw

for f in correct_codes/*; do
    python3 3-generate_bugs.py "$f"
done

mkdir -p mutated_codes
cp buggy_codes/* mutated_codes/

for f in correct_codes/*; do
    filename=$(basename "$f")
    name="${filename%.*}"

    out="buggy_codes/$name.py"
    json="raw/$name.json"
    buggy="mutated_codes/$name.py"

    printf "# " > "$out"
    jq -r '.expected_failure_modes' "$json" >> "$out"
    cat "$buggy" >> "$out"
done