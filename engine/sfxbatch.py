"""Generate a batch of ElevenLabs sound effects, max 3 concurrent (plan limit). Skips files that already exist.
  python3 engine/sfxbatch.py batch.json      # [[out_path, seconds, prompt, loop?], ...]"""
import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))


def one(item):
    out, sec, prompt = item[:3]
    if os.path.exists(out): return f'skip {out}'
    cmd = [sys.executable, os.path.join(HERE, 'tts.py'), 'sfx', out, str(sec), prompt] + (['loop'] if len(item) > 3 and item[3] else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip().splitlines()[-1]


if __name__ == '__main__':
    items = json.load(open(sys.argv[1]))
    with ThreadPoolExecutor(3) as ex:
        for line in ex.map(one, items): print(line)
