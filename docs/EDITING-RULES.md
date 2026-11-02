# Editing rules and QA checklist

These are the kit's default quality bar for short-form talking-head clips.
They are defaults, not laws: tune them in your brand preset and in the
editing plugin's config as your own style develops.

## Caption and layout rules (defaults)

- Vertical 9:16 output, 1080x1920. Source footage at 1080p or better -
  never upscale 720p sources to fake it.
- Captions sit in the lower third of the frame and never cover the
  speaker's mouth. One caption chunk on screen at a time; keep chunks short.
- Headline/title text stays in the top safe area and never sits over the
  speaker's face.
- Keep clear of the bottom ~15% of vertical covers - app UI (caption,
  buttons) overlays that strip on TikTok, Reels and Shorts.
- Face stays centered and large; when reframing horizontal footage, track
  the face rather than cropping blindly.

## Audio

- Remove obvious background noise (chair squeaks, hum) when the pipeline
  flags it. No background music under talking-head content unless the
  creator asks for it.

## QA before anything ships

Run through this list on every clip and cover:

1. Watch the whole clip once, sound on. Cuts land on natural pauses, no
   clipped words, captions in sync with speech.
2. Captions spelled right, numbers read naturally, no word covering the
   face or mouth.
3. True vertical output (1080x1920) - no rotated or letterboxed exports.
4. Cover/thumbnail: headline readable at phone size, accent word correct,
   face visible, nothing important in the bottom 15% UI strip.
5. File names are clean and dated so posts are findable later.
6. Originals untouched in their source folder; exports in the output
   folder only.

If any check fails, fix and re-render before showing the result.

## Platform crop and overlay safety

- Vertical covers: the headline must survive a centered 1:1 crop (feed grids
  show only the middle square). The builder places it there automatically.
- Text never covers the speaker's eyes or mouth. Supporting text and design
  cards sit beside or below the face.
- Captions are natural phrase chunks beside/below the face - no caption
  background boxes and no progress bars by default. Both can be added per
  brand preset if a creator wants them.
- The kit's caption engine defaults to rapid word-by-word pops. For the
  phrase-chunk look, render with `brand/presets/captions-phrase.json`:

  `python3 plugins/vibe-editing/skills/caption-clips/scripts/generate_spice.py <spice_norm.json> --preset brand/presets/captions-phrase.json --style <director_stream.json> --out subs.ass --burn <clip.mp4> --burn-out <final.mp4>`

## Claims and sound

- If a video says a tool did something, show that literal screen recording -
  no stand-in footage for product claims.
- No background music under talking-head content by default.
