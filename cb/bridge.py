import csv
import os
import subprocess
import tempfile
from typing import Dict, List, Tuple

from .notion import create_database_row
import yaml


def _export_sheet_to_csv_via_powershell(workbook_path: str, sheet: str, out_csv_path: str) -> None:
    ps = f"$ErrorActionPreference='Stop';$path='{workbook_path}';$csv='{out_csv_path}';$s='{sheet}';"
    ps += (
        "$excel=New-Object -ComObject Excel.Application;"
        "$excel.Visible=$false;"
        "$wb=$excel.Workbooks.Open($path);"
        "if ($s -match '^[0-9]+$') { $ws=$wb.Worksheets.Item([int]$s) } else { $ws=$wb.Worksheets.Item($s) };"
        "$xlCSV=6;"
        "$ws.SaveAs($csv, $xlCSV);"
        "$wb.Close($false);$excel.Quit();"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _read_csv_dicts(csv_path: str) -> Tuple[List[str], List[Dict[str, str]]]:
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = [row for row in reader]
    return headers, rows


def excel_to_notion(
    workbook_path: str,
    sheet: str,
    database_id: str,
    header_to_notion: Dict[str, str] | None = None,
    max_rows: int | None = None,
    dry_run: bool = False,
) -> Dict[str, int]:
    header_to_notion = header_to_notion or {}
    with tempfile.TemporaryDirectory() as td:
        csv_path = os.path.join(td, "export.csv")
        _export_sheet_to_csv_via_powershell(workbook_path, sheet, csv_path)
        headers, rows = _read_csv_dicts(csv_path)

    created = 0
    skipped = 0
    for i, row in enumerate(rows, start=1):
        if max_rows is not None and created >= max_rows:
            break
        # Skip completely empty rows
        if not any((row.get(h) or "").strip() for h in headers):
            skipped += 1
            continue

        # Build properties mapping
        props: Dict[str, str] = {}
        for h in headers:
            val = (row.get(h) or "").strip()
            if not val:
                continue
            notion_name = header_to_notion.get(h, h)
            props[notion_name] = val

        # Ensure Name exists (Notion title)
        if "Name" not in props:
            # Use the first non-empty header's value as a fallback
            for h in headers:
                v = (row.get(h) or "").strip()
                if v:
                    props["Name"] = v
                    break
        if "Name" not in props:
            skipped += 1
            continue

        if dry_run:
            created += 1
            continue
        else:
            create_database_row(database_id, props)
            created += 1

    return {"created": created, "skipped": skipped}


def excel_to_notion_from_profile(profile: str, max_rows: int | None = None, dry_run: bool = False) -> Dict[str, int]:
    config_path = os.path.join(os.getcwd(), "config", "bridge.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Missing config: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    profiles = (cfg or {}).get("profiles", {})
    if profile not in profiles:
        raise KeyError(f"Profile '{profile}' not found in config/bridge.yaml")
    p = profiles[profile]
    mapping = p.get("map", {})
    return excel_to_notion(
        workbook_path=p["workbook"],
        sheet=str(p["sheet"]),
        database_id=p["database_id"],
        header_to_notion=mapping,
        max_rows=max_rows,
        dry_run=dry_run,
    )


def excel_preview(workbook_path: str, sheet: str, max_rows: int = 5) -> Dict[str, object]:
    with tempfile.TemporaryDirectory() as td:
        csv_path = os.path.join(td, "export.csv")
        _export_sheet_to_csv_via_powershell(workbook_path, sheet, csv_path)
        headers, rows = _read_csv_dicts(csv_path)
    return {
        "headers": headers,
        "rows": rows[:max_rows],
        "total_rows": len(rows),
    }


