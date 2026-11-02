# Thumbnail & cover builder

Make platform-ready covers from a photo or a video frame, in any brand.

## When to use

The user wants a YouTube thumbnail, or a vertical cover for TikTok /
Instagram Reels / YouTube Shorts.

## Inputs

- An image: a photo of the person (best), or pull a frame first:
  `python3 scripts/thumb.py frame --video take.mp4 --time 4.0 --out frame.png`
- A headline: 3-6 words, all caps reads best. Pick ONE word to accent.
- A brand preset: `brand/presets/default.json` to start; copy it to make
  their own (colors, font). `brand/presets/vibe-code-ceo.json` is a worked
  example.

## Command

```bash
python3 scripts/thumb.py make \
  --image face.png \
  --headline "CLAUDE EDITS MY VIDEOS" \
  --accent EDITS \
  --preset ../../brand/presets/default.json \
  --outdir covers/
```

Outputs `covers/thumb-youtube.png` (1280x720) and
`covers/thumb-vertical.png` (1080x1920).

## Rules

- Show the rendered covers to the user and get a "looks right" before they
  post. Iterate on headline/accent/preset, not on manual pixel edits.
- Background removal is optional: `--cutout` uses the open-source `rembg`
  package (`pip install rembg`). If the photo already has transparency,
  skip it.
- Inputs are read-only. Never overwrite the user's photos or footage.
- Headline legibility beats cleverness: if the tool warns the headline is
  too long, shorten it.
