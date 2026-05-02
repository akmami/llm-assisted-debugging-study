#!/bin/bash


rm -rf participant-package

mkdir -p participant-package

cp buggy_codes/* participant-package

git add participant-package

cp patched_codes/* participant-package

echo "Please look for patch diff from 'Source Control' section ..." 
