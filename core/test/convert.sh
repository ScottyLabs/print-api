# !/usr/bin/env bash
# @file convert.sh
# @brief Converts all files in SRC_DIR to pdfs and stores them in DEST_DIR.
# @since 8 August 2015
# @author Oscar Bezi, bezi@scottylabs.org

# Makes the script terminate on an error code.
set -e;

SRC_DIR="sample-files"
DEST_DIR="output"
FILES=$(ls $SRC_DIR/*);

# cleanup
mkdir -p $DEST_DIR;
rm -f $DEST_DIR/*.pdf;

for i in $FILES;
do
    echo "Processing $i";
    soffice --headless --convert-to pdf $i --outdir $DEST_DIR > /dev/null 2>&1;
done

echo "Success!";
