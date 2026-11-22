#!/usr/bin/env bash
set -euo pipefail

quality="${1:-preview}"
if [[ "$quality" == "preview" ]]; then
  export MANIMGL_RENDER_OPTIONS="-w -r 854x480 --fps 15"
else
  export MANIMGL_RENDER_OPTIONS="-w -r 1920x1080 --fps 60"
fi

scenes=(
  "scenes_basics.py A1CompressionPrediction" "scenes_basics.py A2CrossEntropyWaste"
  "scenes_basics.py A3NCDMechanism" "scenes_basics.py A4GzipWindow"
  "scenes_data.py B1NCDHeatmap" "scenes_data.py B2GrowingDendrogram"
  "scenes_data.py B3WordsCarryBits" "scenes_data.py B4LossVsData"
  "scenes_data.py B5ClassifyingAbstract" "scenes_data.py B6KLAsymmetry"
  "scenes_3d.py C1KnowledgeMap3D" "scenes_3d.py C2ArticlesCloud3D"
  "scenes_3d.py C3CrossEntropyLandscape"
)

for item in "${scenes[@]}"; do
  read -r file scene <<< "$item"
  manimgl "animations/$file" "$scene" $MANIMGL_RENDER_OPTIONS --config_file animations/custom_config.yml
  manimgl "animations/$file" "$scene" -sw --config_file animations/custom_config.yml
done
