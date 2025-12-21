import json
from pathlib import Path

KERNEL_NAME = "tcga_tf"
DISPLAY_NAME = "Python (tcga_tf)"
LANGUAGE = "python"


def update_notebook(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))

    # Ensure minimal required keys exist
    if "cells" not in data:
        data["cells"] = []

    # Notebook-level metadata
    metadata = data.get("metadata") or {}
    metadata["kernelspec"] = {
        "display_name": DISPLAY_NAME,
        "language": LANGUAGE,
        "name": KERNEL_NAME,
    }
    metadata.setdefault("language_info", {"name": LANGUAGE})
    if isinstance(metadata.get("language_info"), dict):
        metadata["language_info"].setdefault("name", LANGUAGE)

    data["metadata"] = metadata

    # Standard nbformat fields (safe defaults)
    data.setdefault("nbformat", 4)
    data.setdefault("nbformat_minor", 5)

    original = path.read_text(encoding="utf-8")
    updated = json.dumps(data, ensure_ascii=False, indent=4) + "\n"

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True

    return False


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    notebooks = [
        p
        for p in project_root.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in p.parts
    ]

    changed = []
    for nb in sorted(notebooks):
        if update_notebook(nb):
            changed.append(nb)

    print(f"Found {len(notebooks)} notebooks")
    print(f"Updated {len(changed)} notebooks")
    for p in changed:
        print(f" - {p.relative_to(project_root)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
