from pathlib import Path
import subprocess, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: apply_v354.py PROJECT_DIR')
root = Path(sys.argv[1]).resolve()
overlay = Path(__file__).resolve().parent

def join_parts(prefix: str) -> str:
    parts = sorted(overlay.glob(prefix + '.part*'))
    if not parts:
        raise SystemExit(f'no chunks for {prefix}')
    return ''.join(p.read_text(encoding='utf-8') for p in parts)

native = join_parts('native.patch')
native_file = overlay / '_native_joined.patch'
native_file.write_text(native, encoding='utf-8')
subprocess.run(['patch', '-p1', '--forward', '--batch', '-d', str(root), '-i', str(native_file)], check=True)

html = root / 'app/src/main/assets/index.html'
h = html.read_text(encoding='utf-8')
if 'V354_VERSION' in h:
    raise SystemExit('v3.5.4 patch already present')
marker = '/* ===== end v3.5.3 ===== */'
if marker not in h:
    raise SystemExit('v3.5.3 marker not found')
js = join_parts('patch.js').rstrip() + '\n'
h = h.replace(marker, js + marker, 1)
html.write_text(h, encoding='utf-8')
print('Applied TrackerClassic 3.5.4 acceptance patch')
