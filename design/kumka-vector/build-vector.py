"""Hand-authored Bézier artwork. Emits SVG and native Rive shapes from one source.

No bitmap embedding, image meshes, automatic tracing or runtime scripts.
Coordinates follow the approved 1448×1086 artwork. This is a likeness review,
not the final animation or a replacement for the production asset yet.
"""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring, indent
import re, math

OUT = Path(__file__).resolve().parent
parts = []
def part(group, name, path, paint):
    parts.append(dict(group=group, name=name, path=path, paint=paint))

# Back legs are complete shapes behind the body, with their own silhouettes.
part('leg-left', 'left-hind-leg', '''M 225 715 C 168 699 119 729 103 773
 C 83 826 127 870 178 901 C 130 905 90 919 78 949
 C 58 988 109 1003 156 977 L 192 958 C 179 986 195 1005 222 1005
 C 263 1008 290 982 309 951 L 368 923 C 345 863 297 758 225 715 Z''', 'limb')
part('leg-right', 'right-hind-leg', '''M 1139 718 C 1192 703 1252 722 1276 762
 C 1308 816 1264 868 1209 901 C 1262 901 1308 921 1324 950
 C 1346 991 1290 1004 1244 979 L 1206 959 C 1221 987 1202 1007 1171 1006
 C 1133 1006 1108 984 1092 953 L 1039 924 C 1066 846 1100 764 1139 718 Z''', 'limb')

# Body and eye mounds form one continuous contour, rather than overlapping ovals.
part('body', 'body-contour', '''M 369 383 C 350 350 340 313 348 273
 C 354 208 387 154 441 125 C 493 97 543 108 589 132
 C 634 156 661 199 673 249 C 706 241 742 242 773 249
 C 787 194 820 148 868 125 C 915 101 962 106 1005 125
 C 1069 153 1103 215 1101 282 C 1101 322 1090 357 1075 383
 C 1104 424 1126 474 1145 522 C 1168 578 1182 641 1172 707
 C 1175 771 1147 834 1093 880 C 1047 921 999 945 945 961
 C 819 992 622 987 505 962 C 422 943 335 902 278 847
 C 224 796 201 744 208 684 C 211 617 241 557 284 501
 C 319 456 345 418 369 383 Z''', 'pink')

# Raised limb overlaps the right shoulder. The hidden root extends into the body.
part('arm-wave', 'waving-arm', '''M 1094 568 C 1113 549 1138 527 1158 507
 C 1141 472 1144 435 1164 409 C 1183 383 1211 388 1226 405
 C 1241 422 1236 444 1231 459 C 1250 440 1276 417 1299 426
 C 1320 433 1333 453 1323 476 C 1315 491 1299 502 1288 509
 C 1315 516 1329 533 1315 556 C 1302 584 1276 586 1248 573
 C 1229 610 1201 645 1166 672 C 1148 638 1120 602 1094 568 Z''', 'pink')

part('belly', 'pale-belly', '''M 428 718 C 491 624 602 568 720 573
 C 856 568 987 648 1005 763 C 980 801 949 856 930 905
 C 891 911 862 931 846 958 C 748 995 630 983 574 964
 C 557 930 518 912 487 905 C 475 840 449 767 428 718 Z''', 'belly')

# Four characteristic spots; asymmetric hand-shaped paths preserve the reference.
part('spots-left', 'large-left-spot', '''M 250 536 C 282 498 322 475 355 480
 C 394 480 418 505 406 541 C 396 578 355 611 315 622
 C 281 631 251 619 243 598 C 235 578 240 554 250 536 Z''', 'spot')
part('spots-left', 'small-left-spot', '''M 268 665 C 282 643 311 638 330 647
 C 350 656 350 676 338 694 C 326 713 297 720 279 710
 C 262 702 261 681 268 665 Z''', 'spot')
part('spots-right', 'small-right-spot', '''M 1005 557 C 1020 536 1045 536 1062 551
 C 1077 565 1079 588 1067 604 C 1052 624 1026 621 1011 607
 C 995 593 995 573 1005 557 Z''', 'spot')
part('spots-right', 'large-right-spot', '''M 1038 652 C 1062 632 1095 639 1119 666
 C 1143 692 1151 726 1132 749 C 1113 773 1081 768 1056 751
 C 1026 731 1012 683 1038 652 Z''', 'spot')

part('arm-left', 'left-front-arm', '''M 334 761 C 315 805 327 852 332 883
 C 305 864 293 844 278 825 C 296 873 325 903 365 923
 C 332 935 316 966 326 989 C 333 1009 357 1015 381 1006
 C 392 1002 403 984 412 963 C 403 989 409 1013 434 1023
 C 466 1037 496 1015 491 986 L 488 963 C 502 991 522 1016 548 1008
 C 576 1001 582 977 569 954 C 556 928 521 914 487 905
 C 472 843 449 787 431 724 C 393 743 361 752 334 761 Z''', 'pink')
# The upper boundary is hidden by the body/belly; inner creases are separate.
part('arm-left', 'left-arm-crease', '''M 334 761 C 327 826 339 883 366 923
 L 349 930 C 325 880 318 817 334 761 Z''', 'crease')
part('arm-right', 'right-front-arm', '''M 1005 763 C 1026 791 1053 811 1091 814
 C 1090 854 1072 889 1042 919 C 1071 927 1091 945 1099 965
 C 1110 993 1092 1010 1068 1010 C 1042 1010 1024 988 1008 968
 C 1019 996 1007 1019 983 1025 C 956 1032 934 1012 935 989 L 938 969
 C 921 997 898 1013 875 1007 C 848 1001 836 980 849 957
 C 863 929 894 913 930 905 C 950 849 974 802 1005 763 Z''', 'pink')
part('arm-right', 'right-arm-crease', '''M 1091 814 C 1082 860 1066 895 1042 919
 L 1058 925 C 1082 890 1095 848 1091 814 Z''', 'crease')

# Eye whites follow the original pear shapes. The pupils are separately editable.
part('eye-left', 'left-eye-white', '''M 469 179 C 508 176 563 215 597 257
 C 626 291 636 322 624 352 C 612 389 578 414 541 419
 C 498 424 451 406 417 374 C 391 348 380 314 388 280
 C 397 233 434 185 469 179 Z''', 'cream')
part('eye-left', 'left-pupil', '''M 547 210 C 577 225 599 250 607 277
 C 617 311 602 350 575 368 C 551 384 521 375 501 356
 C 476 334 470 305 480 275 C 489 243 515 214 547 210 Z''', 'ink')
part('eye-left', 'left-eye-glint', '''M 573 239 C 584 237 593 247 593 258
 C 594 271 585 281 574 281 C 563 280 553 270 553 259
 C 552 248 560 239 573 239 Z''', 'cream')
part('eye-right', 'right-eye-white', '''M 974 179 C 1008 179 1036 207 1050 244
 C 1068 288 1054 338 1026 374 C 1001 404 965 421 929 420
 C 882 421 841 390 824 353 C 806 321 825 286 850 261
 C 884 223 940 181 974 179 Z''', 'cream')
part('eye-right', 'right-pupil', '''M 900 210 C 932 208 956 231 969 261
 C 985 293 976 329 954 353 C 934 377 908 382 883 369
 C 853 353 836 319 840 286 C 842 257 862 223 886 213
 C 891 211 895 210 900 210 Z''', 'ink')
part('eye-right', 'right-eye-glint', '''M 936 239 C 948 236 957 247 958 258
 C 958 271 950 281 938 281 C 927 281 917 271 917 259
 C 916 249 924 240 936 239 Z''', 'cream')

part('nose', 'nostril-left', '''M 679 369 C 688 366 702 377 704 386
 C 707 398 697 403 687 396 C 677 391 666 374 679 369 Z''', 'ink')
part('nose', 'nostril-right', '''M 765 368 C 777 367 774 383 765 392
 C 758 401 747 400 744 391 C 741 381 756 367 765 368 Z''', 'ink')
part('mouth', 'smile', '''M 563 444 C 652 499 790 503 879 441
 C 886 437 895 440 899 446 C 814 540 646 548 552 467
 C 536 453 548 435 563 444 Z''', 'ink')
part('mouth', 'smile-corner', '''M 883 421 C 900 423 916 437 921 449
 C 927 462 917 466 907 458 C 899 449 889 442 879 438
 C 865 432 869 418 883 421 Z''', 'ink')

gradients = {
 'pink': ('EBA0BD','E89AB8', (520,220,920,950)),
 'belly': ('F8D6E3','F4CBDB', (570,600,860,980)),
 'spot': ('CF7B9E','C66E93', (280,500,1100,790)),
 'limb': ('D984A7','D17C9F', (200,740,900,1030)),
 'crease': ('D681A5','CE789D', (300,780,1000,990)),
 'cream': ('FFF9E9','FCF3E2', (500,180,800,420)),
 'ink': ('593147','4E2A40', (600,220,800,520)),
}

# SVG: one named layer per controllable feature, genuine cubic paths only.
svg = Element('svg', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 1448 1086',
              width='1448', height='1086', role='img')
SubElement(svg, 'title').text = 'Kumka — vector likeness study'
defs = SubElement(svg,'defs')
for name,(c1,c2,xy) in gradients.items():
    x1,y1,x2,y2=xy
    g=SubElement(defs,'linearGradient',id=name,gradientUnits='userSpaceOnUse',
                 x1=str(x1),y1=str(y1),x2=str(x2),y2=str(y2))
    SubElement(g,'stop',offset='0',attrib={'stop-color':'#'+c1})
    SubElement(g,'stop',offset='1',attrib={'stop-color':'#'+c2})
for v in parts:
    group=SubElement(svg,'g',id=v['name'],attrib={'data-rig-group':v['group']})
    SubElement(group,'path',d=v['path'],fill='url(#'+v['paint']+')')
indent(svg)
(OUT/'kumka-vector.svg').write_bytes(tostring(svg,encoding='utf-8',xml_declaration=True))

# Rive uses the same cubic curves; there is no ImageAsset, Image, Mesh or Skin.
r=Element('Rive',version='1',kind='fragment')
a=SubElement(r,'Artboard',name='Kumka vector study',id='0:2',width='724',height='543',styleId='0:5')
SubElement(a,'LayoutComponentStyle',id='0:5')
root=SubElement(a,'Node',name='Kumka',id='0:100',scaleX='.5',scaleY='.5')
ids=iter(range(110,10000))
def uid(): return '0:'+str(next(ids))

def parse(d):
    tokens=re.findall(r'[MCLZ]|-?\d+(?:\.\d+)?',d);i=0;points=[]
    while i<len(tokens):
        cmd=tokens[i];i+=1
        if cmd=='Z':break
        count={'M':2,'L':2,'C':6}[cmd]
        nums=list(map(float,tokens[i:i+count]));i+=count
        if cmd=='M':points.append([tuple(nums),None,None])
        elif cmd=='L':points.append([tuple(nums),None,None])
        else:
            points[-1][2]=tuple(nums[:2]);points.append([tuple(nums[4:]),tuple(nums[2:4]),None])
    if points[-1][0]==points[0][0]:
        points[0][1]=points[-1][1];points.pop()
    return points

for v in reversed(parts):
    group=SubElement(root,'Node',name=v['group']+' / '+v['name'],id=uid())
    shape=SubElement(group,'Shape',name=v['name'],id=uid())
    points=parse(v['path'])
    area=sum(p[0][0]*q[0][1]-q[0][0]*p[0][1] for p,q in zip(points,points[1:]+points[:1]))
    path=SubElement(shape,'PointsPath',name='Bezier contour',id=uid(),isClosed='true',isClockwise=str(area>0).lower())
    for (x,y),hin,hout in points:
        attrs=dict(x=str(x),y=str(y),id=uid())
        for prefix,handle in [('in',hin),('out',hout)]:
            dx,dy=(handle[0]-x,handle[1]-y) if handle else (0,0)
            attrs[prefix+'Rotation']=str(math.atan2(dy,dx))
            attrs[prefix+'Distance']=str(math.hypot(dx,dy))
        SubElement(path,'CubicDetachedVertex',**attrs)
    fill=SubElement(shape,'Fill',name='Fill')
    c1,c2,(x1,y1,x2,y2)=gradients[v['paint']]
    grad=SubElement(fill,'LinearGradient',name=v['paint'],startX=str(x1),startY=str(y1),endX=str(x2),endY=str(y2))
    SubElement(grad,'GradientStop',colorValue='FF'+c1,position='0')
    SubElement(grad,'GradientStop',colorValue='FF'+c2,position='1')
indent(r)
(OUT/'scene.rml').write_bytes(tostring(r,encoding='utf-8'))
print(f'{len(parts)} named vector parts; no raster assets or meshes')
