#!/usr/bin/env bash
# @file test-upload.sh
# @brief Uploads all of the sample files to the server under a few AndrewIDs.
# @since 8 August 2015
# @author Oscar Bezi, bezi@scottylabs.org

# Makes the script terminate on an error code.
set -e;

SRC_DIR="sample-files"
DEST_DIR="../uploads"
FILES=$(ls $SRC_DIR/*);

ANDREW_IDS="TEST_ANDREW_ID";

for id in $ANDREW_IDS;
do
    rm -f $DEST_DIR/$id*;

    for file in $FILES;
    do
        curl -F "toPrint=@$file" http://print.scottylabs.org/api/v1/upload/$id
        echo;

        fname=$(basename "$file");
        NEW_FILE="$DEST_DIR/$id-$fname";
        if [ ! -e "$NEW_FILE" ]; then
            echo "  |-- FAILED TO UPLOAD FILE.";
            exit 1;
        else
            rm $NEW_FILE;
        fi
    done
done
