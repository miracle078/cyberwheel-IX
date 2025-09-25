#!/usr/bin/env bash
# Compile all standalone tikz fig_*.tex files in research_docs/figures to PDF and convert to SVG.
# Requires: tectonic or pdflatex, and either pdf2svg or inkscape.

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")"/.. && pwd)"
FIG_DIR="$ROOT_DIR/figures"
cd "$FIG_DIR"

# Compile
for f in fig_*.tex; do
  echo "Compiling $f..."
  if command -v tectonic >/dev/null 2>&1; then
    tectonic "$f"
  else
    pdflatex -interaction=nonstopmode "$f" >/dev/null
  fi
done

# Convert PDFs to SVGs
for pdf in fig_*.pdf; do
  svg="${pdf%.pdf}.svg"
  echo "Converting $pdf -> $svg"
  if command -v pdf2svg >/dev/null 2>&1; then
    pdf2svg "$pdf" "$svg" || echo "pdf2svg failed for $pdf"
  elif command -v inkscape >/dev/null 2>&1; then
    inkscape "$pdf" --export-type=svg --export-filename="$svg" || echo "inkscape failed for $pdf"
  else
    echo "No pdf->svg tool found. Skipping conversion for $pdf"
  fi
done

echo "All done. SVGs are in $FIG_DIR"
