import os
from pathlib import Path
from md_to_pdf import md_to_pdf

def test_md_to_pdf_basic(tmp_path):
    # Create a simple markdown file
    md_content = """
# Test Title

This is a test paragraph.

- Item 1
- Item 2
"""
    md_file = tmp_path / "test.md"
    pdf_file = tmp_path / "test.pdf"
    md_file.write_text(md_content)

    # Run conversion
    out_pdf = md_to_pdf(md_file, pdf_file)
    assert out_pdf.exists(), "PDF file was not created."
    assert out_pdf.stat().st_size > 0, "PDF file is empty."
    print(f"PDF generated at: {out_pdf}")

if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        test_md_to_pdf_basic(Path(tmpdir))
