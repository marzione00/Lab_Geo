from pathlib import Path
import fitz
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'Verifiche/Anteprime_figure';out.mkdir(exist_ok=True)
files=sorted((ROOT/'Risultati/Figure').glob('*.pdf'))
thumbs=[]
for file in files:
 doc=fitz.open(file);pix=doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
 pix.save(out/f'{file.stem}.png')
 im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
 im.thumbnail((620,300))
 tile=Image.new('RGB',(640,330),'#F8F6F1');tile.paste(im,((640-im.width)//2,26))
 ImageDraw.Draw(tile).text((10,7),file.stem,fill='#253344')
 thumbs.append(tile)
for group in range(4):
 montage=Image.new('RGB',(1280,1650),'white')
 for k,tile in enumerate(thumbs[group*10:(group+1)*10]):montage.paste(tile,((k%2)*640,(k//2)*330))
 montage.save(out/f'montage_{group+1}.jpg',quality=92)
print('40 render e4montaggi creati.')
