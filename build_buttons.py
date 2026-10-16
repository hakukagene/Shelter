from PIL import Image, ImageDraw
from pathlib import Path
import math, random
out=Path(__file__).parent/'game/gui/shelter/actions'; out.mkdir(parents=True,exist_ok=True)
for name,col in [('aim',(193,34,34)),('reject',(192,131,22)),('admit',(25,132,68)),('shoot',(193,34,34)),('lower',(192,131,22))]:
 im=Image.new('RGBA',(320,320)); pix=im.load()
 for y in range(320):
  for x in range(320):
   dx,dy=x-160,y-160;r=math.hypot(dx,dy)
   if r>154:continue
   if r>148:c=(14,13,12)
   elif r>122:
    light=(1-dy/160)*.5;v=int(48+100*light+30*math.sin(r*.5));c=(v,min(255,v+2),max(0,v-5))
   elif r>115:c=(12,13,12)
   elif r>111:c=tuple(min(255,int(v*1.5+40)) for v in col)
   elif r>105:c=tuple(int(v*.35) for v in col)
   else:
    light=.42+.55*(1-r/110)+.24*(1-dy/160);c=tuple(min(255,int(v*light)) for v in col)
   pix[x,y]=(*c,255)
 d=ImageDraw.Draw(im)
 random.seed(8)
 for i in range(190):
  x=random.randrange(12,308);y=random.randrange(12,308);r=math.hypot(x-160,y-160)
  if 125<r<146:d.line((x,y,x+random.randrange(1,5),y+1),fill=(23,22,20,130),width=1)
 for x,y in [(160,24),(296,160),(160,296),(24,160)]:
  d.ellipse((x-8,y-8,x+8,y+8),fill='#171716',outline='#999485',width=2);d.line((x-4,y+3,x+4,y-3),fill='#777267',width=2)
 cream='#f4dfaf'
 if name in ('shoot','lower'):
  # Compact, box-shaped MAC silhouette; angled down for the lower action.
  gun=Image.new('RGBA',(320,320));g=ImageDraw.Draw(gun)
  g.rounded_rectangle((105,91,203,124),radius=3,fill=cream)
  g.rectangle((203,102,228,113),fill=cream)
  g.rectangle((125,121,146,161),fill=cream)
  g.rectangle((128,158,143,172),fill=cream)
  g.line((151,124,171,124,171,141,149,141),fill=cream,width=5)
  g.line((157,124,155,133),fill=cream,width=3)
  g.line((105,102,87,102,87,142),fill=cream,width=5)
  g.rectangle((111,85,119,92),fill=cream)
  g.rectangle((190,86,197,92),fill=cream)
  g.line((117,101,187,101),fill='#32271c',width=3)
  if name=='lower':
   gun=gun.rotate(-28,resample=Image.Resampling.BICUBIC,center=(160,128))
   im.alpha_composite(gun)
   d=ImageDraw.Draw(im)
   d.line((218,135,218,161),fill=cream,width=5)
   d.polygon([(208,154),(218,168),(228,154)],fill=cream)
  else:
   im.alpha_composite(gun)
   d=ImageDraw.Draw(im)
   d.polygon([(232,106),(240,95),(238,104),(250,108),(238,113),(240,121),(232,112)],fill=cream)
 elif name=='aim':
  d.polygon([(104,93),(220,93),(220,116),(176,116),(166,130),(145,130),(133,160),(108,154),(120,116),(104,116)],fill=cream)
  d.rounded_rectangle((143,114,178,138),radius=8,outline=cream,width=6)
  d.line((156,115,154,126),fill=cream,width=4)
 else:
  d.line((119,158,119,82,170,82,170,103),fill=cream,width=8)
  d.line((119,158,170,158,170,140),fill=cream,width=8)
  if name=='reject':d.polygon([(150,110),(191,110),(191,96),(216,124),(191,150),(191,135),(150,135)],fill=cream)
  else:d.polygon([(211,110),(172,110),(172,96),(146,124),(172,150),(172,135),(211,135)],fill=cream)
 im.save(out/(name+'.png'))
