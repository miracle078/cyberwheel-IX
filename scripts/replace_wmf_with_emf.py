#!/usr/bin/env python3
"""
Replace WMF media parts in a PPTX with EMF files from research_docs/figures/ (fig_N.emf).
Produces a new PPTX with updated content types.
"""
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

P = Path('/rds/general/user/moa324/home/projects')
PPTX_IN = P / 'cyberwheel/research_docs/cyberwheel_slides_recreated_emf.pptx'
PPTX_OUT = PPTX_IN.with_name(PPTX_IN.stem + '_emf_corrected.pptx')
FIG_DIR = P / 'cyberwheel/research_docs/figures'

if not PPTX_IN.exists():
    print('Input PPTX not found:', PPTX_IN)
    raise SystemExit(1)

with zipfile.ZipFile(PPTX_IN, 'r') as zin:
    files = {n: zin.read(n) for n in zin.namelist()}

# find media wmf entries
media = [n for n in files.keys() if n.startswith('ppt/media/')]
wmf_parts = [m for m in media if m.lower().endswith('.wmf')]
if not wmf_parts:
    print('No WMF parts found; nothing to do')
    raise SystemExit(0)

rename_map = {}
for m in wmf_parts:
    # try to deduce fig index from filename (image1.wmf -> fig_1.emf)
    stem = Path(m).stem  # image1
    # try to map by order: image1->fig_1, image2->fig_2
    try:
        idx = int(''.join(filter(str.isdigit, stem)))
    except Exception:
        idx = None
    if idx:
        candidate = FIG_DIR / f'fig_{idx}.emf'
        if candidate.exists():
            rename_map[m] = str(candidate)

if not rename_map:
    print('No matching EMF files found for WMF parts; aborting')
    raise SystemExit(0)

# Update [Content_Types].xml: add Default for emf? Usually use Override for each /ppt/media/imageX.emf
ct_xml = files['[Content_Types].xml']
ct = ET.fromstring(ct_xml)
ns = {'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}

for old_media, emf_path in rename_map.items():
    # write new media bytes under same media folder but with .emf name
    old_name = old_media
    base = Path(old_name).stem
    new_name = f'ppt/media/{base}.emf'
    files[new_name] = Path(emf_path).read_bytes()
    # remove old wmf part
    del files[old_name]
    # update any rels/presentation xml textual references
    for k in list(files.keys()):
        if k.endswith('.rels') or k.endswith('.xml'):
            try:
                s = files[k].decode('utf-8')
            except Exception:
                continue
            if old_name in s:
                s = s.replace(old_name, new_name)
                files[k] = s.encode('utf-8')

    # update [Content_Types].xml: add an Override entry for the new emf part if not present
    exists_override = any(o.attrib.get('PartName') == '/' + new_name for o in ct.findall('ct:Override', ns))
    if not exists_override:
        override = ET.SubElement(ct, '{http://schemas.openxmlformats.org/package/2006/content-types}Override')
        override.set('PartName', '/' + new_name)
        override.set('ContentType', 'image/x-emf')

# write modified content types back
files['[Content_Types].xml'] = ET.tostring(ct, encoding='utf-8', xml_declaration=True)

# write out new pptx
with zipfile.ZipFile(PPTX_OUT, 'w') as zout:
    for n, data in files.items():
        zout.writestr(n, data)

print('Wrote', PPTX_OUT)
