#!/usr/bin/env bash
# Convert PDFs in the figures directory to EMF files.
# Tries: inkscape (modern CLI), inkscape (legacy flags), then pstoedit.
# Usage: ./convert_pdfs_to_emf.sh /path/to/research_docs/figures
set -euo pipefail
DIR=${1:-$(pwd)}
if [ ! -d "$DIR" ]; then
  echo "Directory $DIR not found"
  exit 2
fi
shopt -s nullglob
PDFS=("$DIR"/*.pdf)
if [ ${#PDFS[@]} -eq 0 ]; then
  echo "No PDF files found in $DIR"
  exit 0
fi
for pdf in "${PDFS[@]}"; do
  base=$(basename "$pdf" .pdf)
  emf="$DIR/${base}.emf"
  echo "Converting $pdf -> $emf"

  # Try modern Inkscape (>=1.0)
  if command -v inkscape >/dev/null 2>&1; then
    echo " - trying inkscape (modern CLI)"
    if inkscape "$pdf" --export-type=emf --export-filename="$emf" >/dev/null 2>&1; then
      echo "   -> success (inkscape --export-type=emf)"
      continue
    fi
    echo " - modern inkscape failed or not supported, trying legacy flags"
    # Try older CLI flags
    if inkscape --export-emf="$emf" "$pdf" >/dev/null 2>&1; then
      echo "   -> success (inkscape --export-emf)"
      continue
    fi
  fi

  # Try pstoedit (requires ghostscript and pstoedit + libwmf installed)
  if command -v pstoedit >/dev/null 2>&1; then
    echo " - trying pstoedit"
    if pstoedit -f emf "$pdf" "$emf" >/dev/null 2>&1; then
      echo "   -> success (pstoedit)"
      continue
    fi
  fi

  echo "Failed to convert $pdf to EMF. Recommended options:
  - Install Inkscape >= 1.0 and try again: https://inkscape.org/
  - Or install Ghostscript + pstoedit + libwmf and try pstoedit: https://pstoedit.sourceforge.net/"
  echo "You can also convert manually on Windows by opening the PDF in Inkscape and saving as EMF."
  # do not exit - continue with other files
done

echo "Done"
