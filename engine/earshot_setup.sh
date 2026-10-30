#!/usr/bin/env bash
# earshot (github.com/Leonxlnx/earshot, MIT): «ears for coding agents» — listening (CLAP + AST on CPU), measured QA of a film's sound,
# and a bank of 252 sound effects made in code. Installs into EARSHOT_DIR (default /home/user/tools/earshot, outside the repo; the
# container is ephemeral, so run this once per session that needs it). ~1.1 GB models + ~1 GB torch CPU.
set -euo pipefail
D=${EARSHOT_DIR:-/home/user/tools/earshot}
PIN=591fa3e028032e6dce56620a20e932e35667e8d8          # the commit tested 30.10.2026 (v0.4.0)
if [ ! -d "$D/.git" ]; then git clone -q https://github.com/Leonxlnx/earshot "$D"; fi
git -C "$D" fetch -q --depth 1 origin "$PIN" 2>/dev/null || true
git -C "$D" checkout -q "$PIN" 2>/dev/null || echo "note: could not pin $PIN, using the cloned HEAD"
[ -x "$D/.venv/bin/python" ] || python3 -m venv "$D/.venv"
"$D/.venv/bin/python" -m pip install -q torch --index-url https://download.pytorch.org/whl/cpu
"$D/.venv/bin/python" -m pip install -q -e "$D"
"$D/.venv/bin/python" -m earshot doctor --fetch | tail -3
echo "earshot ready: $D/.venv/bin/python -m earshot ..."
