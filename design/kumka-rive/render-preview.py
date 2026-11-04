import pathlib,subprocess,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
p=pathlib.Path(__file__).resolve().parent;(p/'build/frames').mkdir(exist_ok=True)
original=(p/'scene.rml').read_text()
try:
 for mode,state in [('idle','0:12'),('wave','0:30'),('success','0:31'),('encourage','0:32')]:
  r=ET.fromstring(original);r.find('.//EntryState/StateTransition').set('stateToId',state)
  (p/'scene.rml').write_text(ET.tostring(r,encoding='unicode'))
  for i in range(12):
   subprocess.run(['./rive-tools/bin/rive',str(p),f'--screenshot={p}/build/frames/{mode}-{i:02}.png',f'--advance={1+i*8}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
finally:
 (p/'scene.rml').write_text(original)
subprocess.run(['./rive-tools/bin/rive',str(p),'--once'],check=True)
frames=[]
for i in range(12):
 canvas=Image.new('RGB',(1000,380),'#fffafc');d=ImageDraw.Draw(canvas)
 for j,(mode,label) in enumerate([('idle','Spoczynek'),('wave','Machanie'),('success','Podskok'),('encourage','Zacheta')]):
  im=Image.open(p/f'build/frames/{mode}-{i:02}.png').convert('RGB').resize((250,250));canvas.paste(im,(j*250,80));d.text((j*250+90,40),label,fill='#493144')
 frames.append(canvas)
frames[0].save(p/'build/kumka-preview.gif',save_all=True,append_images=frames[1:],duration=133,loop=0)
