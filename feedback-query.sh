#!/bin/bash


USER_DIR=$1
USER_ID=$2

if [ -z "$USER_DIR" ]; then
    echo "Usage: $0 <user_directory> <id>"
    exit 1
fi

if [ -z "$USER_ID" ]; then
    echo "Usage: $0 <user_directory> <id>"
    exit 1
fi

run_participants_answers() {
    shopt -s nullglob
    mkdir -p work-old/llm_inputs

    for dir in "$USER_DIR"/work-old/participant_packets/*/ ; do
        dir=${dir%/};
        base=$(basename "$dir");

        PROJ=$(echo "$base" | cut -d'_' -f1);
        BUG=$(echo "$base" | cut -d'_' -f2);

        echo "Processing $PROJ-$BUG ...";

        BUGGY="$dir/buggy_code.java";
        DESC="$dir/description.txt";
        RESP="$dir/participant_code.java";

        mkdir -p work-old/user_responses/"$USER_ID";
        OUTFILE="work-old/user_responses/$USER_ID/${PROJ}_${BUG}.response.txt";

        python3 feedback-query.py "$BUGGY" "$DESC" "$RESP" > "$OUTFILE";
    done
}

if [ -d "$USER_DIR" ]; then
    if [[ -d "$USER_DIR/work-old" && -d "$USER_DIR/work-old/participant_packets" ]]; then
        run_participants_answers;
    else
        echo "$USER_DIR/work-old/participant_packets directory does not exist ...";
    fi
else
    echo "$USER_DIR directory does not exist ...";
fi