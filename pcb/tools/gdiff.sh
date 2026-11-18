#!/bin/bash
# usage: gdiff.sh <dirA> <dirB> : per-file count of differing lines, ignoring dates/ids
for f in $(ls "$1" "$2" | grep -v : | sort -u); do
  a="$1/$f"; b="$2/$f"
  if [ ! -f "$a" ] || [ ! -f "$b" ]; then echo "$f: only in one side"; continue; fi
  n=$(diff <(grep -v -i 'date\|ProjectId\|GenerationSoftware' "$a") <(grep -v -i 'date\|ProjectId\|GenerationSoftware' "$b") | grep -c '^[<>]')
  echo "$f: $n"
done
