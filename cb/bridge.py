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


def _read_sheet_headers_and_rows(workbook_path: str, sheet: str) -> Tuple[List[str], List[Dict[str, str]]]:
    """Read headers and rows from an Excel sheet.

    Strategy:
    1) Try fast path via PowerShell SaveAs CSV
    2) Fallback to xlwings COM if CSV export fails
    """
    # Attempt PowerShell CSV export first
    try:
        with tempfile.TemporaryDirectory() as td:
            csv_path = os.path.join(td, "export.csv")
            _export_sheet_to_csv_via_powershell(workbook_path, sheet, csv_path)
            return _read_csv_dicts(csv_path)
    except subprocess.CalledProcessError:
        pass  # Fallback to xlwings below

    # Fallback: read via xlwings COM directly (no extra dependency, xlwings is included)
    try:
        import xlwings as xw
    except Exception as e:  # pragma: no cover - defensive: xlwings should be installed per pyproject
        raise RuntimeError("xlwings import failed; cannot read workbook without PowerShell CSV export") from e

    app = None
    wb = None
    try:
        app = xw.App(visible=False, add_book=False)
        # Suppress alerts to avoid prompts on open
        app.api.DisplayAlerts = False
        wb = app.books.open(workbook_path)
        # Resolve sheet by name or index (1-based if numeric input)
        target_sheet = None
        if str(sheet).strip().isdigit():
            idx = int(str(sheet).strip()) - 1
            target_sheet = wb.sheets[idx]
        else:
            target_sheet = wb.sheets[str(sheet)]

        used = target_sheet.used_range
        values = used.value
        if values is None:
            return [], []
        # Normalize to 2D array
        if not isinstance(values, list) or (values and not isinstance(values[0], list)):
            values = [values]  # single row or single cell

        if len(values) == 0:
            return [], []

        # First row = headers
        raw_headers = values[0]
        if not isinstance(raw_headers, list):
            raw_headers = [raw_headers]
        headers: List[str] = []
        for i, h in enumerate(raw_headers, start=1):
            name = (str(h).strip() if h is not None else f"Column{i}")
            headers.append(name)

        # Remaining rows
        rows: List[Dict[str, str]] = []
        for r in values[1:]:
            if not isinstance(r, list):
                r = [r]
            # Pad row to headers length
            if len(r) < len(headers):
                r = r + [None] * (len(headers) - len(r))
            # Trim extra cells beyond headers
            if len(r) > len(headers):
                r = r[: len(headers)]
            # Skip completely empty rows
            if not any((str(c).strip() if c is not None else "") for c in r):
                continue
            row_dict: Dict[str, str] = {}
            for h, c in zip(headers, r):
                row_dict[h] = (str(c).strip() if c is not None else "")
            rows.append(row_dict)

        return headers, rows
    finally:
        try:
            if wb is not None:
                wb.close()
        finally:
            if app is not None:
                app.quit()


def excel_to_notion(
    workbook_path: str,
    sheet: str,
    database_id: str,
    header_to_notion: Dict[str, str] | None = None,
    max_rows: int | None = None,
    dry_run: bool = False,
) -> Dict[str, int]:
    header_to_notion = header_to_notion or {}
    headers, rows = _read_sheet_headers_and_rows(workbook_path, sheet)

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
    headers, rows = _read_sheet_headers_and_rows(workbook_path, sheet)
    return {
        "headers": headers,
        "rows": rows[:max_rows],
        "total_rows": len(rows),
    }


