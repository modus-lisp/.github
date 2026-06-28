#!/usr/bin/env python3
"""Final modus (m) mark: 70s orange-teal, 10px stroke, tight crop.
Outputs full master, tight-crop avatar PNGs, and a size legibility sheet."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
SS=4; S=640*SS; W=int(10*SS)
BG=(38,28,20); PC=(224,86,30); MC=(40,150,138)   # warm dark / burnt orange / teal
def lerp(a,b,t): return a+(b-a)*t
def quad(p0,p1,p2,n):
    o=[]
    for i in range(n+1):
        t=i/n
        o.append(((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],
                  (1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]))
    return o
def line(p0,p1,n): return [(lerp(p0[0],p1[0],i/n),lerp(p0[1],p1[1],i/n)) for i in range(n+1)]
def P(x,y): return (x*SS,y*SS)
def stamp(d,pts,r,c):
    for (x,y) in pts: d.ellipse([x-r,y-r,x+r,y+r],fill=c)
NS=260
lparen=quad(P(215,235),P(165,327),P(215,460),NS)
rparen=quad(P(425,235),P(475,327),P(425,460),NS)
stem =line(P(258,295),P(258,400),NS)
hump1=quad(P(258,295),P(290,255),P(322,295),NS)+line(P(322,295),P(322,400),NS)
hump2=quad(P(322,295),P(354,255),P(386,295),NS)+line(P(386,295),P(386,400),NS)
mpaths=(stem,hump1,hump2); ppaths=(lparen,rparen)
def master():
    img=Image.new("RGB",(S,S),BG); d=ImageDraw.Draw(img)
    for p in ppaths: stamp(d,p,W,PC)
    for p in mpaths: stamp(d,p,W,MC)
    return img
def tight_square(img,pad_frac=0.14):
    arr=np.asarray(img).astype(int); bgv=np.array(BG)
    mask=(np.abs(arr-bgv).sum(2)>30); ys,xs=np.where(mask)
    y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    side=max(y1-y0,x1-x0); pad=int(side*pad_frac); side+=2*pad
    cy=(y0+y1)//2; cx=(x0+x1)//2
    return img.crop((cx-side//2,cy-side//2,cx+side//2,cy+side//2))

m=master(); sq=tight_square(m)
m.resize((640,640),Image.LANCZOS).save("/tmp/modus-final-full.png")     # padded master
sq.resize((512,512),Image.LANCZOS).save("/tmp/modus-final.png")         # tight preview
sq.resize((420,420),Image.LANCZOS).save("/tmp/modus-avatar.png")        # avatar upload
sq.resize((1024,1024),Image.LANCZOS).save("/tmp/modus-mark-1024.png")   # hi-res archive

# size sheet
SIZES=[256,128,64,40,32]
cell=270; gap=24; top=66
sheet=Image.new("RGB",(cell*len(SIZES)+gap*(len(SIZES)+1),cell+top+gap+40),(22,22,28))
d=ImageDraw.Draw(sheet)
try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",22)
except: font=ImageFont.load_default()
d.text((gap,20),"modus (m) — 70s orange-teal, 10px, tight crop  (actual pixel sizes)",fill=(230,230,235),font=font)
for i,s in enumerate(SIZES):
    x=gap+i*(cell+gap); a=sq.resize((s,s),Image.LANCZOS)
    sheet.paste(a,(x+(cell-s)//2,top+(cell-s)//2)); d.text((x+4,top+cell+6),f"{s}px",fill=(205,205,215),font=font)
sheet.save("/tmp/modus-final-sizes.png")
print("wrote /tmp/modus-final.png, modus-avatar.png (420), modus-mark-1024.png, modus-final-sizes.png")
