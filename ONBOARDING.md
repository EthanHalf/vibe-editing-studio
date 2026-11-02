# Guided onboarding (for your Claude Code agent)

Read this whole file, then set the kit up with the user. Work in order.
Ask before installing anything, before spending anything, and before
touching files outside this repo. Keep all secrets local - never commit
keys, never upload them.

## 1. Health check

Run `python3 plugins/vibe-editing/doctor.py`. Report what is missing in
plain words and offer the exact install command for each missing piece
(`./setup.sh` handles ffmpeg and Python dependencies on macOS via Homebrew).

## 2. Keys (local only)

Ask which transcription path they want:

- **AssemblyAI** (default, paid pay-as-you-go): they paste their key; save
  it with `python3 plugins/vibe-editing/onboard.py set ASSEMBLYAI_API_KEY`.
  Tell them this costs money per minute of audio.
- **Local fallback** (free, slower): no key needed; uses faster-whisper
  already in requirements.

Never print a key back. Never write keys anywhere except the kit's private
config. Keys must never appear in git.

## 3. Brand preset

Ask four questions: brand name, headline color, accent color, and whether
they have a preferred font. Then create `brand/presets/<their-name>.json`
by copying `brand/presets/default.json` and changing those values. Show
them the file. `brand/presets/vibe-code-ceo.json` is a finished example.

## 4. Prove it on the sample

1. `bash sample/make_sample.sh` - generates a synthetic test clip.
2. `python3 skills/thumbnail/scripts/thumb.py selftest --preset brand/presets/<their-name>.json`
   - renders test covers; open them and confirm the sizes report OK.
3. Ask them to look at both covers. Only move on when they say the look is
   right (adjust the preset if not).

## 5. First real job

Ask for one short vertical talking-head take (phone footage is fine).
Run the edit pipeline per `plugins/vibe-editing/docs/ONBOARDING.md`, then
make its cover with the thumbnail builder. Preview everything before they
post. Their original footage is never modified.

## Rules that always apply

- Originals are read-only; outputs go to a folder the user picks.
- If a step fails, say what failed and the single next command to fix it.
- Only claim support for setups you have actually tested on this machine.
