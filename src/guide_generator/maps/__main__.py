"""Google My Maps CSV export CLI."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from guide_generator.maps.build import build_map_csv

_REPO_ROOT = Path(__file__).resolve().parents[3]
_TOPICS = _REPO_ROOT / "topics"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export topic guide sites to Google My Maps CSV"
    )
    parser.add_argument(
        "topic",
        help="Topic id or path to topics/<topic_id>/",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output CSV path (default: topics/<id>/guide_map.csv)",
    )
    args = parser.parse_args(argv)

    topic_arg = Path(args.topic)
    if topic_arg.is_dir():
        topic_dir = topic_arg.resolve()
    else:
        topic_dir = (_TOPICS / args.topic).resolve()

    try:
        result = build_map_csv(topic_dir, args.output)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {result.csv_path} ({len(result.placemarks)} placemarks)")
    if result.skipped:
        print(f"Skipped {len(result.skipped)} site(s) without coordinates:", file=sys.stderr)
        for slug, reason in result.skipped:
            print(f"  - {slug}: {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
