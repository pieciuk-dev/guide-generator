"""PDF export CLI."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from guide_generator.pdf.build import build_pdf

_REPO_ROOT = Path(__file__).resolve().parents[3]
_TOPICS = _REPO_ROOT / "topics"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile topic guide to PDF")
    parser.add_argument(
        "topic",
        help="Topic id or path to topics/<topic_id>/",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output PDF path (default: topics/<id>/guide.pdf)",
    )
    args = parser.parse_args(argv)

    topic_arg = Path(args.topic)
    if topic_arg.is_dir():
        topic_dir = topic_arg.resolve()
    else:
        topic_dir = (_TOPICS / args.topic).resolve()

    try:
        pdf = build_pdf(topic_dir, args.output)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {pdf}")
    html = topic_dir / "guide.html"
    if html.is_file():
        print(f"Wrote {html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
