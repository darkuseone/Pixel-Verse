"""Re-encode a final.mp4 that is too big for chat upload (limit 30 MB): keeps audio, raises CRF until it fits.
  python3 engine/shrink.py path/to/final.mp4 [max_mb=28]      (rain/noise scenes at CRF 20 can reach 40 MB)"""
import os, shutil, subprocess, sys

def shrink(path, max_mb=28.0):
    if os.path.getsize(path) / 1e6 <= max_mb: return path
    src = path + '.crf20.mp4'; shutil.copy(path, src)
    for crf in (22, 23, 24, 26, 28):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-pix_fmt', 'yuv420p',
                        '-c:a', 'copy', '-movflags', '+faststart', path], check=True)
        mb = os.path.getsize(path) / 1e6
        print(f'crf {crf}: {mb:.1f} MB')
        if mb <= max_mb: break
    os.remove(src)
    return path

if __name__ == '__main__':
    shrink(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 28.0)
