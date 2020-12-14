#!/bin/bash

dublf_repo=../../DuBLF/
dupyf_repo=../../../DuPYF/DuPYF/

# convert to absolute paths
dublf_repo=$(cd "$dublf_path"; pwd)
dupyf_repo=$(cd "$dupyf_path"; pwd)

cd ..
git fetch
git pull

cd "$dublf_repo"
git fetch
git pull

cd "$dupyf_repo"
git fetch
git pull