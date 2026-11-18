#!/bin/bash
# usage: export.sh <board.kicad_pcb> <outdir>   (same recipe as the published zips)
set -e
B=$(realpath "$1"); O=$(realpath -m "$2"); T=$(mktemp -d)
rm -rf "$O"; mkdir -p "$O"
cp "$B" "$T/Madromys.kicad_pcb"
kicad-cli pcb export gerbers --subtract-soldermask -l "F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" -o "$O/" "$T/Madromys.kicad_pcb" >/dev/null
kicad-cli pcb export drill --format excellon --excellon-units mm --excellon-zeros-format decimal --excellon-separate-th -o "$O/" "$T/Madromys.kicad_pcb" >/dev/null
cd "$O"; for f in *\ *; do [ -e "$f" ] && mv "$f" "${f// /_}"; done; rm -f Madromys-job.gbrjob; rm -rf "$T"
