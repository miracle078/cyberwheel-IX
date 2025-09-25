#!/usr/bin/env python3
r"""
Replace embedded PNG media in a PPTX with SVG bytes (change content type) by matching PNG bytes
with the generated PNG fallbacks in research_docs/figures/. Produces a new PPTX with the same
structure but SVG media content — an experimental attempt to make diagrams editable as SVG in Office.
"""
import zipfile
from pathlib import Path
import hashlib
from xml.etree import ElementTree as ET

pptx_in = Path('/rds/general/user/moa324/home/projects/cyberwheel/research_docs/cyberwheel_slides_from_original.pptx')
if not pptx_in.exists():
    print('Input PPTX not found:', pptx_in)
    raise SystemExit(1)

out = pptx_in.with_name(pptx_in.stem + '_svg_injected.pptx')
fig_dir = pptx_in.parent / 'figures'
pngs = list(sorted(fig_dir.glob('fig_*.png')))
# compute hashes for png fallbacks
png_hash_map = {}
for p in pngs:
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    png_hash_map[h] = p

# read all entries
with zipfile.ZipFile(pptx_in, 'r') as zin:
    namelist = zin.namelist()
    # find media files
    media_files = [n for n in namelist if n.startswith('ppt/media/')]
    print('Found media files in PPTX:', media_files)
    media_bytes = {n: zin.read(n) for n in media_files}
    content_types = zin.read('[Content_Types].xml')
    content_types_xml = ET.fromstring(content_types)

# mapping from media file -> matching svg path
replace_map = {}
for name, data in media_bytes.items():
    h = hashlib.sha256(data).hexdigest()
    if h in png_hash_map:
        svg_path = png_hash_map[h].with_suffix('.svg')
        if svg_path.exists():
            replace_map[name] = svg_path
            print('Will replace', name, 'with', svg_path.name)
        else:
            print('Matched PNG but SVG missing for', png_hash_map[h])
    else:
        print('No match for media', name)

if not replace_map:
    print('No media matched PNG fallbacks; aborting')
    raise SystemExit(0)

# update [Content_Types].xml: change Override ContentType for matched parts
ns = {'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}
for override in content_types_xml.findall('ct:Override', ns):
    part = override.attrib.get('PartName')
    if part and part.startswith('/ppt/media/'):
        key = part.lstrip('/')
        if key in replace_map:
            print('Updating content type for', part)
            override.set('ContentType', 'image/svg+xml')

# write new pptx with replaced media bytes and updated content types
with zipfile.ZipFile(pptx_in, 'r') as zin, zipfile.ZipFile(out, 'w') as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename in replace_map:
            # write svg bytes instead
            svg_bytes = replace_map[item.filename].read_bytes()
            zout.writestr(item, svg_bytes)
            print('Wrote SVG into', item.filename)
        elif item.filename == '[Content_Types].xml':
            # write modified content types
            zout.writestr(item, ET.tostring(content_types_xml, encoding='utf-8', xml_declaration=True))
            print('Wrote updated [Content_Types].xml')
        else:
            zout.writestr(item, data)

print('Wrote new PPTX with SVG media:', out)
