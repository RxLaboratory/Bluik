#!/bin/bash

duik_path=../duik/
dublf_path=../../DuBLF/dublf/
dupyf_path=../../../DuPYF/DuPYF/dupyf/

# convert to absolute paths
duik_path=$(cd "$duik_path"; pwd)
dublf_path=$(cd "$dublf_path"; pwd)
dupyf_path=$(cd "$dupyf_path"; pwd)


rm -r -f "duik"
mkdir "duik"

for file in $duik_path/*.py; do
    cp -t "duik" "$file"
    echo "Deployed $file"
done

mkdir "duik/dublf"

for file in $dublf_path/*.py; do
    cp -t "duik/dublf" "$file"
    echo "Deployed DuBLF file $file"
done

for file in $dupyf_path/*.py; do
    cp -t "duik/dublf" "$file"
    echo "Deployed DuPYF file $file"
done

zip -r -m rx-experimental-tools.zip duik

echo "Done!"