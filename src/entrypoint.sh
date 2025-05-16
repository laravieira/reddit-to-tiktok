#!/bin/sh
mkdir -p assets/inputs assets/output

echo "Downloading input files..."
python3 input-download.py

echo "Generating thumbnail..."
python3 thumbnail-generator.py

echo "Generating video..."
python3 video-generator.py

echo "Uploading output files..."
python3 output-upload.py

echo "Publishing video on TikTok..."
python3 output-publish.py

echo "Cleaning up..."
rm -rf assets/inputs assets/output

echo "Process completed."