"""Repo-relative paths for all render scripts (replaces the old /home/claude/px/... chat paths).

Episode scripts live in series/<slug>/episodes/epNN/ and do:
    import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
    import paths as P
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / 'engine'
FONT_PX = str(ENGINE / 'fonts' / 'PressStart.ttf')               # Press Start 2P (Cyrillic)
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'  # captions (apt: fonts-dejavu-core)
LIB_SFX = ROOT / 'library' / 'sfx'
BUILD = ROOT / 'build'                                            # gitignored: segments, wav cache, test sheets
PDZ = 'pochti-dikiy-zapad'


def series(slug=PDZ):
    return ROOT / 'series' / slug


def episode(ep, slug=PDZ):
    return series(slug) / 'episodes' / ep


def build(*parts):
    """Path inside build/ (parent dirs created)."""
    p = BUILD.joinpath(*parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)


def voice_wav(ep, key, slug=PDZ):
    """Mono 16-bit wav of series/<slug>/voice/<ep>/<key>.mp3, cached in build/ (for lip-flap envelopes)."""
    src = series(slug) / 'voice' / ep / f'{key}.mp3'
    dst = Path(build('cache', slug, ep, f'{key}.wav'))
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-ac', '1', '-c:a', 'pcm_s16le', str(dst)], check=True)
    return str(dst)
