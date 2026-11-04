"""Preserve approved PNG byte-for-byte; animate its native Rive mesh."""
from pathlib import Path
from xml.etree.ElementTree import Element,SubElement,indent,tostring
import math,base64
r=Element('Rive',version='1',kind='fragment')
SubElement(r,'ImageAsset',file='kumka-original.png',name='Approved Kumka original',id='0:60')
a=SubElement(r,'Artboard',name='Kumka',id='0:2',width='500',height='500',defaultStateMachineId='0:7',styleId='0:5')
SubElement(a,'LayoutComponentStyle',id='0:5')
root=SubElement(a,'Node',name='Kumka',id='0:100',x='250',y='450',scaleX='0.30',scaleY='0.30')
im=SubElement(root,'Image',name='Original artwork mesh',id='0:101',assetId='0:60',originX='0.5',originY='1')
# Counter-clockwise boundary followed by interior grid vertices.
w,h=1448,1086;nx,ny=40,30
coords=[(x,0) for x in range(nx+1)]+[(nx,y) for y in range(1,ny+1)]+[(x,ny) for x in range(nx-1,-1,-1)]+[(0,y) for y in range(ny-1,0,-1)]+[(x,y) for y in range(1,ny) for x in range(1,nx)]
lookup={xy:i for i,xy in enumerate(coords)}
def vint(i):
 b=[]
 while i>127:b.append((i&127)|128);i>>=7
 return bytes(b+[i])
indices=[]
for y in range(ny):
 for x in range(nx):
  v0,v1,v2,v3=[lookup[p] for p in [(x,y),(x+1,y),(x+1,y+1),(x,y+1)]];indices.extend([v0,v1,v2,v0,v2,v3])
mesh=SubElement(im,'Mesh',name='Kumka deformable mesh',id='0:102',triangleIndexBytes=base64.b64encode(b''.join(vint(i) for i in indices)).decode())
verts=[]
for i,(gx,gy) in enumerate(coords):
 x,y=w*gx/nx,h*gy/ny
 v=SubElement(mesh,'ContourMeshVertex' if i<2*(nx+ny) else 'MeshVertex',name=f'v{i}',id=f'0:{1000+i}',x=str(x-w/2),y=str(y-h),u=str(x/w),v=str(y/h));verts.append((v,x,y))
def animation(name,id,duration,loop='oneShot'):return SubElement(a,'LinearAnimation',name=name,id=id,duration=str(duration),fps='60',loopValue=loop)
def key(anim,obj,prop,pairs):
 k=SubElement(anim,'KeyedObject',objectId=obj.attrib['id']);p=SubElement(k,'KeyedProperty',propertyKey=str(prop))
 for f,val in pairs:SubElement(p,'KeyFrameDouble',frame=str(f),value=str(val),interpolationType='linear')
idle=animation('Idle','0:6',240,'loop')
key(idle,root,17,[(0,.30),(60,.303),(120,.30),(180,.303),(240,.30)])
wave=animation('Wave','0:10',90)
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
for v,x,y in verts:
 weight=smooth(1080,1210,x)*(1-smooth(660,790,y))
 if weight>.001:
  pairsx=[];pairsy=[]
  for f,angle in [(0,0),(15,-.12),(28,.12),(41,-.12),(54,.12),(70,-.06),(90,0)]:
   angle*=weight;dx,dy=x-1120,y-680
   xx=1120+math.cos(angle)*dx-math.sin(angle)*dy;yy=680+math.sin(angle)*dx+math.cos(angle)*dy
   pairsx.append((f,xx-w/2));pairsy.append((f,yy-h))
  key(wave,v,24,pairsx);key(wave,v,25,pairsy)
success=animation('Success','0:11',75)
key(success,root,14,[(0,450),(9,455),(24,417),(40,450),(47,454),(60,450),(75,450)])
key(success,root,17,[(0,.30),(9,.292),(24,.306),(40,.30),(47,.295),(60,.30),(75,.30)])
enc=animation('Encourage','0:13',90);key(enc,root,15,[(0,0),(25,-.035),(55,-.035),(90,0)])
sm=SubElement(a,'StateMachine',name='KumkaController',id='0:7')
for nm,id in [('wave','0:20'),('success','0:21'),('encourage','0:22')]:SubElement(sm,'StateMachineTrigger',name=nm,id=id)
layer=SubElement(sm,'StateMachineLayer',name='Expression',id='0:8')
SubElement(layer,'AnyState',x='0',y='-160');SubElement(layer,'ExitState',x='200',y='-160');entry=SubElement(layer,'EntryState');SubElement(entry,'StateTransition',stateToId='0:12')
rest=SubElement(layer,'AnimationState',x='200',y='0',id='0:12',animationId='0:6')
for i,(anim,st,trig) in enumerate([('0:10','0:30','0:20'),('0:11','0:31','0:21'),('0:13','0:32','0:22')]):
 t=SubElement(rest,'StateTransition',stateToId=st,duration='120');SubElement(t,'TransitionTriggerCondition',inputId=trig)
 s=SubElement(layer,'AnimationState',x='450',y=str(180*i),id=st,animationId=anim)
 SubElement(s,'StateTransition',stateToId='0:12',duration='120',enableExitTime='true',exitTimeIsPercetange='true',exitTime='100')
indent(r);Path(__file__).with_name('scene.rml').write_bytes(tostring(r,encoding='utf-8'))
