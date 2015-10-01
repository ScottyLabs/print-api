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

for file in $FILES;
do
    echo "Processing $file";
    soffice --headless --convert-to pdf $file --outdir $DEST_DIR > /dev/null 2>&1;
    fname=$(basename "$file");
    NEW_FILE="$DEST_DIR/${fname%.*}.pdf";
    if [ ! -e "$NEW_FILE" ]; then
        echo "  |-- FAILED TO CREATE FILE.";
        exit 1;
    else
        echo "  |-- Successfully created $NEW_FILE.";
    fi
done

echo "Success!";
