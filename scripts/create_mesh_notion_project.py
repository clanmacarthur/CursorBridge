"""
Create a Notion project page from task-manager/docs/mesh package.

Default behavior:
- Reads package from C:/code/task-manager/docs/mesh/MESH_NOTION_PROJECT_PACKAGE.json
- Creates a parent "Mesh Master Project - Unified Adaptive Engine" page under
  the existing root project page from docs/_notion_project_creation_result.json
- Creates child pages per section
- Loads each section markdown into simple Notion blocks
- Writes result to docs/_mesh_notion_project_result.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests


ROOT = Path(__file__).resolve().parents[1]
TASK_MANAGER_MESH_DIR = Path(r"C:\code\task-manager\docs\mesh")
DEFAULT_PACKAGE = TASK_MANAGER_MESH_DIR / "MESH_NOTION_PROJECT_PACKAGE.json"
PROJECT_RESULT = ROOT / "docs" / "_notion_project_creation_result.json"
OUTPUT_RESULT = ROOT / "docs" / "_mesh_notion_project_result.json"
ENV_PATH = ROOT / ".env"
NOTION_VERSION = "2022-06-28"


def load_notion_token() -> str:
    token = os.getenv("NOTION_TOKEN", "").strip()
    if token:
        return token
    if not ENV_PATH.exists():
        return ""
    for raw in ENV_PATH.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip().lstrip("\ufeff") == "NOTION_TOKEN":
            return value.strip()
    return ""


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def extract_root_project_page_id() -> str:
    data = read_json(PROJECT_RESULT)
    root = data.get("root_project_row", {})
    page_id = str(root.get("id", "")).strip()
    if not page_id:
        raise RuntimeError("root_project_row.id missing in docs/_notion_project_creation_result.json")
    return page_id


def chunk_text(text: str, limit: int = 1800) -> List[str]:
    cleaned = text.strip()
    if not cleaned:
        return []
    chunks: List[str] = []
    current = ""
    for line in cleaned.splitlines():
        line = line.rstrip()
        if not line:
            line = " "
        if len(current) + len(line) + 1 <= limit:
            current = f"{current}\n{line}".strip("\n")
        else:
            chunks.append(current)
            current = line
    if current:
        chunks.append(current)
    return chunks


def make_rich_text(text: str) -> List[Dict[str, Any]]:
    return [{"type": "text", "text": {"content": text[:2000]}}]


def markdown_to_blocks(markdown: str) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    in_code = False
    code_lines: List[str] = []
    code_lang = "plain text"

    def flush_code() -> None:
        nonlocal code_lines, in_code, code_lang
        if not code_lines:
            in_code = False
            return
        code_text = "\n".join(code_lines).strip()
        for chunk in chunk_text(code_text, limit=1800):
            blocks.append(
                {
                    "object": "block",
                    "type": "code",
                    "code": {"rich_text": make_rich_text(chunk), "language": code_lang},
                }
            )
        code_lines = []
        in_code = False
        code_lang = "plain text"

    for raw in markdown.splitlines():
        line = raw.rstrip()

        if line.strip().startswith("```"):
            marker = line.strip().replace("`", "").strip().lower()
            if in_code:
                flush_code()
            else:
                in_code = True
                code_lang = "plain text"
                if marker:
                    code_lang = marker if marker in {
                        "plain text",
                        "typescript",
                        "javascript",
                        "python",
                        "sql",
                        "json",
                        "bash",
                        "markdown",
                    } else "plain text"
            continue

        if in_code:
            code_lines.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("### "):
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {"rich_text": make_rich_text(stripped[4:])},
                }
            )
            continue
        if stripped.startswith("## "):
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": make_rich_text(stripped[3:])},
                }
            )
            continue
        if stripped.startswith("# "):
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {"rich_text": make_rich_text(stripped[2:])},
                }
            )
            continue
        if stripped.startswith("- "):
            blocks.append(
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": make_rich_text(stripped[2:])},
                }
            )
            continue
        if stripped.startswith("|"):
            # Keep markdown tables readable in Notion as code blocks.
            blocks.append(
                {
                    "object": "block",
                    "type": "code",
                    "code": {"rich_text": make_rich_text(stripped), "language": "plain text"},
                }
            )
            continue

        for chunk in chunk_text(stripped):
            blocks.append(
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": make_rich_text(chunk)},
                }
            )

    if in_code:
        flush_code()

    return blocks


class Notion:
    def __init__(self, token: str, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.base = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def _request(
        self, method: str, path: str, *, json_body: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if self.dry_run:
            return {}
        resp = requests.request(
            method,
            f"{self.base}{path}",
            headers=self.headers,
            json=json_body,
            timeout=60,
        )
        if resp.status_code >= 300:
            raise RuntimeError(f"{method} {path} failed ({resp.status_code}): {resp.text}")
        if not resp.text:
            return {}
        return resp.json()

    def verify(self) -> None:
        self._request("GET", "/users/me")

    def create_page(self, parent_page_id: str, title: str) -> Dict[str, Any]:
        if self.dry_run:
            return {
                "id": f"dry-run-{title.lower().replace(' ', '-')}",
                "url": f"https://www.notion.so/{title.lower().replace(' ', '-')}",
            }
        payload = {
            "parent": {"page_id": parent_page_id},
            "properties": {
                "title": {"title": [{"type": "text", "text": {"content": title[:2000]}}]}
            },
        }
        return self._request("POST", "/pages", json_body=payload)

    def append_children(self, page_id: str, blocks: List[Dict[str, Any]]) -> None:
        if self.dry_run or not blocks:
            return
        start = 0
        while start < len(blocks):
            chunk = blocks[start : start + 80]
            self._request("PATCH", f"/blocks/{page_id}/children", json_body={"children": chunk})
            start += 80


def load_package(package_path: Path) -> Dict[str, Any]:
    if not package_path.exists():
        raise RuntimeError(f"Package file not found: {package_path}")
    return read_json(package_path)


def section_markdown(mesh_dir: Path, file_name: str) -> str:
    path = mesh_dir / file_name
    if not path.exists():
        return f"# Missing Source\n\nCould not find `{file_name}`."
    return path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Mesh Notion project from docs package.")
    parser.add_argument("--package", default=str(DEFAULT_PACKAGE), help="Path to package JSON")
    parser.add_argument(
        "--parent-page-id",
        default="",
        help="Optional Notion parent page id. Defaults to root project page id.",
    )
    parser.add_argument("--dry-run", action="store_true", help="No Notion writes")
    args = parser.parse_args()

    token = load_notion_token()
    if not token:
        raise RuntimeError("NOTION_TOKEN missing in root .env")

    package_path = Path(args.package)
    package = load_package(package_path)
    mesh_dir = package_path.parent

    parent_page_id = args.parent_page_id.strip() or extract_root_project_page_id()
    project_title = str(package.get("project_title") or "Mesh Master Project").strip()
    version = str(package.get("version") or "1.0.0").strip()

    notion = Notion(token=token, dry_run=args.dry_run)
    notion.verify()

    stamp = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    main_page_title = f"{project_title} ({stamp})"
    main_page = notion.create_page(parent_page_id, main_page_title)
    main_page_id = str(main_page.get("id", ""))

    intro_blocks = markdown_to_blocks(
        f"# {project_title}\n\nVersion: {version}\n\nGenerated from `{package_path}`."
    )
    notion.append_children(main_page_id, intro_blocks)

    section_results: List[Dict[str, Any]] = []
    for section in package.get("sections", []):
        title = str(section.get("title", "Untitled Section")).strip()
        source = str(section.get("source", "")).strip()
        child = notion.create_page(main_page_id, title)
        child_id = str(child.get("id", ""))
        child_url = str(child.get("url", ""))
        md = section_markdown(mesh_dir, source)
        blocks = markdown_to_blocks(md)
        notion.append_children(child_id, blocks)
        section_results.append(
            {"title": title, "source": source, "id": child_id, "url": child_url}
        )

    result = {
        "generated_at_utc": dt.datetime.now(dt.UTC).isoformat(),
        "dry_run": args.dry_run,
        "parent_page_id": parent_page_id,
        "main_page": {"id": main_page.get("id", ""), "url": main_page.get("url", ""), "title": main_page_title},
        "sections": section_results,
        "package_path": str(package_path),
    }
    OUTPUT_RESULT.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"Main page: {result['main_page']['url']}")
    print(f"Sections: {len(section_results)}")
    print(f"Result file: {OUTPUT_RESULT}")


if __name__ == "__main__":
    main()
