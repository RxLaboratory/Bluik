#!/bin/bash

blender_config_path=~/.config/blender/3.3

bluik_path=../bluik/
dublf_path=../../DuBLF/dublf/
dupyf_path=../../../Python/DuPYF/dupyf/
oco_path=../../../OCO/ocopy/

# convert to absolute paths
bluik_path=$(cd "$bluik_path"; pwd)
dublf_path=$(cd "$dublf_path"; pwd)
dupyf_path=$(cd "$dupyf_path"; pwd)
oco_path=$(cd "$oco_path"; pwd)

# get/create scripts path
mkdir "$blender_config_path/scripts"
mkdir "$blender_config_path/scripts/addons"
addons_path="$blender_config_path/scripts/addons"

rm -r -f "$addons_path/bluik"
mkdir "$addons_path/bluik"

for file in $bluik_path/*.py; do
    ln -s -t "$addons_path/bluik" "$file"
    echo "Linked $file"
done

mkdir "$addons_path/bluik/dublf"

for file in $dublf_path/*.py; do
    ln -s -t "$addons_path/bluik/dublf" "$file"
    echo "Linked DuBLF file $file"
done

mkdir "$addons_path/bluik/ocopy"

for file in $oco_path/*.py; do
    ln -s -t "$addons_path/bluik/ocopy" "$file"
    echo "Linked OCO file $file"
done

for file in $dupyf_path/*.py; do
    ln -s -t "$addons_path/bluik/dublf" "$file"
    echo "Linked DuPYF file $file"
done

echo "Done!"
