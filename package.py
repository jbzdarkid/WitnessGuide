from pathlib import Path
from PIL import Image
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_BZIP2, ZIP_LZMA
from progressbar import ProgressBar, Bar, Percentage

guide_names = {
  'WG_100_final': '100%',
  'WG_100_advanced_final': '100% (advanced)',
  'WG_all_discards': 'All Discarded Panels',
  'WG_all_discards_low': 'All Discarded Panels Low%',
  'WG_all_lasers_final': 'All Lasers',
  'WG_any_final': 'Any%',
  'WG_any_final2': 'Any% (v2)',
  'WG_any_v3': 'Any% (v3)',
  'WG_any_desert_final': 'Any% (desert route)',
}

guides = {}
for dir in Path('.').iterdir():
  if not dir.is_dir():
    continue
  dir = dir.name
  if not dir.startswith('WG_'):
    continue
  if dir not in guide_names:
    print(f'Guide named {dir} skipped, missing proper name')
    continue
  guides[dir] = guide_names[dir] + '.zip'

TMP = Path('./tmp.png').resolve()
for guide, name in guides.items():
  # mode=w: Modify existing files
  # compression=ZIP_LZMA for maginally better compression
  with ZipFile(name, mode='w', compression=ZIP_LZMA) as zip:
    files = list(Path(guide).iterdir())
    bar = ProgressBar(maxval=len(files), widgets=[Bar('=', '[', ']'), ' ', Percentage()])
    bar.start()
    for i, file in enumerate(files):
      bar.update(i)
      if file.suffix == '.png':
        try:
          im = Image.open(file)
        except OSError as e:
          print(e)
          print(f'Skipping file {file.name}, as it could not be opened.')
        if im.width == 1920 and im.height == 1080:
          im = im.resize((720, 480))
          im.save(TMP, 'PNG')
          zip.write(TMP, file.name)
          continue
      zip.write(file)
    bar.finish()
  print(f'Wrote {name}')
TMP.unlink()
