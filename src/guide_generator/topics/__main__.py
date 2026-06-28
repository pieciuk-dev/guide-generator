from __future__ import annotations

import sys
from pathlib import Path

from guide_generator.topics.scaffold import _TOPICS_DIR, init_topic, refresh_topic_profile


def main() -> None:
    if len(sys.argv) < 2:
        _usage()
        raise SystemExit(2)

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) < 3:
            _usage()
            raise SystemExit(2)
        trip_path = Path(sys.argv[2])
        if not trip_path.is_file():
            trip_path = _TRIPS_DIR / f"{sys.argv[2]}.yaml"
        if not trip_path.is_file():
            print(f"Trip file not found: {sys.argv[2]}")
            raise SystemExit(1)
        topic_dir = init_topic(trip_path.resolve())
        print(f"Created topic: {topic_dir}")
        return

    if command == "refresh-profile":
        if len(sys.argv) < 3:
            print("Usage: python -m guide_generator.topics refresh-profile <topic_id>")
            raise SystemExit(2)
        profile = refresh_topic_profile(sys.argv[2])
        print(f"Updated: {profile}")
        return

    _usage()
    raise SystemExit(2)


def _usage() -> None:
    print("Usage:")
    print("  python -m guide_generator.topics init data/trips/<trip_id>.yaml")
    print("  python -m guide_generator.topics refresh-profile <topic_id>")


if __name__ == "__main__":
    main()
