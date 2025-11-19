#!/usr/bin/env bash
set -euo pipefail

# Expects env var DATA_URL (direct link to the CSV zip or CSV file)
if [ -z "${DATA_URL:https:https://drive.google.com/file/d/1AOgG9QTXUu1IQ45OGMeSvRa5TgUVDJ-H/view?usp=drive_link" ]; then
  echo "ERROR: DATA_URL not set. Set repo secret DATA_URL to a direct download link."
  exit 2
fi

mkdir -p data

# If the link is a zip: try to curl then unzip, else save as csv
echo "Downloading dataset..."
curl -L --fail -o data/dataset_download "$DATA_URL"

# If it's a zip, unzip. If it's a csv, rename accordingly
file data/dataset_download | grep -qi zip && {
  echo "Detected zip archive — extracting..."
  unzip -q data/dataset_download -d data/
  rm data/dataset_download
} || {
  # Not a zip; try detect CSV by first bytes; assume direct CSV — ensure semicolon delimiter
  mv data/dataset_download data/UNSW_2018_IoT_Botnet_Final_10_B.csv || true
}

echo "Download step finished. Files in data/:"
ls -lah data || true
