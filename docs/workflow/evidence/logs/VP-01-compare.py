"""Compose real reference/native captures, preserving each image's aspect ratio."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[4]
S=ROOT/'docs/screenshots'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
native=Image.open(S/'visual-01-native-target-gsv.png').convert('RGB')
pairs=[
 ('header',Image.open(ROOT/'docs/design/header-detail-reference.jpg'),native.crop((8,31,792,114))),
 ('footer',Image.open(ROOT/'docs/design/footer-detail-reference.jpg'),native.crop((8,469,792,532))),
 ('splash',Image.open(ROOT/'docs/design/splash-installer-reference.jpg'),Image.open(S/'visual-01-native-splash.png')),
]
for name,ref,actual in pairs:
 width=784 if name!='splash' else 560
 images=[im.convert('RGB').resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS) for im in [ref,actual]]
 height=max(im.height for im in images)
 board=Image.new('RGB',(width*2+48,height+62),'#eaf0f4');draw=ImageDraw.Draw(board)
 for i,(im,label) in enumerate(zip(images,['Reference (user image)','Implementation (real native capture)'])):
  x=16+i*(width+16);draw.text((x,12),label,font=font,fill='#123545');board.paste(im,(x,45+(height-im.height)//2))
 board.save(S/f'visual-01-compare-{name}.png')
 print(name,'source crop',actual.size,'comparison',board.size)
