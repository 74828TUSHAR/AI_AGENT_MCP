from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TARGET_DIR_NAMES = {
    ".pytest_cache",
    "__pycache__",
    "allure-results",
    "downloads",
    "logs",
    "reports",
    "screenshots",
    "video",
}

TARGET_FILE_NAMES = {
    "test-results.xml",
}


def iter_targets(root: Path):
    for path in root.rglob("*"):
        if path.name in TARGET_FILE_NAMES and path.is_file():
            yield path
        elif path.name in TARGET_DIR_NAMES and path.is_dir():
            yield path


def remove_target(path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] remove {path.relative_to(PROJECT_ROOT)}")
        return

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)
    print(f"removed {path.relative_to(PROJECT_ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove generated Playwright artifacts before committing."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without deleting anything.",
    )
    args = parser.parse_args()

    if not PROJECT_ROOT.exists():
        raise SystemExit(f"Project root not found: {PROJECT_ROOT}")

    targets = sorted(
        {path.resolve() for path in iter_targets(PROJECT_ROOT)},
        key=lambda path: len(path.relative_to(PROJECT_ROOT).parts),
        reverse=True,
    )

    if not targets:
        print("No generated artifacts found.")
        return 0

    for target in targets:
        remove_target(target, args.dry_run)

    if args.dry_run:
        print("Dry run complete. No files were deleted.")
    else:
        print("Cleanup complete.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
