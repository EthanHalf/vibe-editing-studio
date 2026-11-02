# Vibe Code Studio - the guide

*Working name - not finalized.*

Vibe Code Studio is a private kit that turns raw talking-head footage into
captioned vertical clips, and makes the covers to go with them. It runs on
your own machine, inside Claude Code. This guide is for you, the person
using it. (A separate file, `ONBOARDING.md`, carries the step-by-step
instructions your coding assistant follows during setup.)

## Where it lives

Private repository: **https://github.com/EthanHalf/vibe-code-studio**

It is visible only to you. Clone it with your own GitHub login:

```bash
git clone https://github.com/EthanHalf/vibe-code-studio.git
cd vibe-code-studio
./setup.sh
```

Then open the folder in Claude Code and say: **Set up Vibe Code Studio for
me.** The assistant walks you through keys, brand, and a sample run.

## The two things it does

**1. Caption a clip - free and offline.** Uses local Whisper on your
machine; no account, no API key, nothing uploaded:

```bash
bin/caption-local take.mp4 take_captioned.mp4 --preset brand/presets/captions-phrase.json
```

**2. Make covers.** A photo or a frame from your video plus a headline
becomes a YouTube thumbnail (1280x720) and a vertical cover (1080x1920) in
your brand, with platform safe zones handled:

```bash
python3 skills/thumbnail/scripts/thumb.py make --image frame.png \
    --headline "CLAUDE EDITS MY VIDEOS" --accent EDITS \
    --preset brand/presets/vibe-code-ceo.json --outdir covers/
```

## What it costs, and where your data goes

The kit itself is free and open source (MIT). Honest picture of the rest:

- **Local captioning (the default above):** runs entirely on your machine.
  Your footage and audio are not uploaded anywhere. First run downloads the
  Whisper model (~460 MB) from a public model repository.
- **Cover background removal (`--cutout`):** also fully local; first run
  downloads the rembg model (~176 MB).
- **Claude Code:** the assistant that drives the kit processes your footage
  details, transcripts, and instructions under your own Claude plan and its
  terms - that is the one service that sees your content on the local path.
- **AssemblyAI (optional):** the upstream editor's default transcription
  service. If you choose it, your audio is uploaded to AssemblyAI and billed
  per minute on your own key. It is not required for the local path above.
- **Anything else the full editor connects** (Google Drive ingest, posting
  tools) is off until you connect it yourself during onboarding.

## What is tested, and what is not

Tested (on Linux, in this project's build environment):

- The offline caption chain above, end to end on a sample clip, including a
  caption-vs-audio sync check that passed with 0 mismatches.
- The cover builder, including background removal on a real photo, both
  brand presets, and both output sizes, with rendered results inspected.

Not yet tested:

- The full `/edit` workflow (silence cutting, face-tracking reframe, end
  card). It runs inside Claude Code on your machine and needs a first real
  run on your Mac before you rely on it.
- A clean install on a fresh Mac. Treat your first `./setup.sh` run as the
  real install test; the health check (`doctor.py`) will name anything
  missing and the exact command to fix it.

## Make it yours

Your brand is a preset file: colors, font, accent. Copy
`brand/presets/default.json`, change it, pass it with `--preset`. The
`vibe-code-ceo` preset (black, white, gold #FFD60A, Montserrat ExtraBold)
ships as a worked example.

## Credit

Built on the open-source Vibe Editing plugin (MIT) - see `NOTICE.md`.
Bundled fonts are SIL Open Font License. Originals are never modified: the
kit reads your footage and writes new files to an output folder you choose.
