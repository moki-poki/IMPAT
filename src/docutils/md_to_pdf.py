import subprocess
from pathlib import Path

def md_to_pdf(md_path, pdf_path=None):
    """
    Convert a Markdown file to PDF using pandoc with LaTeX formatting.
    Requires pandoc and a LaTeX distribution installed.
    """
    md_path = Path(md_path)
    if pdf_path is None:
        pdf_path = md_path.with_suffix('.pdf')
    else:
        pdf_path = Path(pdf_path)
    result = subprocess.run([
'pandoc', str(md_path), '-o', str(pdf_path), '--pdf-engine=pdflatex'    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Pandoc failed: {result.stderr}")
    return pdf_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py <input.md> [output.pdf]")
        sys.exit(1)
    md_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        out = md_to_pdf(md_file, pdf_file)
        print(f"PDF created at: {out}")
    except Exception as e:
        print(f"Error: {e}")
