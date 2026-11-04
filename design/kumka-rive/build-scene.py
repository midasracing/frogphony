from pathlib import Path
from xml.etree.ElementTree import Element,SubElement,indent,tostring
r=Element('Rive',version='1',kind='fragment');a=SubElement(r,'Artboard',name='Kumka',id='0:2',width='500',height='500',defaultStateMachineId='0:7')
a.set('styleId','0:5');SubElement(a,'LayoutComponentStyle',id='0:5')
ids=iter(range(100,9999))
def node(p,name,x=0,y=0):return SubElement(p,'Node',name=name,id=f'0:{next(ids)}',x=str(x),y=str(y))
def ellipse(p,name,x,y,w,h,c,rot=0):
 s=SubElement(p,'Shape',name=name,id=f'0:{next(ids)}',x=str(x),y=str(y),rotation=str(rot));SubElement(s,'Ellipse',width=str(w),height=str(h));f=SubElement(s,'Fill');SubElement(f,'SolidColor',colorValue='FF'+c);return s
root=node(a,'Kumka',250,416)
ellipse(root,'LeftFoot',-117,0,130,42,'CE809F',-.16);ellipse(root,'RightFoot',117,0,130,42,'CE809F',.16)
body=node(root,'BreathingBody',0,0)
ellipse(body,'Body',0,-139,306,294,'ECAFC5');ellipse(body,'LeftEyeMound',-77,-284,123,144,'ECAFC5');ellipse(body,'RightEyeMound',77,-284,123,144,'ECAFC5')
ellipse(body,'Belly',0,-77,202,159,'F9DCE5')
for n,x,y,w,h in [('SpotL',-118,-163,44,31),('SpotL2',-125,-125,23,22),('SpotR',121,-136,38,45),('SpotR2',114,-181,23,24)]:ellipse(body,n,x,y,w,h,'CE809F')
l=node(body,'LeftArm',-103,-112);ellipse(l,'LeftForearm',0,38,33,102,'E39DB9',-.10);ellipse(l,'LeftPalm',4,87,49,27,'E39DB9')
for x in [-12,0,12]:ellipse(l,'LeftFinger'+str(x),x+4,94,15,24,'E39DB9')
arm=node(body,'RightArm',104,-112);ellipse(arm,'RightForearm',26,-24,32,100,'E39DB9',.66);ellipse(arm,'RightPalm',56,-62,41,37,'E39DB9')
for x,y,rot in [(46,-86,-.2),(65,-84,.5),(77,-67,1.1)]:ellipse(arm,'RightFinger',x,y,16,38,'E39DB9',rot)
face=node(body,'Face',0,0)
eyes=[]
for name,x in [('LeftEye',-77),('RightEye',77)]:
 e=node(face,name,x,-278);eyes.append(e)
 ellipse(e,'EyeWhite',0,0,78,99,'FFF9E8');ellipse(e,'Pupil',7 if x<0 else -7,5,45,67,'493144');ellipse(e,'Highlight',15 if x<0 else 1,-17,15,16,'FFF9E8')
ellipse(face,'LeftNostril',-12,-214,9,13,'493144',-.4);ellipse(face,'RightNostril',12,-214,9,13,'493144',.4)
# Curved crescent smile with cubic vertices (angles are radians).
s=SubElement(face,'Shape',name='Smile');path=SubElement(s,'PointsPath',isClosed='true')
for x,y,ir,ind,orr,outd in [(-53,-190,0,0,.65,36),(53,-190,2.49,36,2.2,45),(-53,-190,.94,45,0,0)]:SubElement(path,'CubicDetachedVertex',x=str(x),y=str(y),inRotation=str(ir),inDistance=str(ind),outRotation=str(orr),outDistance=str(outd))
f=SubElement(s,'Fill');SubElement(f,'SolidColor',colorValue='FF493144')
def animation(name,id,duration,loop='oneShot'):
 return SubElement(a,'LinearAnimation',name=name,id=id,duration=str(duration),fps='60',loopValue=loop)
def key(anim,obj,prop,pairs):
 k=SubElement(anim,'KeyedObject',objectId=obj.attrib['id']);p=SubElement(k,'KeyedProperty',propertyKey=str(prop))
 for frame,val in pairs:SubElement(p,'KeyFrameDouble',frame=str(frame),value=str(val),interpolationType='linear')
idle=animation('Idle','0:6',240,'loop')
key(idle,body,17,[(0,1),(60,1.018),(120,1),(180,1.018),(240,1)])
for e in eyes:key(idle,e,17,[(0,1),(92,1),(96,.06),(100,1),(203,1),(207,.06),(211,1),(240,1)])
wave=animation('Wave','0:10',90);key(wave,arm,15,[(0,0),(15,-.2),(28,.23),(41,-.22),(54,.23),(70,-.15),(90,0)])
success=animation('Success','0:11',75);key(success,root,14,[(0,416),(9,423),(24,386),(40,416),(47,423),(60,416),(75,416)]);key(success,root,17,[(0,1),(9,.94),(24,1.05),(40,1),(47,.95),(60,1),(75,1)])
enc=animation('Encourage','0:13',90);key(enc,face,15,[(0,0),(25,-.065),(55,-.065),(90,0)])
sm=SubElement(a,'StateMachine',name='KumkaController',id='0:7')
for name,id in [('wave','0:20'),('success','0:21'),('encourage','0:22')]:SubElement(sm,'StateMachineTrigger',name=name,id=id)
lay=SubElement(sm,'StateMachineLayer',name='Expression',id='0:8');SubElement(lay,'AnyState',x='0',y='-160');SubElement(lay,'ExitState',x='200',y='-160');entry=SubElement(lay,'EntryState');SubElement(entry,'StateTransition',stateToId='0:12')
rest=SubElement(lay,'AnimationState',x='200',y='0',id='0:12',animationId='0:6')
for nm,anim,st,trig in [('Wave','0:10','0:30','0:20'),('Success','0:11','0:31','0:21'),('Encourage','0:13','0:32','0:22')]:
 t=SubElement(rest,'StateTransition',stateToId=st,duration='120');SubElement(t,'TransitionTriggerCondition',inputId=trig)
 stt=SubElement(lay,'AnimationState',x='450',y=str(180*int(st.split(':')[1])-5400),id=st,animationId=anim);SubElement(stt,'StateTransition',stateToId='0:12',duration='120',enableExitTime='true',exitTimeIsPercetange='true',exitTime='100')
for n in r.iter('Node'): n[:] = list(reversed(list(n)))
indent(r);Path(__file__).with_name('scene.rml').write_bytes(tostring(r,encoding='utf-8'))
