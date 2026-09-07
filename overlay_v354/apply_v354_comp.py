from pathlib import Path
import base64, gzip, subprocess, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: apply_v354_comp.py PROJECT_DIR')
root = Path(sys.argv[1]).resolve()
overlay = Path(__file__).resolve().parent

def unpack_text(name: str) -> str:
    raw = base64.b64decode((overlay / name).read_text(encoding='ascii'))
    return gzip.decompress(raw).decode('utf-8')

native = unpack_text('native.patch.gz.b64')
native_file = overlay / '_native_v354.patch'
native_file.write_text(native, encoding='utf-8')
subprocess.run(['patch', '-p1', '--forward', '--batch', '-d', str(root), '-i', str(native_file)], check=True)

html = root / 'app/src/main/assets/index.html'
h = html.read_text(encoding='utf-8')
if 'V354_VERSION' in h:
    raise SystemExit('v3.5.4 patch already present')
marker = '/* ===== end v3.5.3 ===== */'
if marker not in h:
    raise SystemExit('v3.5.3 marker not found')
js = unpack_text('patch.js.gz.b64').rstrip() + '\n'
h = h.replace(marker, js + marker, 1)
html.write_text(h, encoding='utf-8')
print('Applied TrackerClassic 3.5.4 acceptance patch')
