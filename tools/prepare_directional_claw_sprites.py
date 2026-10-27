"""Split generated equal-cell atlases into independent transparent game PNGs."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'tools/art/shooting-test'
DEST = ROOT / 'game/images/shooting_test'

def split(name, columns, rows):
    with Image.open(ART / name) as source:
        assert source.mode == 'RGBA'
        for row in range(rows):
            for col in range(columns):
                yield row,col,source.crop((round(col*source.width/columns),round(row*source.height/rows),
                                          round((col+1)*source.width/columns),round((row+1)*source.height/rows)))

def save(frame,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    frame.save(path,optimize=True)
    with Image.open(path) as check:
        assert check.mode == 'RGBA' and check.tobytes() == frame.tobytes()

for row,col,cell in split('aim-directions-sheet.png',5,2):
    # Same logical canvas and forearm baseline as the existing reload sequence.
    frame = Image.new('RGBA',(600,500))
    frame.paste(cell.resize((400,400),Image.Resampling.LANCZOS),(100,0))
    save(frame,DEST / 'aim' / ('%s-%02d.png' % (('idle','fire')[row],col)))
    if col == 2:
        save(frame,DEST / 'aim' / ('center-%s.png' % ('idle','fire')[row]))

for row,col,cell in split('monster-claw-sheet.png',4,2):
    save(cell.resize((362,362),Image.Resampling.LANCZOS),DEST / 'monster' / ('claw-%02d.png' % (row*4+col)))
print('Verified 10 directional aim/fire PNGs and 8 claw swipe PNGs.')
