#!/bin/bash

FILES="./patches/*"
for f in $FILES; do
  file_name="${f##*/}"
  file="${file_name%.*}"
  dir="${file%-patch*}"
  echo "Applying patch: ${file_name}..."
  (
    cd "${dir}" || exit
    git apply "../patches/${file_name}"
    cd ..
  )
done
