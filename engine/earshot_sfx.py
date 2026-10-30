"""Render sounds from the earshot bank (code-made, no models, no network) into a series' own sfx folder, audited.
  python3 engine/earshot_sfx.py batch.json      # [[out_path, "bank/id", {"dur":..,"apex":..,"pitch":..,"seed":..,"peak":..}], ...]
Skips files that exist. Every render passes earshot's model-free audit (clicks, cut tails, clipping, ring); a warned take is
re-rolled on the next seeds, the audit verdict is printed. earshot lives in EARSHOT_DIR (default /home/user/tools/earshot,
setup: engine/earshot_setup.sh)."""
import json, os, subprocess, sys

ES = os.environ.get('EARSHOT_DIR', '/home/user/tools/earshot')
PY = os.path.join(ES, '.venv', 'bin', 'python')


def render(out, sid, opt):
    out = os.path.abspath(out)                                            # earshot runs with cwd=ES
    if os.path.exists(out): return f'skip {out}'
    seeds = [opt.get('seed')] + [s for s in range(1, 6) if s != opt.get('seed')]
    for seed in seeds:
        cmd = [PY, '-m', 'earshot', 'sfx', 'render', sid, '-o', out, '--json']
        for k in ('dur', 'apex', 'pitch', 'peak'):
            if k in opt: cmd += [f'--{k}', str(opt[k])]
        if seed is not None: cmd += ['--seed', str(seed)]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ES)
        if r.returncode: return f'FAIL {sid}: {r.stderr.strip()[:200]}'
        try: j = json.loads(r.stdout)
        except ValueError: j = {}
        warn = (j.get('audit') or {}).get('warnings') or j.get('warnings') or []
        if not warn: return f'ok {out} ({sid}, seed {seed})'
    return f'WARN {out} ({sid}): {warn}'


if __name__ == '__main__':
    for out, sid, opt in json.load(open(sys.argv[1])):
        print(render(out, sid, opt))
