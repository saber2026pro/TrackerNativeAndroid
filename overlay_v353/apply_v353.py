from pathlib import Path
import sys
root=Path(sys.argv[1])
html=root/'app/src/main/assets/index.html'
gradle=root/'app/build.gradle.kts'
s=html.read_text(encoding='utf-8')
s=s.replace('state.audit=state.audit.slice(0,5000);','state.audit=state.audit.slice(0,20000);')
append=Path(__file__).with_name('v353_append.js').read_text(encoding='utf-8')
if 'V353_VERSION' not in s:
    idx=s.rfind('</script>')
    if idx<0: raise SystemExit('script close not found')
    s=s[:idx]+append+'\n'+s[idx:]
html.write_text(s,encoding='utf-8')
g=gradle.read_text(encoding='utf-8')
g=g.replace('versionCode = 352','versionCode = 353').replace('versionName = "3.5.2-stable"','versionName = "3.5.3-stable"')
gradle.write_text(g,encoding='utf-8')
