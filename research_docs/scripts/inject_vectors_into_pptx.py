#!/usr/bin/env python3
"""Replace PPTX raster/wmf media with EMF or inject SVGs where available.

Usage: python inject_vectors_into_pptx.py --input input.pptx --out output.pptx --figdir ../figures

The script prefers EMF (fig_N.emf) for media replacement. If EMF is absent but
fig_N.svg exists it will replace the corresponding media part with the SVG bytes
and update [Content_Types].xml and any .rels that reference the media part.

This uses only the Python stdlib (zipfile + xml.etree) so it should run in the
project environment without extra packages.
"""

import argparse
import io
import os
import re
import zipfile
import xml.etree.ElementTree as ET


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to source PPTX")
    p.add_argument("--out", required=True, help="Path to output PPTX")
    p.add_argument("--figdir", required=True, help="Directory containing fig_N.emf/.svg files")
    return p.parse_args()


def find_media_candidates(figdir, idx):
    # prefer emf then svg
    base = os.path.join(figdir, f"fig_{idx}")
    candidates = []
    emf = base + ".emf"
    svg = base + ".svg"
    if os.path.exists(emf):
        candidates.append((emf, 'emf', 'image/x-emf'))
    if os.path.exists(svg):
        candidates.append((svg, 'svg', 'image/svg+xml'))
    return candidates


def update_content_types(content_types_xml, old_partname, new_partname, new_ct):
    # content_types_xml is an ElementTree root
    ns = ''
    # Try to find Override for old_partname and either update it or add a new Override
    found = False
    for ov in content_types_xml.findall('.//Override'):
        if ov.get('PartName') == old_partname:
            ov.set('PartName', new_partname)
            ov.set('ContentType', new_ct)
            found = True
    if not found:
        ET.SubElement(content_types_xml, 'Override', PartName=new_partname, ContentType=new_ct)


def replace_in_rels_xml(rels_xml_root, old_target, new_target):
    # rels_xml_root is the parsed ElementTree root
    for rel in rels_xml_root.findall('.//Relationship'):
        t = rel.get('Target')
        if not t:
            continue
        # Targets in rels are often relative like "media/image1.png"
        if t.endswith(old_target):
            rel.set('Target', t[:-len(old_target)] + new_target)


def main():
    args = parse_args()
    src = args.input
    out = args.out
    figdir = args.figdir

    if not os.path.exists(src):
        raise SystemExit(f"Input PPTX not found: {src}")
    if not os.path.isdir(figdir):
        raise SystemExit(f"Figure dir not found: {figdir}")

    media_name_re = re.compile(r'^ppt/media/image(\d+)\.(png|wmf|emf|jpg|jpeg)$', re.IGNORECASE)

    with zipfile.ZipFile(src, 'r') as zin:
        namelist = zin.namelist()
        # Read content types
        content_types_xml = None
        if '[Content_Types].xml' in namelist:
            content_types_xml = ET.fromstring(zin.read('[Content_Types].xml'))

        # Read all rels into memory for modification
        rels_map = {}
        for name in namelist:
            if name.startswith('ppt/') and name.endswith('.rels'):
                rels_map[name] = ET.fromstring(zin.read(name))

        # Prepare output zip
        with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for name in namelist:
                data = zin.read(name)
                m = media_name_re.match(name)
                if m:
                    idx = int(m.group(1))
                    candidates = find_media_candidates(figdir, idx)
                    if not candidates:
                        # no vector candidate; copy original
                        zout.writestr(name, data)
                        continue

                    # pick first candidate (emf preferred)
                    path, ext, ctype = candidates[0]
                    with open(path, 'rb') as fh:
                        newbytes = fh.read()

                    # new part name under ppt/media - keep same imageN but extension may change
                    new_name = f'ppt/media/image{idx}.{ext}'

                    # write new media part
                    zout.writestr(new_name, newbytes)

                    # update any rels that referenced the old media file
                    old_target = os.path.basename(name)
                    new_target = os.path.basename(new_name)
                    for rels_name, rels_root in rels_map.items():
                        # make a string copy, modify, write back later
                        replace_in_rels_xml(rels_root, old_target, new_target)

                    # update content types
                    if content_types_xml is not None:
                        update_content_types(content_types_xml, f'/{name}', f'/{new_name}', ctype)
                    continue

                # update rels files later (we'll write modified versions below)
                if name in rels_map:
                    # write modified rels
                    rel_root = rels_map[name]
                    # NB: preserve XML declaration
                    rel_bytes = ET.tostring(rel_root, encoding='utf-8')
                    zout.writestr(name, rel_bytes)
                    continue

                if name == '[Content_Types].xml' and content_types_xml is not None:
                    ct_bytes = ET.tostring(content_types_xml, encoding='utf-8')
                    zout.writestr(name, ct_bytes)
                    continue

                # default: copy unchanged
                zout.writestr(name, data)

    print(f'Wrote {out}')


if __name__ == '__main__':
    main()
