TikZ extraction and conversion workflow

This folder contains helper scripts to extract TikZ figures from the Beamer file and convert
them to vector images that can be embedded into a PowerPoint produced by pandoc.

Steps

1. Extract tikzpicture blocks

   From the repository root run:

     python3 research_docs/scripts/extract_tikz.py research_docs/cyberwheel_slides_final.tex

   This writes standalone wrappers to research_docs/figures/fig_<n>.tex

2. Compile each wrapper to PDF and convert to SVG

   From the figures dir (or run the helper):

     research_docs/scripts/compile_and_convert.sh

   Requirements: tectonic or pdflatex, and pdf2svg or inkscape in PATH.

3. Convert LaTeX slides to PPTX with pandoc (basic)

   - First create a LaTeX source where tikzpicture blocks have been replaced with image includes
     referencing the exported SVGs (e.g., figures/fig_1.svg). You can do this manually, or use
     a small script to replace the tikzpicture blocks with \includegraphics commands.

   - Then run:

     pandoc -s -t pptx research_docs/cyberwheel_slides_for_pptx.tex -o cyberwheel_slides.pptx

   Notes:
   - Pandoc's LaTeX reader doesn't support all Beamer features. You will likely need to produce a
     simplified LaTeX file where each slide is a separate section or contains plain content and
     image references instead of TikZ code.

4. Optional: programmatic PPTX assembly

   For more control, generate a PPTX template and insert the exported SVGs into slides using
   python-pptx. See https://python-pptx.readthedocs.io/ for docs.

Troubleshooting

- If tectonic fails due to missing fonts or LaTeX packages, try pdflatex or install missing packages.
- If svg output is rasterized or missing elements, try using inkscape instead of pdf2svg.
- If the main .tex file doesn't compile because of unmatched environments, run the provided
  research_docs/scripts/check_tex_envs.py (or similar) to locate unclosed \begin{...} blocks.

