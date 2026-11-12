import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image

root=Path.cwd()
logs=root/'docs/workflow/evidence/logs'
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest().upper()
pre=json.loads((logs/'VP-02-resumed-preflight.json').read_text(encoding='utf-8-sig'))
artifacts=[]
for item in pre['artifacts']:
    p=Path(item['path'])
    assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],p
    artifacts.append({**item,'postBytes':p.stat().st_size,'postSHA256':sha(p),'unchanged':True})
shots=[]
for p in sorted((root/'docs/screenshots').glob('visual-02-*.png')):
    with Image.open(p) as im:
        shots.append({'path':p.relative_to(root).as_posix(),'pixels':im.size,'format':im.format,'bytes':p.stat().st_size,'sha256':sha(p)})
cycle=Path('C:/Users/user/AppData/Local/Temp/opencode/vp-02-resume-cycle/backup')
registry={'before':sha(cycle/'uninstall.reg'),'after':sha(cycle/'restored.reg')}
assert registry['before']==registry['after']
before=json.loads((cycle/'user-install.json').read_text(encoding='utf-8-sig'))
for item in before:
    p=Path(item['path'])
    assert p.stat().st_size==item['size'] and sha(p)==item['sha256'],p
assert sum(p.is_file() for p in Path('C:/Users/user/AppData/Local/Programs/GasProjectCalculator').rglob('*'))==106
links=json.loads((cycle/'links.json').read_text(encoding='utf-8-sig'))
for item in links:
    if item['exists']:assert sha(Path(item['path']))==item['hash']
state=json.loads((logs/'VP-02-resumed-final-state.json').read_text(encoding='utf-8-sig'))
assert not state['isolatedProcesses'] and not state['testListeners']
product=subprocess.check_output(['git','diff','--name-only','HEAD','--','app','frontend','packaging','requirements.txt','tests']).decode().strip()
assert not product,product
owned=[p.relative_to(root).as_posix() for p in sorted(logs.glob('VP-02-resumed-*')) if p.is_file()]
owned += [p['path'] for p in shots if '/visual-02-resumed-' in p['path']]
owned += ['docs/workflow/evidence/VP-02-evidence.md']
out={'cwd':str(root),'baseline':pre['head'],'branch':pre['branch'],'artifacts':artifacts,'screenshots':shots,'registry':registry,'userFilesUnchanged':len(before),'shortcutHashes':links,'zeroDiff':['app/','frontend/','packaging/','requirements.txt','tests/'],'workerAddedFiles':owned}
(logs/'VP-02-resumed-manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'artifactsUnchanged':len(artifacts),'screenshots':len(shots),'userFilesUnchanged':len(before),'registryExact':True,'shortcutHashesExact':True,'productChangesThisResume':0,'ownedFiles':len(owned)},ensure_ascii=False,indent=2))
