#!/usr/bin/env bash
# One-command setup for Vibe Code Studio.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
PLUG="$DIR/plugins/vibe-editing"
echo "== Vibe Code Studio setup =="
if command -v brew >/dev/null 2>&1; then
  echo "Installing system tools via Homebrew (ffmpeg, tesseract, yt-dlp, rclone)..."
  brew install ffmpeg tesseract yt-dlp rclone || true
else
  echo "!! Homebrew not found. Install it (https://brew.sh) then re-run, or install"
  echo "   ffmpeg + tesseract + yt-dlp yourself. (Linux: use your package manager.)"
fi
echo "Setting up Python environment..."
cd "$PLUG"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo ""
echo "Running health checks..."
python3 "$PLUG/doctor.py" || true
cd "$DIR"
"$PLUG/.venv/bin/python" skills/thumbnail/scripts/thumb.py selftest --outdir sample/out || \
  echo "!! Thumbnail selftest failed - re-run after fixing the error above."
echo ""
echo "Next steps:"
echo "  1) Open this repo in Claude Code and say: Set up Vibe Code Studio for me"
echo "  2) The agent follows ONBOARDING.md: keys (local only), your brand preset,"
echo "     then a full sample run before you trust it with real footage."
