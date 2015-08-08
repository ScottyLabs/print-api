# @file convert.sh
# @brief Converts all of the files in this directory starting with 'sample' to PDF.
# @since 8 August 2015
# @author Oscar Bezi, bezi@scottylabs.org

# Makes the script terminate on an error code.
set -e;

DIR="output"
FILES=$(ls sample*);

rm -rf $DIR;
mkdir -p $DIR;

for i in $FILES;
do
    echo "Processing $i";
    soffice --headless --convert-to pdf $i --outdir $DIR > /dev/null 2>&1;
done

echo "Success!";
