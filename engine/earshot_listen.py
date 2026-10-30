"""Listen to a finished episode with earshot in one process (models load once): timeline with the episode's cue sheet (sync of
every sound to its picture event), the annotated sheet PNG and the critique scorecard. Run with earshot's venv python:
  /home/user/tools/earshot/.venv/bin/python engine/earshot_listen.py final.mp4 sound/cues.json build/<bk>/vN
-> vN_timeline.json, vN_sheet.png, vN_critique.json; the plain-text summaries go to stdout (~1 min for a 31 s short)."""
import sys, json
from earshot import timeline as TL, sheet as SH, critique as CR
v, cues, out = sys.argv[1], sys.argv[2], sys.argv[3]
tl = TL.timeline(v, cues=cues, detail='normal')
json.dump(tl, open(out + '_timeline.json', 'w'), indent=1, default=str)
print(TL.timeline_text(tl) if hasattr(TL, 'timeline_text') else tl['summary'])
SH.sheet(v, out + '_sheet.png', cues=cues, tl=tl)
cr = CR.critique(v)
json.dump(cr, open(out + '_critique.json', 'w'), indent=1, default=str)
print(CR.critique_text(cr))
