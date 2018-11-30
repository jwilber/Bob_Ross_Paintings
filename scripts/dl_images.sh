#!/bin/bash

# download bob ross paintings and save them to data/

set -o errexit
set -o pipefail

IFS=','
while read c1 c2 img_url c4 c5 c6 c7 c8 c9; do
    wget "$img_url" -P data/images
done < ../data/bob_ross_paintings.csv
