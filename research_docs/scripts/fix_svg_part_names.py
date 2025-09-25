#!/usr/bin/env python3
r"""
Rename media parts that contain SVG bytes to .svg and update all relationship targets and [Content_Types].xml
so PowerPoint sees them as SVG parts. Input file should be the svg-injected PPTX.
"""
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

inp = Path('/rds/general/user/moa324/home/projects/cyberwheel/research_docs/cyberwheel_slides_from_original_svg_injected.pptx')
if not inp.exists():
    print('Input PPTX not found:', inp)
    raise SystemExit(1)
out = inp.with_name(inp.stem + '_svg_injected_renamed.pptx')

with zipfile.ZipFile(inp, 'r') as zin:
    namelist = zin.namelist()
    media = [n for n in namelist if n.startswith('ppt/media/')]
    print('Found media parts:', media)
    # detect which media parts are SVG by checking start bytes
    svg_parts = []
    for m in media:
        b = zin.read(m)
        head = b[:200].lstrip()
        if head.startswith(b'<?xml') or head.startswith(b'<svg') or b'<svg' in head:
            svg_parts.append(m)
    print('Detected SVG parts:', svg_parts)
    # parse content types
    ct_xml = zin.read('[Content_Types].xml')
    ct = ET.fromstring(ct_xml)

    # build mapping old->new name
    rename_map = {}
    for old in svg_parts:
        base = Path(old).stem
        new = f'ppt/media/{base}.svg'
        rename_map[old] = new

    if not rename_map:
        print('No svg parts detected, aborting')
        raise SystemExit(0)

    # read all files into memory
    files = {n: zin.read(n) for n in namelist}

# update relationships files: replace targets that reference media/*.png with media/*.svg where applicable
for name, data in list(files.items()):
    if name.endswith('.rels') or name.endswith('presentation.xml') or name.endswith('.xml'):
        try:
            s = data.decode('utf-8')
        except Exception:
            continue
        modified = False
        for old, new in rename_map.items():
            old_rel = old.replace('ppt/','')
            new_rel = new.replace('ppt/','')
            if old_rel in s:
                s = s.replace(old_rel, new_rel)
                modified = True
        if modified:
            files[name] = s.encode('utf-8')
            print('Updated rels/xml:', name)

# update content types: change Override PartName for media png to .svg and ContentType to image/svg+xml
ns = {'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}
modified_ct = False
for override in ct.findall('ct:Override', ns):
    pn = override.attrib.get('PartName')
    if pn and pn.startswith('/ppt/media/'):
        path = pn.lstrip('/')
        if path in rename_map:
            newpn = '/' + rename_map[path]
            override.set('PartName', newpn)
            override.set('ContentType', 'image/svg+xml')
            modified_ct = True

if modified_ct:
    files['[Content_Types].xml'] = ET.tostring(ct, encoding='utf-8', xml_declaration=True)
    print('Updated [Content_Types].xml')

# write new zip with renamed media entries
with zipfile.ZipFile(out, 'w') as zout:
    for n, data in files.items():
        if n in rename_map:
            # write under new name
            newname = rename_map[n]
            zout.writestr(newname, data)
            print('Wrote renamed media', newname)
        elif n in rename_map.values():
            # skip if duplicate
            continue
        else:
            zout.writestr(n, data)

print('Wrote', out)
