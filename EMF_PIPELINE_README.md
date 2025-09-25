EMF Conversion & PPTX pipeline

Goal
----
Produce a PowerPoint where TikZ diagrams are embedded as PowerPoint-native vectors (EMF), so they are editable in PowerPoint.

Why EMF
------
- PowerPoint on Windows (and many versions of Office) treats EMF as a native vector format that can be ungrouped and edited.
- Embedding raw SVG into PPTX sometimes works on modern Office, but compatibility is inconsistent.

What I provided
----------------
- `scripts/convert_pdfs_to_emf.sh` - a shell script that tries to convert PDFs to EMF using Inkscape or pstoedit.
- `scripts/build_pptx_with_emf.py` - Python script that builds a PPTX embedding `fig_N.emf` when present; falls back to PNG if EMF is missing.

Recommended local setup (Windows preferred)
-------------------------------------------
1. Install Inkscape (>=1.0) on your local machine: https://inkscape.org
2. Optionally, install Ghostscript and pstoedit (for alternate conversion): https://pstoedit.sourceforge.net/
3. Copy the `research_docs/figures/*.pdf` files from this repository to your local machine.
4. Run the conversion script from a terminal / WSL / Git Bash (on Windows):

   ./scripts/convert_pdfs_to_emf.sh research_docs/figures

   - This will try Inkscape's CLI to write `fig_N.emf` files next to the PDFs.
   - If that fails, the README suggests pstoedit-based alternatives.

5. After conversion, run the Python builder locally (in the repo root) to create a PPTX with EMFs embedded:

   python3 research_docs/scripts/build_pptx_with_emf.py

   - Requirements: python3, python-pptx, cairosvg (for optional SVG->PNG fallback), Pillow if needed.
   - If you prefer, run it inside a virtualenv and `pip install python-pptx cairosvg`.

Notes and troubleshooting
-------------------------
- If EMF files are not created, the script will embed PNG fallbacks that were generated previously in this repo.
- On Windows, Inkscape can open the PDF and "Save As" EMF manually if CLI tools fail.
- EMF output quality depends on the original PDF and Inkscape conversion. If the diagrams use complex patterns, review the EMF and adjust Inkscape export settings.

If you'd like, I can:
- Walk you through a remote session to run these locally.
- Try installing Inkscape here (may not be practical on the HPC cluster).
- Finish the EMF conversion for you if you can provide a desktop environment or allow installing GUI tools.
