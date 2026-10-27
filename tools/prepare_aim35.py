"""Export individual aim poses from generated atlases; no runtime cropping."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'tools/art/shooting-test/aim35'
OUT = ROOT / 'game/images/shooting_test/aim35'
NAMES = ('up-high','up-soft','level','down-soft','down-high')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    signatures = set()
    for pitch,name in enumerate(NAMES):
        with Image.open(ART / (name+'.png')) as source:
            assert source.mode == 'RGBA'
            alpha = source.getchannel('A')
            # Locate the transparent gutter between the two authored rows.
            candidates = range(round(source.height*.45),round(source.height*.56))
            divider = min(candidates,key=lambda y:(sum(alpha.crop((0,y,source.width,y+1)).getdata()),abs(y-source.height/2)))
            print(name,source.size,'row divider',divider)
            row_bounds = ((0,divider),(divider,source.height))
            for pose,(top,bottom) in enumerate(row_bounds):
                for yaw in range(7):
                    cell = source.crop((round(yaw*source.width/7),top,round((yaw+1)*source.width/7),bottom))
                    # Fixed canvas preserves authored muzzle-height differences.
                    frame = Image.new('RGBA',(600,500))
                    frame.paste(cell.resize((400,400),Image.Resampling.LANCZOS),(100,0))
                    target = OUT / ('%s-%02d-%02d.png' % (('idle','fire')[pose],pitch,yaw))
                    frame.save(target,optimize=True)
                    with Image.open(target) as check:
                        assert check.mode == 'RGBA' and check.size == (600,500)
                        assert check.tobytes() == frame.tobytes()
                        assert check.getchannel('A').getextrema() == (0,255)
                    signatures.add(frame.tobytes())
    assert len(signatures) == 70
    print('Verified 70 distinct independent RGBA sprites: 35 idle + 35 fire.')

if __name__ == '__main__':
    main()
