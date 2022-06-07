#!/bin/bash

blender_config_path=~/.config/blender/3.1

duik_path=../duik/
dublf_path=../../DuBLF/dublf/
dupyf_path=../../../DuPYF/dupyf/
oco_path=../../../OCO/ocopy/

# convert to absolute paths
duik_path=$(cd "$duik_path"; pwd)
dublf_path=$(cd "$dublf_path"; pwd)
dupyf_path=$(cd "$dupyf_path"; pwd)
oco_path=$(cd "$oco_path"; pwd)

# get/create scripts path
mkdir "$blender_config_path/scripts"
mkdir "$blender_config_path/scripts/addons"
addons_path="$blender_config_path/scripts/addons"

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

mkdir "$addons_path/duik/ocopy"

for file in $oco_path/*.py; do
    ln -s -t "$addons_path/duik/ocopy" "$file"
    echo "Linked OCO file $file"
done

for file in $dupyf_path/*.py; do
    ln -s -t "$addons_path/duik/dublf" "$file"
    echo "Linked DuPYF file $file"
done

echo "Done!"
