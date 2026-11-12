"""Evidence-only assertions against the existing installer and installed payload."""
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path
from PIL import Image

root = Path.cwd()
installed = Path('C:/Users/user/AppData/Local/Temp/opencode/vp-02-isolated/install')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
out = {'cwd': str(root), 'checks': [], 'payload': [], 'assets': []}
def check(name, condition):
    assert condition, name
    out['checks'].append(name)

iss = (root/'installer/GasProjectCalculator.iss').read_text(encoding='utf-8-sig')
old_iss = subprocess.check_output(['git','show','HEAD:installer/GasProjectCalculator.iss']).decode('utf-8')
appid = lambda s: re.search(r'^AppId=(.+)$', s, re.M).group(1)
check('AppId preserved', appid(iss) == appid(old_iss))
check('version 1.2.0 and 1.2.0.0', '#define AppVersion "1.2.0"' in iss and 'VersionInfoVersion=1.2.0.0' in iss)
check('RU-only', re.findall(r'^Name: "([^"]+)"; MessagesFile:',iss,re.M)==['russian'] and 'ShowLanguageDialog=no' in iss)
check('per user and no shutdown of foreign apps', 'PrivilegesRequired=lowest' in iss and 'CloseApplications=no' in iss)
check('no uninstall-delete section', not re.search(r'^\[UninstallDelete\]',iss,re.M))
check('no network/signing script directive', not re.search(r'^(?:SignTool|#expr.*Download|Source:.*https?://)',iss,re.M|re.I))
build = (root/'installer/build-installer.ps1').read_text(encoding='utf-8-sig')
check('version-specific artifact guard', 'Refusing to overwrite existing installer' in build and 'Get-Item -LiteralPath $artifactPath' in build)
for name in ['sidebar','header']:
    bmp=root/f'installer/assets/wizard-{name}.bmp'
    png=root/f'frontend/assets/installer-{name}.png'
    with Image.open(bmp) as b, Image.open(png) as p:
        check(f'{name} BMP matches accepted PNG', b.convert('RGB').tobytes()==p.convert('RGB').tobytes() and b.size==p.size)
        out['assets'].append({'path':str(bmp),'size':b.size,'mode':b.mode,'sha256':sha(bmp)})
check('frontend zero diff',subprocess.check_output(['git','diff','HEAD','--','frontend','app','requirements.txt'])==b'')
for source in sorted((root/'dist/GasProjectCalculator').rglob('*')):
    if source.is_file():
        rel=source.relative_to(root/'dist/GasProjectCalculator')
        target=installed/rel
        check(f'installed payload matches dist: {rel}',target.is_file() and sha(target)==sha(source))
        out['payload'].append({'relative':str(rel),'sha256':sha(target),'bytes':target.stat().st_size})
for source in sorted((root/'frontend').rglob('*')):
    if source.is_file():
        target=installed/'_internal'/source.relative_to(root)
        check(f'installed frontend matches accepted source: {source.name}',target.is_file() and sha(target)==sha(source))
exe=installed/'GasProjectCalculator.exe'
raw=exe.read_bytes()
offset=struct.unpack_from('<I',raw,0x3c)[0]
check('windowed PE subsystem (no CLI console)',struct.unpack_from('<H',raw,offset+0x5c)[0]==2)
check('bundled Python runtime', bool(list((installed/'_internal').glob('python3*.dll'))))
old=json.loads((root/'docs/workflow/evidence/logs/VP-02-old-artifacts-before.json').read_text(encoding='utf-8-sig'))
out['old_artifact_baseline']=old
for artifact in old:
    path=Path(artifact.get('path') or artifact.get('Path'))
    check(f'old artifact unchanged: {path.name}',sha(path)==(artifact.get('sha256') or artifact.get('SHA256')))
out['check_count']=len(out['checks'])
(root/'docs/workflow/evidence/logs/VP-02-resumed-static.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks':out['check_count'],'payload_files':len(out['payload']),'assets':out['assets']},ensure_ascii=False,indent=2))
