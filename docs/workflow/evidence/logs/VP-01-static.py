from pathlib import Path
import ast, hashlib, json, re, subprocess
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[4]
def old(p):return subprocess.check_output(['git','show','ac59d8c27ed47be07ac9b54acf8285bcab704be0:'+p],cwd=root).decode('utf-8')
def current(p):return (root/p).read_text(encoding='utf-8')
paths=['frontend/index.html','frontend/splash.html','app/desktop_launcher.py','tests/test_desktop_launcher.py']
result={'baseline':'ac59d8c27ed47be07ac9b54acf8285bcab704be0','sha256':{},'checks':{}}
for p in paths+list(str(p.relative_to(root)).replace('\\','/') for p in (root/'frontend/assets').glob('*')):
 result['sha256'][p]=hashlib.sha256((root/p).read_bytes()).hexdigest()
before=old('frontend/index.html');after=current('frontend/index.html')
assert re.findall(r'<script>(.*?)</script>',before,re.S)==re.findall(r'<script>(.*?)</script>',after,re.S)
result['checks']['index_javascript_identical_to_baseline']=True
class Form(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ('input','select','button','label','option','form'):self.nodes.append((tag,a))
a=Form();b=Form();a.feed(before);b.feed(after);assert a.nodes==b.nodes
result['checks']['form_nodes_attributes_order_identical']=True
def neutral_ast(s):
 t=ast.parse(s)
 t.body=[n for n in t.body if not(isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id in ('SPLASH_WIDTH','SPLASH_HEIGHT','SPLASH_BACKGROUND') for x in n.targets))]
 return ast.dump(t)
assert neutral_ast(old('app/desktop_launcher.py'))==neutral_ast(current('app/desktop_launcher.py'))
result['checks']['launcher_only_three_splash_constants_changed']=True
for p in ['app/main.py','app/calculator.py','app/gsv_calculator.py']:
 assert old(p)==current(p);result['checks'][p+'_zero_diff']=True
resources=[]
for p in [root/'frontend/index.html',root/'frontend/splash.html',*(root/'frontend/assets').glob('*.svg')]:
 s=p.read_text(encoding='utf-8')
 urls=re.findall(r'https?://[^\s"\)<>]+',s)
 assert all(u=='http://www.w3.org/2000/svg' for u in urls),(p,urls)
 assert '@import' not in s
 resources.append({'file':str(p.relative_to(root)),'external_urls_except_svg_namespace':[]})
result['checks']['static_network_scan']=resources
result['checks']['emblem_preserved']=hashlib.sha256((root/'frontend/assets/company-emblem.png').read_bytes()).hexdigest()
result['checks']['git_diff_check_product_exit']=subprocess.run(['git','diff','--check','--',*paths,'frontend/assets'],cwd=root).returncode
assert result['checks']['git_diff_check_product_exit']==0
print(json.dumps(result,ensure_ascii=False,indent=2))
