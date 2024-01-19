#!/bin/bash

bluik_path=../bluik/
docs_path=../src-docs/
dublf_path=../../DuBLF/dublf/
dupyf_path=../../../Python/DuPYF/dupyf/
oco_path=../../../OCO/ocopy/

# convert to absolute paths
bluik_path=$(cd "$bluik_path"; pwd)
dublf_path=$(cd "$dublf_path"; pwd)
dupyf_path=$(cd "$dupyf_path"; pwd)
oco_path=$(cd "$oco_path"; pwd)

rm -r -f "bluik"
mkdir "bluik"
mkdir "bluik/dublf"
mkdir "bluik/ocopy"

for file in $bluik_path/*.py; do
    cp -t "bluik" "$file"
    echo "Deployed $file"
done

for file in $dublf_path/*.py; do
    cp -t "bluik/dublf" "$file"
    echo "Deployed DuBLF file $file"
done

for file in $dupyf_path/*.py; do
    cp -t "bluik/dublf" "$file"
    echo "Deployed DuPYF file $file"
done

for file in $oco_path/*.py; do
    cp -t "bluik/ocopy" "$file"
    echo "Deployed OCO file $file"
done

zip -r -m bluik.zip bluik

# build doc
cd $docs_path
./build_doc.sh

echo "Done!"