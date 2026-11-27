# WASHEEJ — The Invisible Order (9:16 commercial)

- `docs/FREE_GENERATION_KIT.md`: copy-paste kit for free tools (16 generations, day plan, file naming).
- `docs/PRODUCTION_BIBLE.md`: storyboard, VO-synced timeline, Higgsfield prompts per shot, start/end frames, assets, sound, workflow, QA.
- `timeline.json`: single source of truth for the edit (shots, VO cues, music automation, SFX).
- `brand/`: authentic logo SVGs, fonts and imagery extracted from washeej.site.
- `gfx/`: source HTML for every graphics element (deterministic, `window.seek(t)`).
- `renders/`: rendered graphics (ProRes 4444 alpha / 422 HQ), `renders/preview/` H.264 previews.
- `shots/`: put generated shots here as `<ID>.mp4` (or `<ID>_comp.mp4` after screen replacement).
- `audio/`: `vo.wav` (or `vo/V1.wav…`), `music.wav`, `sfx/*.wav` (names in timeline.json).

```
python3 tools/assemble.py --check
python3 tools/assemble.py
tools/qa.sh renders/WASHEEJ_InvisibleOrder_9x16_1080x1920_30fps.mp4
tools/render_all.sh      # re-render graphics after editing gfx/*.html
```
- `tools/screen_replace.py`: track a screen and insert a GFX plate (KLT + reference homography; verified ~1px error on a synthetic test).
- `tools/stitch_s06.py`: joins S06A/B/C into the 13.2s one-take `shots/S06.mp4`.
