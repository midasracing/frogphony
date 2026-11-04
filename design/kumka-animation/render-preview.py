"""Render the actual state-machine triggers with official Rive CLI.

Isolated worker projects avoid shared build output. PNGs are decoded before
accepting a capture, with retries for an interrupted GPU readback.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageFont
import os, subprocess, tempfile, threading, shutil, json

HERE=Path(__file__).resolve().parent
WORKSPACE=next(p for p in HERE.parents if (p/'rive-tools/bin/rive').exists())
CLI=WORKSPACE/'rive-tools/bin/rive'
os.environ['LD_LIBRARY_PATH']=str(WORKSPACE/'rive-tools/libs/usr/lib/x86_64-linux-gnu')
os.environ['RIVE_DOCS_DIR']=str(WORKSPACE/'rive-tools/versions/1.8.0/docs')
BUILD=HERE/'build';BUILD.mkdir(exist_ok=True)
FRAMES=BUILD/'frames';FRAMES.mkdir(exist_ok=True)
workers=threading.local()
temps=[]
def project():
    if not hasattr(workers,'project'):
        p=Path(tempfile.mkdtemp(prefix='render-',dir=BUILD));temps.append(p)
        import xml.etree.ElementTree as ET
        tree=ET.parse(HERE/'scene.rml');art=tree.getroot().find('Artboard')
        bg=ET.SubElement(art,'Shape',name='Preview background',x='362',y='322')
        ET.SubElement(bg,'Rectangle',width='724',height='644')
        fill=ET.SubElement(bg,'Fill');ET.SubElement(fill,'SolidColor',colorValue='FFFFF7FB')
        tree.write(p/'scene.rml',encoding='utf-8')
        (p/'rive.yaml').write_text('name: kumka-render\n')
        workers.project=p
    return workers.project

def capture(mode,index,advance):
    output=FRAMES/f'{mode}-{index:03}.png'
    command=[str(CLI),str(project()),f'--screenshot={output}','--quiet']
    if mode=='idle':command += [f'--advance={max(1,advance)}']
    else:command += ['--advance=1',f'--data={mode}=1',f'--advance={max(1,advance)}']
    for attempt in range(3):
        result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        try:
            if result.returncode:raise RuntimeError(result.stdout[-2000:])
            with Image.open(output) as im:im.load()
            return mode,index
        except Exception:
            if attempt==2:raise

def compose():
    labels=[('blink','Mruganie'),('look','Spojrzenia'),('wave','Machanie'),('success','Radość')]
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
    frames=[]
    for i in range(60):
        canvas=Image.new('RGB',(800,800),'#fff7fb');d=ImageDraw.Draw(canvas)
        for j,(mode,label) in enumerate(labels):
            x=(j%2)*400;y=(j//2)*400
            with Image.open(FRAMES/f'{mode}-{i:03}.png') as im:
                canvas.paste(im.convert('RGB').resize((400,356),Image.Resampling.LANCZOS),(x,y+35))
            d.text((x+20,y+12),label,font=font,fill='#60344d')
        canvas.save(BUILD/f'montage-{i:03}.png')
        frames.append(canvas)
    frames[0].save(HERE/'kumka-animations.gif',format='GIF',save_all=True,append_images=frames[1:],duration=50,loop=0)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','20','-i',str(BUILD/'montage-%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',str(HERE/'kumka-animations.mp4')],check=True)

if __name__=='__main__':
    try:
        jobs=[(mode,i,i*3) for mode in ['blink','look','wave','success'] for i in range(60)]
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures=[pool.submit(capture,*args) for args in jobs]
            for n,f in enumerate(as_completed(futures),1):
                f.result()
                if n%40==0:print(f'Rendered {n}/{len(jobs)} native frames',flush=True)
        # Recheck after the batch too: an interrupted native output must not
        # reach the delivered preview. Repair only failed captures.
        for mode,i,advance in jobs:
            try:
                with Image.open(FRAMES/f'{mode}-{i:03}.png') as im:im.load()
            except Exception:capture(mode,i,advance)
        compose()
        # Verify that each triggered animation changes the actual rendered output.
        results={}
        for mode in ['blink','look','wave','success']:
            hashes={ (FRAMES/f'{mode}-{i:03}.png').read_bytes() for i in range(60) }
            results[mode]={'distinctFrames':len(hashes),'samples':60}
            assert len(hashes)>5, f'{mode} did not move'
        (HERE/'render-verification.json').write_text(json.dumps(results,indent=2)+'\n')
        print('Preview and motion checks complete',flush=True)
    finally:
        for p in temps:shutil.rmtree(p,ignore_errors=True)
