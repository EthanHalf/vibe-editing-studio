# Sound for talking-head clips

How this kit approaches music and sound effects. The short version: the
voice is the product. Everything else is optional seasoning.

## The default direction

- **Voice first.** Clean, present speech beats any soundtrack. Remove
  background noise (chair squeaks, hum) when the pipeline flags it.
- **Music is opt-in.** No music under talking-head content unless the
  creator asks for it. When they do ask, the proven direction is a
  **quiet, rhythmic bed with forward momentum** - not a sleepy ambient
  pad, and never loud enough to compete with the voice.
- **No arbitrary stingers.** Don't bolt a startup beep or logo sting onto
  the opening unless the creator asks for one. The hook is the first
  spoken word; get to it fast.
- **SFX are sparse and motivated.** A pop or whoosh earns its place only
  when a visual moment motivates it - a graphic landing, a cross-out, a
  transition. If you can't point at the on-screen moment it serves, cut it.

## Adding a bed

1. Drop royalty-free tracks into `brand/music/` (or point `VIBE_MUSIC` at
   your folder).
2. Pick a track with a steady rhythmic pulse. Avoid slow ambient pads for
   talking-head energy.
3. Duck it under the voice. ffmpeg starting points - carve space for
   speech, then sidechain so the bed dips when they talk - are in
   `plugins/vibe-editing/skills/edit/references/audio_music_presets.md`.

## Pacing edits that make sound work

- The first word lands almost immediately: target under ~0.2s of leading
  quiet. Hook videos speak on frame one.
- Tighten long pauses - anything over roughly half a second reads as a
  mistake, not a beat.
- Cut stutters and false starts.

## The hearing gap (read this before shipping audio)

Coding agents can't hear. Waveforms, loudness stats and transcripts are
hypotheses, not listening:

- ASR transcription can silently skip segments, so never use a transcript
  alone to declare audio gap-free. Cross-check with silence/envelope
  detection and compare timing against the source clip.
- The `audit-audio` skill's signal checks catch clipped words, splice
  clicks and level problems - but they don't prove the mix sounds good.
- The final gate is a real listen: play the export yourself, or use a
  hearing tool. Don't ship sound nobody has heard.

Optional companion: [earshot](https://github.com/Leonxlnx/earshot) is a
free, open-source tool that gives coding agents audio review ("ears").
It's a third-party project - review it before installing, and treat its
output as a check, not a verdict.
