from __future__ import annotations

import sys

from guide_generator.audiences.validate import main as validate_main


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == "resolve":
        from guide_generator.audiences.resolve import main as resolve_main

        # resolve expects argv: script, audience_id, [output]
        sys.argv = [sys.argv[0], *sys.argv[2:]]
        resolve_main()
        return

    if len(sys.argv) >= 2 and sys.argv[1] not in ("validate",):
        print("Usage:")
        print("  python -m guide_generator.audiences              # validate audiences")
        print("  python -m guide_generator.audiences resolve <id> [output.md]")
        raise SystemExit(2)

    validate_main()


if __name__ == "__main__":
    main()
