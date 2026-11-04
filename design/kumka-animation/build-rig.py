"""Native vector character rig. The approved drawing is the source of truth.

Joint hierarchy + independently drawn hand/forearm; eyelid aperture clipping;
separate pupil/glint controls. No image assets, meshes, skins or scripts.
"""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, indent, tostring
import runpy, math

HERE=Path(__file__).resolve().parent
src=runpy.run_path(str(HERE.parent/'kumka-vector/build-vector.py'))
parts={p['name']:p for p in src['parts']}
parse=src['parse']; gradients=src['gradients']
r=Element('Rive',version='1',kind='fragment')
a=SubElement(r,'Artboard',name='Kumka',id='0:2',width='724',height='644',styleId='0:5',defaultStateMachineId='0:7')
SubElement(a,'LayoutComponentStyle',id='0:5')
counter=iter(range(100,10000))
def uid():return '0:'+str(next(counter))
def el(p,t,**kw):
    return SubElement(p,t,id=uid(),**{k:str(v) for k,v in kw.items()})
root=el(a,'Node',name='Motion / ground pivot',x=362,y=590,scaleX=.5,scaleY=.5)
body=el(root,'RootBone',name='Body',x=0,y=0,length=0)
shadow=el(a,'Shape',name='Ground shadow',x=362,y=600,opacity=.14)
el(shadow,'Ellipse',width=390,height=24)
shadowfill=el(shadow,'Fill')
el(shadowfill,'SolidColor',colorValue='FF75445F')

def group(parent,name,origin,parentorigin=(724,1025),bone=False):
    return el(parent,'RootBone' if bone else 'Node',name=name,
              x=origin[0]-parentorigin[0],y=origin[1]-parentorigin[1])

def local(p,origin,angle=0):
    dx,dy=p[0]-origin[0],p[1]-origin[1]
    return (math.cos(angle)*dx+math.sin(angle)*dy,-math.sin(angle)*dx+math.cos(angle)*dy)

def shape(parent,name,d,paint,origin=(724,1025),angle=0,stroke=None):
    s=el(parent,'Shape',name=name)
    pp=el(s,'PointsPath',name=name+' contour',isClosed='true')
    points=parse(d)
    area=sum(p[0][0]*q[0][1]-q[0][0]*p[0][1] for p,q in zip(points,points[1:]+points[:1]))
    pp.set('isClockwise',str(area>0).lower())
    vertices=[]
    for pt,hin,hout in points:
        x,y=local(pt,origin,angle)
        attrs=dict(x=x,y=y)
        for prefix,h in [('in',hin),('out',hout)]:
            hx,hy=local(h,origin,angle) if h else (x,y)
            dx,dy=hx-x,hy-y
            attrs[prefix+'Rotation']=math.atan2(dy,dx)
            attrs[prefix+'Distance']=math.hypot(dx,dy)
        vertices.append(el(pp,'CubicDetachedVertex',**attrs))
    if paint:
        f=el(s,'Stroke' if stroke else 'Fill',name='Paint',**(dict(thickness=stroke,cap='round',join='round') if stroke else {}))
        c1,c2,(x1,y1,x2,y2)=gradients[paint]
        x1,y1=local((x1,y1),origin,angle);x2,y2=local((x2,y2),origin,angle)
        g=el(f,'LinearGradient',name=paint,startX=x1,startY=y1,endX=x2,endY=y2)
        el(g,'GradientStop',colorValue='FF'+c1,position=0)
        el(g,'GradientStop',colorValue='FF'+c2,position=1)
    return s,vertices

def art(parent,name,origin=(724,1025),angle=0):
    v=parts[name];return shape(parent,name,v['path'],v['paint'],origin,angle)

legs=[]
for side,origin in [('left',(250,830)),('right',(1170,830))]:
    b=group(body,'Hind leg / '+side,origin,bone=True);legs.append(b)
    art(b,side+'-hind-leg',origin)
art(body,'body-contour')

# Two-bone joint: shoulder -> wrist. Each owns real vector contours.
shoulder_origin=(1120,620);wrist_origin=(1185,535)
dx=wrist_origin[0]-shoulder_origin[0];dy=wrist_origin[1]-shoulder_origin[1]
angle=math.atan2(dy,dx)
shoulder=group(body,'Wave / shoulder',shoulder_origin,bone=True)
shoulder.set('length',str(math.hypot(dx,dy)));shoulder.set('rotation',str(angle))
forearm='''M 1094 568 C 1113 549 1138 527 1158 507
 C 1176 497 1196 507 1214 527 C 1232 545 1244 559 1248 573
 C 1229 610 1201 645 1166 672 C 1148 638 1120 602 1094 568 Z'''
shape(shoulder,'Wave forearm',forearm,'pink',shoulder_origin,angle)
wrist=el(shoulder,'Bone',name='Wave / wrist',length=80,rotation=0)
hand='''M 1158 507 C 1141 472 1144 435 1164 409 C 1183 383 1211 388 1226 405
 C 1241 422 1236 444 1231 459 C 1250 440 1276 417 1299 426
 C 1320 433 1333 453 1323 476 C 1315 491 1299 502 1288 509
 C 1315 516 1329 533 1315 556 C 1302 584 1276 586 1248 573
 C 1217 586 1171 553 1158 507 Z'''
shape(wrist,'Wave hand / three fingers',hand,'pink',wrist_origin,angle)

art(body,'pale-belly')
for name in ['large-left-spot','small-left-spot','small-right-spot','large-right-spot']:art(body,name)
arms=[]
for side,origin in [('left',(385,780)),('right',(1040,810))]:
    b=group(body,'Front arm / '+side,origin,bone=True);arms.append(b)
    art(b,side+'-front-arm',origin);art(b,side+'-arm-crease',origin)

face=group(body,'Face / follow-through',(724,320))
gazes=[];lids=[];creases=[]
for side,cx in [('left',510),('right',935)]:
    origin=(cx,300)
    eye=group(face,'Eye / '+side,origin,(724,320))
    white,_=art(eye,side+'-eye-white',origin)
    gaze=el(eye,'Node',name='Gaze / '+side);gazes.append(gaze)
    pupil,_=art(gaze,side+'-pupil',origin)
    glint,_=art(gaze,side+'-eye-glint',origin)
    # Equal upper/lower cubic arcs move together to form a fully closed lid.
    # Eye geometry stays full-sized; clipping reveals skin underneath it.
    x0,x1=(370,650) if side=='left' else (800,1075)
    aperture=f'M {x0} 125 C {x0+80} 165 {x1-80} 165 {x1} 125 L {x1} 450 C {x1-80} 490 {x0+80} 490 {x0} 450 Z'
    mask,vertices=shape(eye,'Lid aperture / '+side,aperture,None,origin)
    lids.append((vertices,origin))
    for s in [white,pupil,glint]:
        el(s,'ClippingShape',sourceId=mask.attrib['id'],name='Clip / eyelids')
    for s in [pupil,glint]:
        el(s,'ClippingShape',sourceId=white.attrib['id'],name='Clip / eye outline')
    line=f'M {x0+20} 303 C {x0+90} 343 {x1-90} 343 {x1-20} 303'
    crease,_=shape(eye,'Closed lid crease / '+side,line,'ink',origin,stroke=7)
    crease.find('PointsPath').set('isClosed','false');crease.set('opacity','0');creases.append(crease)
for name in ['nostril-left','nostril-right']:art(face,name,(724,320))
mouth=group(face,'Mouth / smile',(724,470),(724,320))
art(mouth,'smile',(724,470));art(mouth,'smile-corner',(724,470))

def animation(name,duration,loop='oneShot'):
    return el(a,'LinearAnimation',name=name,duration=duration,fps=60,loopValue=loop)
def key(anim,obj,prop,pairs,ease=(.42,0,.58,1)):
    k=el(anim,'KeyedObject',objectId=obj.attrib['id'])
    p=el(k,'KeyedProperty',propertyKey=prop)
    for frame,value in pairs:
        f=el(p,'KeyFrameDouble',frame=frame,value=value,interpolationType='cubic' if ease else 'linear')
        if ease:el(f,'CubicEaseInterpolator',x1=ease[0],y1=ease[1],x2=ease[2],y2=ease[3])

def blink(anim,poses):
    for vertices,origin in lids:
        for i,v in enumerate(vertices):
            openy=125 if i<2 else 450
            key(anim,v,25,[(f,openy+(303-openy)*closed-origin[1]) for f,closed in poses])
    for c in creases:
        key(anim,c,18,[(f,max(0,(closed-.83)/.17)) for f,closed in poses])

idle=animation('Idle',300,'loop')
key(idle,body,17,[(0,1),(75,1.007),(150,1),(225,1.007),(300,1)])
key(idle,body,16,[(0,1),(75,.998),(150,1),(225,.998),(300,1)])
blink(idle,[(0,0),(136,0),(141,1),(143,1),(153,0),(300,0)])

bl=animation('Blink',72)
blink(bl,[(0,0),(16,0),(21,1),(23,1),(34,0),(72,0)])

look=animation('LookAround',180)
for gaze in gazes:
    key(look,gaze,13,[(0,0),(20,0),(35,-16),(68,-16),(86,14),(122,14),(145,0),(180,0)])
    key(look,gaze,14,[(0,0),(35,-3),(68,-3),(86,-6),(122,-6),(145,0),(180,0)])
key(look,face,13,[(0,0),(38,-3),(68,-3),(91,3),(122,3),(151,0),(180,0)])
key(look,face,15,[(0,0),(38,-.012),(68,-.012),(91,.012),(122,.012),(151,0),(180,0)])
blink(look,[(0,0),(75,0),(79,1),(81,1),(90,0),(180,0)])

wave=animation('Wave',132)
key(wave,shoulder,15,[(0,angle),(13,angle-.06),(30,angle+.09),(48,angle+.04),(66,angle+.09),(84,angle+.04),(108,angle-.018),(124,angle),(132,angle)])
key(wave,wrist,15,[(0,0),(15,-.12),(31,.24),(48,-.20),(65,.22),(82,-.16),(100,.08),(116,-.025),(128,0),(132,0)])
key(wave,body,15,[(0,0),(16,-.012),(40,.01),(90,.006),(118,-.002),(132,0)])
key(wave,face,15,[(0,0),(22,.015),(85,.015),(121,0),(132,0)])
blink(wave,[(0,0),(95,0),(100,1),(102,1),(113,0),(132,0)])

success=animation('Success',126)
key(success,shadow,16,[(0,1),(16,1.08),(47,.78),(76,1),(82,1.09),(108,1),(126,1)])
key(success,shadow,18,[(0,.14),(16,.16),(47,.07),(76,.14),(82,.16),(108,.14),(126,.14)])
key(success,root,14,[(0,590),(16,590),(27,559),(47,524),(60,535),(76,590),(83,590),(99,590),(126,590)])
key(success,body,16,[(0,1),(16,1.045),(27,.977),(47,.995),(73,.987),(82,1.045),(96,.992),(112,1),(126,1)])
key(success,body,17,[(0,1),(16,.94),(27,1.035),(47,1.012),(73,1.025),(82,.947),(96,1.009),(112,1),(126,1)])
for sign,b in [(-1,legs[0]),(1,legs[1])]:
    key(success,b,15,[(0,0),(17,-sign*.035),(36,sign*.11),(56,sign*.11),(76,0),(90,sign*.025),(107,0),(126,0)])
for sign,b in [(-1,arms[0]),(1,arms[1])]:
    key(success,b,15,[(0,0),(18,sign*.025),(39,-sign*.09),(60,-sign*.09),(79,sign*.025),(104,0),(126,0)])
key(success,shoulder,15,[(0,angle),(17,angle-.04),(35,angle+.14),(63,angle+.13),(84,angle-.03),(106,angle),(126,angle)])
key(success,wrist,15,[(0,0),(21,-.1),(41,.13),(63,.13),(84,-.07),(107,0),(126,0)])
key(success,mouth,17,[(0,1),(20,1.04),(37,1.17),(65,1.17),(89,1.04),(112,1),(126,1)])
key(success,face,14,[(0,320-1025),(18,320-1025+5),(39,320-1025-6),(65,320-1025-6),(85,320-1025+7),(109,320-1025),(126,320-1025)])
for gaze in gazes:key(success,gaze,14,[(0,0),(18,2),(35,-9),(65,-9),(86,3),(109,0),(126,0)])
blink(success,[(0,0),(9,0),(15,1),(18,1),(27,0),(76,0),(81,1),(83,1),(94,0),(126,0)])

# Explicit rest keys in every action allow reliable blending back to Idle.
animations=[idle,bl,look,wave,success]
defaults={}
for n in r.iter():
    if 'id' not in n.attrib:continue
    for prop,attr,default in [(13,'x',0),(14,'y',0),(15,'rotation',0),(16,'scaleX',1),(17,'scaleY',1),(18,'opacity',1),(25,'y',0)]:
        defaults[n.attrib['id'],prop]=float(n.attrib.get(attr,default))
allkeys={(k.attrib['objectId'],int(p.attrib['propertyKey'])) for anim in animations for k in anim.findall('KeyedObject') for p in k.findall('KeyedProperty')}
objects={n.attrib['id']:n for n in r.iter() if 'id' in n.attrib}
for anim in animations:
    own={(k.attrib['objectId'],int(p.attrib['propertyKey'])) for k in anim.findall('KeyedObject') for p in k.findall('KeyedProperty')}
    for oid,prop in sorted(allkeys-own):key(anim,objects[oid],prop,[(0,defaults[oid,prop]),(int(anim.attrib['duration']),defaults[oid,prop])])

vm=SubElement(r,'ViewModel',name='KumkaControls',id='0:40',defaultInstanceId='0:41')
instance=SubElement(vm,'ViewModelInstance',name='Default',id='0:41',exports='true')
a.set('viewModelId','0:40');a.set('viewModelInstanceId','0:41')
sm=SubElement(a,'StateMachine',name='KumkaController',id='0:7')
triggers={}
for name in ['blink','look','wave','success']:
    triggers[name]=el(vm,'ViewModelPropertyTrigger',name=name)
    el(instance,'ViewModelInstanceTrigger',viewModelPropertyId=triggers[name].attrib['id'])
layer=el(sm,'StateMachineLayer',name='Character')
el(layer,'AnyState',x=0,y=-150);el(layer,'ExitState',x=200,y=-150)
entry=el(layer,'EntryState',x=-200,y=0)
states=[]
for i,anim in enumerate(animations):states.append(el(layer,'AnimationState',animationId=anim.attrib['id'],reset='true',x=i*180,y=0 if i==0 else 180))
el(entry,'StateTransition',stateToId=states[0].attrib['id'])
for trigger,state in zip(['blink','look','wave','success'],states[1:]):
    t=el(states[0],'StateTransition',stateToId=state.attrib['id'],duration=100)
    condition=el(t,'TransitionViewModelCondition',opValue='equal')
    comparator=el(condition,'TransitionPropertyViewModelComparator')
    bindable=el(comparator,'BindablePropertyTrigger')
    el(bindable,'DataBindContext',sourcePathIds='0:40-'+triggers[trigger].attrib['id'],propertyKey=686)
    el(condition,'TransitionValueTriggerComparator')
    el(state,'StateTransition',stateToId=states[0].attrib['id'],duration=180,enableExitTime='true',exitTimeIsPercetange='true',exitTime=100)

a.remove(sm);a.insert(1,sm)
# Rive draws siblings front-to-back. Authoring above is back-to-front.
for n in r.iter():
    if n.tag in ['Node','RootBone','Bone']:n[:]=list(reversed(list(n)))
indent(r)
(HERE/'scene.rml').write_bytes(tostring(r,encoding='utf-8'))
import json
(HERE/'rig-manifest.json').write_text(json.dumps(dict(artboard='Kumka',stateMachine='KumkaController',entry=entry.attrib['id'],states={anim.attrib['name']:state.attrib['id'] for anim,state in zip(animations,states)},triggers={name:t.attrib['id'] for name,t in triggers.items()},animations={n.attrib['name']:dict(durationFrames=int(n.attrib['duration']),fps=60) for n in animations}),indent=2)+'\n')
print('Built native bone rig, clipped eyelids and five timelines.')
