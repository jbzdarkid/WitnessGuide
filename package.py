from pathlib import Path
from PIL import Image
from zipfile import ZipFile, ZIP_DEFLATED
from progressbar import ProgressBar, Bar

guide_names = {
  'WG_100_advanced_final2': '100% (advanced)',
  'WG_100_final2': '100%',
  'WG_all_discards': 'All Discarded Panels',
  'WG_all_discards_low': 'All Discarded Panels Low%',
  'WG_all_lasers_final': 'All Lasers',
  'WG_any_v3': 'Any% (v3)',
  'WG_low_final': 'Low%',
}

TMP = Path('./tmp.png').resolve()

for dir in Path('.').iterdir():
  if not dir.is_dir():
    continue
  guide = dir.name
  if not guide.startswith('WG_'):
    continue
  if guide not in guide_names:
    print(f'Skipped folder {guide}')
    continue
  name = guide_names[guide] + '.zip'

  # mode=w: Modify existing files
  with ZipFile(name, mode='w', compression=ZIP_DEFLATED, compresslevel=9) as zip:
    files = list(Path(guide).iterdir())
    bar = ProgressBar(maxval=len(files), widgets=[Bar('=', '[', ']'), ' ', name])
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
          im = im.resize((1280, 720))
          im.save(TMP, 'PNG')
          zip.write(TMP, file.name)
          continue
      zip.write(file, file.name)
    bar.finish()
TMP.unlink()
