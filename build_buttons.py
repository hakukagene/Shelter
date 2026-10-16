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
 if name in ('aim','shoot','lower'):
  # Makarov PM-style compact pistol: rounded slide and short curved grip.
  gun=Image.new('RGBA',(320,320));g=ImageDraw.Draw(gun)
  g.rounded_rectangle((100,91,224,116),radius=8,fill=cream)
  g.polygon([(106,111),(177,111),(172,124),(150,131),(140,167),(111,161),(120,123),(102,121)],fill=cream)
  g.rounded_rectangle((146,116,183,141),radius=10,outline=cream,width=5)
  g.line((160,119,157,130),fill=cream,width=4)
  g.rectangle((211,87,217,93),fill=cream)
  g.rectangle((109,87,115,93),fill=cream)
  g.polygon([(100,103),(93,111),(103,115)],fill=cream)
  for x in [111,117,123,129]:g.line((x,96,x-3,108),fill='#32271c',width=2)
  g.line((131,132,123,155),fill='#32271c',width=3)
  if name=='lower':
   gun=gun.rotate(-28,resample=Image.Resampling.BICUBIC,center=(160,128))
  im.alpha_composite(gun);d=ImageDraw.Draw(im)
  if name=='lower':
   d.line((222,140,222,162),fill=cream,width=5)
   d.polygon([(212,155),(222,170),(232,155)],fill=cream)
  elif name=='shoot':
   d.polygon([(229,101),(240,93),(237,103),(249,107),(237,112),(240,121),(229,113)],fill=cream)

 else:
  d.line((119,158,119,82,170,82,170,103),fill=cream,width=8)
  d.line((119,158,170,158,170,140),fill=cream,width=8)
  if name=='reject':d.polygon([(150,110),(191,110),(191,96),(216,124),(191,150),(191,135),(150,135)],fill=cream)
  else:d.polygon([(211,110),(172,110),(172,96),(146,124),(172,150),(172,135),(211,135)],fill=cream)
 im.save(out/(name+'.png'))
