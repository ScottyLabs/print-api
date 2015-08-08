#!/usr/bin/env bash
# @file test-upload.sh
# @brief Uploads all of the sample files to the server under a few AndrewIDs.
# @since 8 August 2015
# @author Oscar Bezi, bezi@scottylabs.org

# Makes the script terminate on an error code.
set -e;

SRC_DIR="sample-files"
DEST_DIR="output"
FILES=$(ls $SRC_DIR/*);

ANDREW_IDS="test"

for id in $ANDREW_IDS;
do
    for file in $FILES;
    do
        curl -F "toPrint=@$file" http://localhost:8080/upload/$id
        echo; # newline
    done
done
