#!/usr/bin/env bash
# Makes a tiny synthetic sample clip so you can test the whole kit before
# trusting it with your own footage. Generated locally by ffmpeg - nothing
# downloaded, nothing copyrighted, safe to keep or delete.
set -e
cd "$(dirname "$0")"
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ERROR: ffmpeg not found. macOS: brew install ffmpeg  |  Ubuntu: sudo apt install ffmpeg"
  exit 1
fi
ffmpeg -y -loglevel error \
  -f lavfi -i "testsrc2=size=1080x1920:rate=30:duration=8" \
  -f lavfi -i "sine=frequency=440:duration=8" \
  -vf "drawtext=text='SAMPLE TAKE':fontcolor=white:fontsize=90:x=(w-text_w)/2:y=(h-text_h)/2" \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest sample-clip.mp4
echo "WROTE $(pwd)/sample-clip.mp4 (8s synthetic test clip)"
