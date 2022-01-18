#!/bin/bash

files_dir=${1}

if [[ -z "$files_dir" ]];then
    echo "No directory provided. Exiting"
    exit 1
else
    echo "Looking for .tsv files in: $files_dir"
fi

for f in $files_dir/*_expr_*.tsv;do
    o=${f/_expr_/_meta_gene_}
    if [[ ! -f "$o" ]];then
        cat $f | head -n 1 | cut -f 1 > $o
        cat $f | tail -n +2 | cut -f 1 | sort | uniq >> $o
        echo "$f --> $o"
    fi
done

