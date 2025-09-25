from pptx import Presentation
import zipfile
p='/rds/general/user/moa324/home/projects/cyberwheel/research_docs/cyberwheel_slides_from_original_4x3.pptx'
prs=Presentation(p)
print('slides_count', len(prs.slides))
print('slide_width_pts', prs.slide_width, 'slide_height_pts', prs.slide_height)
# 914400 EMU per inch
print('slide_size_inches', prs.slide_width/914400.0, prs.slide_height/914400.0)
with zipfile.ZipFile(p) as z:
    media=[n for n in z.namelist() if n.startswith('ppt/media/')]
    print('media_files', media)
    try:
        ct=z.read('[Content_Types].xml').decode()
        print('has_svg_content_type', 'image/svg+xml' in ct)
        imgs=[l for l in ct.splitlines() if 'image/' in l]
        print('content_types_image_lines_count', len(imgs))
        for line in imgs[:20]:
            print('  ', line)
    except Exception as e:
        print('ct_error', e)
print('Done')
