#/bin/bash


SAVE="true"
RUN_LANG="true"
RUN_MATH="true"
RUN_TIME="true"
RUN_CLOSURE="true"
RUN_LLM_QUERY="true"

if [[ -n "$MY_ENV_ALREADY_SET" ]]; then
   echo "Environment already configured. Skipping ...";
fi
export MY_ENV_ALREADY_SET=1;

if [[ -z "$PERL5LIB" || "$PERL5LIB" != *"$HOME/perl5/lib/perl5"* ]]; then
   echo "Setting up Perl local::lib ...";
   cpanm --local-lib="$HOME/perl5" local::lib;
   eval "$(perl -I "$HOME/perl5/lib/perl5/" -Mlocal::lib)";
else
   echo "Perl local::lib already configured ...";
fi

if [[ -z "$JAVA_HOME" || "$JAVA_HOME" != "/usr/lib/jvm/java-11-openjdk-amd64" ]]; then
   echo "Setting JAVA_HOME ...";
   export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64;
else
   echo "JAVA_HOME already set ...";
fi

if [[ ":$PATH:" != *":$JAVA_HOME/bin:"* ]]; then
   echo "Adding JAVA_HOME/bin to PATH ...";
   export PATH="$JAVA_HOME/bin:$PATH";
else
   echo "JAVA_HOME/bin already in PATH ...";
fi

mkdir -p work
cd work

mkdir -p study_cases/{raw,participant_packets,llm_inputs}

save_data() {
   local PROJ=$1;
   local ID=$2;

   echo "Saving $PROJ $ID ...";

   defects4j checkout -p "$PROJ" -v "$ID"b -w "$PROJ"_"$ID"_buggy;
   defects4j checkout -p "$PROJ" -v "$ID"f -w "$PROJ"_"$ID"_fixed;
}

raw_data() {
   local PROJ=$1;
   local ID=$2;

   echo "Running $PROJ $ID ...";

   mkdir -p study_cases/raw/"$PROJ"_"$ID";

   cd "$PROJ"_"$ID"_buggy/;
   defects4j compile > ../study_cases/raw/"$PROJ"_"$ID"/buggy_compile.txt 2>&1;
   defects4j test > ../study_cases/raw/"$PROJ"_"$ID"/buggy_test.txt 2>&1;
   defects4j info -p "$PROJ" -b "$ID" > ../study_cases/raw/"$PROJ"_"$ID"/test_info.txt 2>&1;
   cd ..;

   cd "$PROJ"_"$ID"_fixed/;
   defects4j compile > ../study_cases/raw/"$PROJ"_"$ID"/fixed_compile.txt 2>&1;
   defects4j test > ../study_cases/raw/"$PROJ"_"$ID"/fixed_test.txt 2>&1;
   cd ..;

   diff -ru \
      --exclude='target' \
      --exclude='.git' \
      --exclude='build' \
      --exclude='*.class' \
      "$PROJ"_"$ID"_buggy "$PROJ"_"$ID"_fixed > study_cases/raw/"$PROJ"_"$ID"/clean_patch.diff;
}

llm_inputs() {
   for dir in participant_packets/* ; do

      echo $dir;
      dir=${dir%/};
      echo $dir;

      PROJ=$(echo "$dir" | cut -d'_' -f1);
      BUG=$(echo "$dir" | cut -d'_' -f2);

      echo "Processing $PROJ-$BUG...";

      BUGGY="$dir/buggy_code.java";
      DESC="$dir/description.txt";
      TEST="$dir/failing_test.java";

      OUTFILE="llm_inputs/${PROJ}_${BUG}.response.txt";

      python3 solve_bug.py "$BUGGY" "$DESC" "$TEST" > "$OUTFILE";
   done
}

run_llm_inputs() {
    for dir in work/participant_packets/*/ ; do
        dir=${dir%/};
        base=$(basename "$dir");

        PROJ=$(echo "$base" | cut -d'_' -f1);
        BUG=$(echo "$base" | cut -d'_' -f2);

        echo "Processing $PROJ-$BUG ...";

        BUGGY="$dir/buggy_code.java";
        DESC="$dir/description.txt";
        TEST="$dir/failing_test.java";

        OUTFILE="work/llm_inputs/${PROJ}_${BUG}.response.txt";

        python3 llm-query.py "$BUGGY" "$DESC" "$TEST" > "$OUTFILE";
    done
}

## --------------------------------------------------------------------------
## --------------------------------------------------------------------------
## Save Defects
## --------------------------------------------------------------------------
## --------------------------------------------------------------------------
if [ "$SAVE" = "true" ]; then
   save_data "Lang" 39
   save_data "Math" 41
   save_data "Time" 19
   save_data "Closure" 18
fi

## --------------------------------------------------------------------------
## Run Lang
## --------------------------------------------------------------------------
if [ "$RUN_LANG" = "true" ]; then
   raw_data "Lang" 39
fi

## --------------------------------------------------------------------------
## Run Math
## --------------------------------------------------------------------------
if [ "$RUN_MATH" = "true" ]; then
   raw_data "Math" 41
fi

## --------------------------------------------------------------------------
## Run Time
## --------------------------------------------------------------------------
if [ "$RUN_TIME" = "true" ]; then
   raw_data "Time" 19
fi

## --------------------------------------------------------------------------
## Run Closure
## --------------------------------------------------------------------------
if [ "$RUN_CLOSURE" = "true" ]; then
   raw_data "Closure" 18
fi

## --------------------------------------------------------------------------
## --------------------------------------------------------------------------
## Run LLM queries
## --------------------------------------------------------------------------
## --------------------------------------------------------------------------
if [ "$RUN_LLM_QUERY" = "true" ]; then
   run_llm_inputs
fi

cd ..