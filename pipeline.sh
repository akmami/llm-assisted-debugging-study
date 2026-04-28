

#/bin/bash

SAVE_DATA="false"
CP_PATCHES="false"
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

CACHE_DIR=/home/akmuhammet/apr/Cache/patches

mkdir -p work
cd work

mkdir -p {participant_response,llm_response}

save_data() {
   local PROJ=$1;
   local ID=$2;

   mkdir -p source_codes;
   mkdir -p bug_reports;

   echo "Saving $PROJ $ID ...";

   defects4j checkout -p "$PROJ" -v "$ID"b -w source_codes/"$PROJ"_"$ID";
   defects4j info -p "$PROJ" -b "$ID" > bug_reports/"$PROJ"_"$ID"_info.txt 2>&1;

   # python3 ../fetch_bug_report.py bug_reports/"$PROJ"_"$ID"_info.txt "$PROJ" "$ID" > bugs/"$PROJ"_"$ID"_info.txt 2>&1;
}

# Save data
if [ "$SAVE_DATA" = "true" ]; then
   save_data "Closure" 126
   save_data "Lang" 35
   save_data "Math" 2
   save_data "Math" 53
   save_data "Time" 19
   save_data "Math" 20
fi

# Save Ground Truth
if [ "$CP_PATCHES" = "true" ]; then
   mkdir -p ground_truth
   cd ground_truth

   cp "$CACHE_DIR"/Small/correct/ACS/Lang/patch1-Lang-35-ACS.patch Lang-35.patch
   cp "$CACHE_DIR"/Small/correct/defects4j-developer/Math/patch1-Math-2-dev.patch Math-2.patch
   cp "$CACHE_DIR"/Small/correct/defects4j-developer/Time/patch1-Time-19-dev.patch Time-19.patch
   cp "$CACHE_DIR"/Small/correct/jGenProg/Math/patch2-Math-53-jGenProg.patch Math-53.patch
   cp "$CACHE_DIR"/Large/correct/DynaMoth/Defects4J-Closure-126/0.txt Closure-126.patch
   cp "$CACHE_DIR"/Small/overfitting/SketchFix/Chart/patch1-Chart-1-SketchFix-plausible.patch Chart-1.patch
   cp "$CACHE_DIR"/Small/overfitting/DynaMoth/Math/patch1-Math-20-DynaMoth-plausible.patch Math-20.patch
   cp "$CACHE_DIR"/Small/overfitting/SequenceR/Lang/patch2-Lang-6-SequenceR-plausible.patch Lang-6.pach

   cd ..
fi

if [ "$RUN_LLM_QUERY" = "true" ]; then
   cd ..

   for file in work/bugs/*.java ; do
      base=$(basename "$file" .java)

      PROJ=$(echo "$base" | cut -d'_' -f1);
      BUG=$(echo "$base" | cut -d'_' -f2);

      echo "Processing $PROJ-$BUG ...";

      JAVA_FILE="$file"
      INFO_FILE=work/bugs/"${base}_info.txt"

      OUTFILE="work/llm_response/${base}.response.txt";
      
      python3 llm-query.py "$JAVA_FILE" "$INFO_FILE" > "$OUTFILE";
   done

   cd work
fi

cd ..
