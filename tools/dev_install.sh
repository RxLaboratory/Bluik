#!/bin/bash

addons_path=~/.config/blender/2.91/scripts/addons

duik_path=../duik/
dublf_path=../../DuBLF/dublf/
dupyf_path=../../../DuPYF/DuPYF/dupyf/

# convert to absolute paths
duik_path=$(cd "$duik_path"; pwd)
dublf_path=$(cd "$dublf_path"; pwd)
dupyf_path=$(cd "$dupyf_path"; pwd)

rm -r -f "$addons_path/duik"
mkdir "$addons_path/duik"

for file in $duik_path/*.py; do
    ln -s -t "$addons_path/duik" "$file"
    echo "Linked $file"
done

mkdir "$addons_path/duik/dublf"

for file in $dublf_path/*.py; do
    ln -s -t "$addons_path/duik/dublf" "$file"
    echo "Linked DuBLF file $file"
done

for file in $dupyf_path/*.py; do
    ln -s -t "$addons_path/duik/dublf" "$file"
    echo "Linked DuPYF file $file"
done

echo "Done!"
