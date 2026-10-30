from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import numpy as np
out=Path(__file__).resolve().parent.parent/'game/gui/shelter/metal';out.mkdir(parents=True,exist_ok=True)
rng=np.random.default_rng(42)
def metal(name,w,h,red=False):
 noise=rng.normal(0,4,(h,w,1));base=np.array([43,38,35] if not red else [91,20,19])
 a=np.clip(base+noise,0,255).astype('uint8');im=Image.fromarray(a,'RGB');d=ImageDraw.Draw(im)
 d.rounded_rectangle((1,1,w-2,h-2),radius=9,outline='#090909',width=4)
 d.rounded_rectangle((7,7,w-8,h-8),radius=6,outline='#75675b',width=2)
 d.line((12,h-12,w-12,h-12),fill='#100d0c',width=3)
 for x,y in [(19,19),(w-20,19),(19,h-20),(w-20,h-20)]:
  d.ellipse((x-6,y-6,x+6,y+6),fill='#121212',outline='#776c61',width=1)
  d.line((x-3,y+2,x+3,y-2),fill='#9b8b79',width=1)
 for _ in range(w*h//2200):
  x=int(rng.integers(12,w-12));y=int(rng.integers(12,h-12));d.line((x,y,min(w-12,x+int(rng.integers(2,15))),y-1),fill='#49413a')
 im.save(out/name)
metal('panel.jpg',1080,780)
metal('button.png',400,70)
metal('selected.png',400,70,True)
metal('thumb.png',26,38)
