"""Build HTML and PDF from a topic folder."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path

from guide_generator.pdf.merge import merge_topic_markdown

_CSS = Path(__file__).resolve().parent / "assets" / "guide.css"

# Preferred browser executables (Edge first — guaranteed on Win 10+)
_BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def _find_browser() -> str:
    for c in _BROWSER_CANDIDATES:
        if Path(c).is_file():
            return c
    exe = shutil.which("msedge") or shutil.which("chrome") or shutil.which("google-chrome")
    if exe:
        return exe
    raise RuntimeError(
        "No Chrome or Edge executable found. "
        "Install Microsoft Edge or Google Chrome to generate PDF."
    )


def _pandoc_to_html(md_path: Path, html_path: Path, topic_dir: Path, css: Path) -> None:
    """Convert merged Markdown to a self-contained HTML file via Pandoc.

    --embed-resources encodes all local images as base64 data URIs so the
    resulting HTML is completely self-contained and needs no external files.
    """
    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(html_path),
        "--standalone",
        "--embed-resources",        # inline all images/CSS as data URIs
        f"--css={css.resolve()}",
        "--toc",
        "--toc-depth=2",
        "--metadata", f"date={date.today().isoformat()}",
        "--resource-path", str(topic_dir),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding="utf-8")
    if result.stderr:
        # Pandoc often emits informational warnings; only raise on non-zero exit
        pass


def _html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    """Print HTML to PDF using Chrome/Edge headless.

    Chrome's headless print engine supports full modern CSS — @page, CSS Grid,
    break-before/after, print-color-adjust — giving publication-quality output.
    """
    browser = _find_browser()
    html_uri = html_path.resolve().as_uri()
    pdf_abs = str(pdf_path.resolve())

    with tempfile.TemporaryDirectory() as user_data_dir:
        cmd = [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--user-data-dir={user_data_dir}",
            f"--print-to-pdf={pdf_abs}",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            html_uri,
        ]
        subprocess.run(cmd, check=True, capture_output=True)


def build_pdf(topic_dir: Path, output: Path | None = None, html_output: Path | None = None) -> Path:
    """Compile topic guide to PDF. Returns path to generated PDF."""
    topic_dir = topic_dir.resolve()
    if not (topic_dir / "index.md").is_file():
        raise FileNotFoundError(f"Not a topic folder (no index.md): {topic_dir}")

    if shutil.which("pandoc") is None:
        raise RuntimeError("pandoc is required on PATH — see docs/PDF.md")

    _find_browser()  # fail early if no browser found

    pdf_path = (output or topic_dir / "guide.pdf").resolve()
    html_out = (html_output or topic_dir / "guide.html").resolve()

    combined, _slugs = merge_topic_markdown(topic_dir)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        md_path = tmp_dir / "guide.md"
        html_tmp = tmp_dir / "guide.html"

        md_path.write_text(combined, encoding="utf-8")
        _pandoc_to_html(md_path, html_tmp, topic_dir, _CSS)

        # Persist the HTML for debugging / inspection
        html_out.write_text(html_tmp.read_text(encoding="utf-8"), encoding="utf-8")

        _html_to_pdf(html_out, pdf_path)

    return pdf_path
