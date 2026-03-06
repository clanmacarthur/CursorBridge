"""
Run Convex table imports from the prepared convex_seed manifest.

Default mode prints commands only (safe).
Use --execute to actually run imports.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
LATEST_PATH = ROOT / "exports" / "convex_stage_seed" / "LATEST.txt"
DEFAULT_WORKSPACE = Path(r"C:\code\Regenerative-Hive-Mind")


def load_latest_export_dir() -> Path:
    if not LATEST_PATH.exists():
        raise RuntimeError(f"Missing export pointer: {LATEST_PATH}")
    out = Path(LATEST_PATH.read_text(encoding="utf-8").strip())
    if not out.exists():
        raise RuntimeError(f"Latest export path does not exist: {out}")
    return out


def load_convex_manifest(latest_dir: Path) -> Dict[str, Any]:
    manifest = latest_dir / "convex_seed" / "manifest_convex.json"
    if not manifest.exists():
        raise RuntimeError(f"Missing convex seed manifest: {manifest}")
    return json.loads(manifest.read_text(encoding="utf-8"))


def build_cmd(
    workspace: Path,
    collection: str,
    file_path: Path,
    deployment_name: str | None,
    prod: bool,
) -> List[str]:
    cmd = [
        "npx.cmd",
        "convex",
        "import",
        "--table",
        collection,
        str(file_path),
        "--format",
        "jsonArray",
        "--append",
        "--yes",
    ]
    if deployment_name:
        cmd.extend(["--deployment-name", deployment_name])
    if prod:
        cmd.append("--prod")
    return cmd


def main() -> None:
    parser = argparse.ArgumentParser(description="Import prepared convex_seed files using Convex CLI")
    parser.add_argument(
        "--workspace",
        default=str(DEFAULT_WORKSPACE),
        help="Workspace that contains Convex project config (default: external workspace)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually run imports. Without this flag, commands are only printed.",
    )
    parser.add_argument("--deployment-name", help="Optional Convex deployment name")
    parser.add_argument("--prod", action="store_true", help="Import into production deployment")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        raise RuntimeError(f"Workspace does not exist: {workspace}")

    latest_dir = load_latest_export_dir()
    manifest = load_convex_manifest(latest_dir)
    rows = manifest.get("collections", [])
    if not isinstance(rows, list) or not rows:
        raise RuntimeError("Convex seed manifest has no collections")

    print(f"Workspace: {workspace}")
    print(f"Source export: {latest_dir}")
    print(f"Execute mode: {args.execute}")
    print("")

    failures = 0
    for row in rows:
        collection = str(row.get("collection", "")).strip()
        rel = str(row.get("file", "")).strip()
        if not collection or not rel:
            failures += 1
            print(f"[SKIP] Bad manifest row: {row}")
            continue
        path = latest_dir / "convex_seed" / rel
        if not path.exists():
            failures += 1
            print(f"[SKIP] Missing file for {collection}: {path}")
            continue

        cmd = build_cmd(
            workspace=workspace,
            collection=collection,
            file_path=path,
            deployment_name=args.deployment_name,
            prod=args.prod,
        )
        print("[CMD]", " ".join(cmd))
        if args.execute:
            proc = subprocess.run(cmd, cwd=str(workspace), check=False)
            if proc.returncode != 0:
                failures += 1
                print(f"[FAIL] {collection} import failed")
            else:
                print(f"[OK] {collection} imported")

    print("")
    if failures:
        print(f"Completed with failures: {failures}")
        raise SystemExit(1)
    print("Completed successfully.")


if __name__ == "__main__":
    main()
