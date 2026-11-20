#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def inspect(root: Path):
    results = []
    for vc in sorted(root.rglob("*ViewController.swift")):
        feature = vc.parent
        missing = []
        if not (feature / "DESIGN.md").is_file():
            missing.append("DESIGN.md")

        swift_files = [path for path in feature.rglob("*.swift") if path != vc]
        names = [path.name for path in swift_files]
        expected = {
            "Views": any("View" in name or "Cell" in name for name in names),
            "ViewModel": any("ViewModel" in name for name in names),
            "Model": any("Model" in name for name in names),
        }
        for directory, needed in expected.items():
            if needed and not (feature / directory).is_dir():
                missing.append(f"{directory}/")

        misplaced = []
        for path in swift_files:
            relative = path.relative_to(feature)
            name = path.name
            if ("ViewModel" in name and relative.parts[0] != "ViewModel") or (
                ("View" in name or "Cell" in name)
                and "ViewController" not in name
                and relative.parts[0] != "Views"
            ) or ("Model" in name and relative.parts[0] != "Model"):
                misplaced.append(str(relative))

        results.append(
            {
                "view_controller": str(vc.relative_to(root)),
                "feature_directory": str(feature.relative_to(root)) or ".",
                "missing": missing,
                "misplaced_candidates": misplaced,
            }
        )
    return results


def main():
    parser = argparse.ArgumentParser(description="Find VC feature structure review candidates.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    results = inspect(root)
    violations = [item for item in results if item["missing"] or item["misplaced_candidates"]]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif not results:
        print("No ViewController files found.")
    else:
        for item in results:
            print(f"## {item['view_controller']}")
            print(f"Feature directory: {item['feature_directory']}")
            print("Missing: " + (", ".join(item["missing"]) or "none"))
            print("Misplaced candidates: " + (", ".join(item["misplaced_candidates"]) or "none"))
            print()

    if args.strict and violations:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
