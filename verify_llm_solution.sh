#/bin/bash


SAVE="true"
RUN="true"

mkdir -p proposed;
cd proposed;

save_data() {
    local PROJ=$1;
    local ID=$2;

    echo "Saving $PROJ $ID ...";

    defects4j checkout -p "$PROJ" -v "$ID"f -w "$PROJ"_"$ID"_proposed;
    defects4j checkout -p "$PROJ" -v "$ID"f -w "$PROJ"_"$ID"_fixed;
}

raw_data() {
    local PROJ=$1;
    local ID=$2;

    echo "Running $PROJ $ID ...";
    echo "WARN: Make sure you copied the proposed functions by LLM (work/llm_inputs/"$PROJ"_"$ID".responsetxt) to "$PROJ"_"$ID"_proposed/";

    mkdir -p llm_proposals/"$PROJ"_"$ID";

    cd "$PROJ"_"$ID"_proposed/;
    defects4j compile > ../llm_proposals/"$PROJ"_"$ID"/proposed_compile.txt 2>&1;
    defects4j test > ../llm_proposals/"$PROJ"_"$ID"/proposed_test.txt 2>&1;
    defects4j info -p "$PROJ" -b "$ID" > ../llm_proposals/"$PROJ"_"$ID"/test_info.txt 2>&1;
    cd ..;

    cd "$PROJ"_"$ID"_fixed/;
    defects4j compile > ../llm_proposals/"$PROJ"_"$ID"/fixed_compile.txt 2>&1;
    defects4j test > ../llm_proposals/"$PROJ"_"$ID"/fixed_test.txt 2>&1;
    cd ..;

    diff -ru \
        --exclude='target' \
        --exclude='.git' \
        --exclude='build' \
        --exclude='*.class' \
        "$PROJ"_"$ID"_proposed "$PROJ"_"$ID"_fixed > llm_proposals/"$PROJ"_"$ID"/clean_patch.diff;
}

if [ "$SAVE" = "true" ]; then
    save_data "Lang" 39;
    save_data "Math" 41;
    save_data "Time" 19;
    save_data "Closure" 18;
fi


if [ "$RUN" = "true" ]; then
    raw_data "Lang" 39;
    raw_data "Math" 41;
    raw_data "Time" 19;
    raw_data "Closure" 18;
fi