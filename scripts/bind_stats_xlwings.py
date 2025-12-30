import argparse
from typing import Dict, List, Optional

import xlwings as xw  # type: ignore


MEASURABLES = [
    ("Height", "Height"),
    ("Weight", "Weight"),
    ("Reach", "Reach"),
    ("Stance", "Stance"),
    ("Record", "Record"),
]


def col_letter(n: int) -> str:
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def read_headers(sheet: xw.Sheet) -> List[str]:
    used = sheet.used_range
    values = used.value
    if values is None:
        return []
    if not isinstance(values, list) or (values and not isinstance(values[0], list)):
        values = [values]
    if len(values) == 0:
        return []
    raw_headers = values[0]
    if not isinstance(raw_headers, list):
        raw_headers = [raw_headers]
    headers: List[str] = []
    for i, h in enumerate(raw_headers, start=1):
        name = (str(h).strip() if h is not None else f"Column{i}")
        headers.append(name)
    return headers


def find_col(headers: List[str], key: str) -> Optional[int]:
    k = key.strip().lower()
    for i, h in enumerate(headers, start=1):
        if (h or "").strip().lower() == k:
            return i
    return None


def make_index_formula(sheet_name: str, value_col: int, name_col: int) -> str:
    val_letter = col_letter(value_col)
    name_letter = col_letter(name_col)
    return (
        f"=IFERROR(INDEX('{sheet_name}'!${val_letter}:${val_letter}, "
        f"MATCH($C$2, '{sheet_name}'!${name_letter}:${name_letter}, 0)), \"\")"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Bind stats via xlwings (COM): measurables from Profiles, striking from FightsStats")
    ap.add_argument("--workbook", required=True)
    ap.add_argument("--profiles-sheet", default="Profiles")
    ap.add_argument("--stats-sheet", default=None, help="Stats sheet (e.g., FightsStats)")
    args = ap.parse_args()

    app = None
    wb = None
    try:
        app = xw.App(visible=False, add_book=False)
        app.api.DisplayAlerts = False
        wb = app.books.open(args.workbook)

        if args.profiles_sheet not in [s.name for s in wb.sheets]:
            raise SystemExit(f"Sheet not found: {args.profiles_sheet}")
        profiles = wb.sheets[args.profiles_sheet]

        stats_sheet_name = args.stats_sheet or args.profiles_sheet
        if stats_sheet_name not in [s.name for s in wb.sheets]:
            raise SystemExit(f"Sheet not found: {stats_sheet_name}")
        stats = wb.sheets[stats_sheet_name]

        dash = None
        for s in wb.sheets:
            if s.name == "Dashboard":
                dash = s
                break
        if dash is None:
            dash = wb.sheets.add("Dashboard")

        hdr_profiles = read_headers(profiles)
        hdr_stats = read_headers(stats)

        # Fighter name indices
        fighter_idx_profiles: Optional[int] = None
        for key in ["Profile", "profile", "Name", "Fighter"]:
            fighter_idx_profiles = find_col(hdr_profiles, key)
            if fighter_idx_profiles:
                break

        fighter_idx_stats: Optional[int] = None
        for key in ["Profile", "profile", "Name", "Fighter"]:
            fighter_idx_stats = find_col(hdr_stats, key)
            if fighter_idx_stats:
                break

        if not fighter_idx_profiles and not fighter_idx_stats:
            raise SystemExit("Neither stats nor profiles sheet has a Profile/Name/Fighter column")

        # Column maps
        profiles_colmap: Dict[str, int] = {}
        for name in hdr_profiles:
            if name:
                profiles_colmap[name] = hdr_profiles.index(name) + 1
        stats_colmap: Dict[str, int] = {}
        for name in hdr_stats:
            if name:
                stats_colmap[name] = hdr_stats.index(name) + 1

        # Connector overrides and dynamic striking keys
        connector_overrides: Dict[str, Dict[str, int]] = {}
        connector_sheets_for_stat: Dict[str, str] = {}
        dynamic_strike_keys: List[str] = []
        if "Connector" in [s.name for s in wb.sheets]:
            conn = wb.sheets["Connector"]
            values = conn.range("A1").expand().value or []
            if values and isinstance(values, list):
                for row in values[1:]:
                    if not row or not isinstance(row, list):
                        continue
                    role = str(row[0]).strip() if row[0] is not None else ""
                    sheet_name = str(row[1]).strip() if row[1] is not None else ""
                    found = str(row[3]).strip() if row[3] is not None else ""
                    col_text = str(row[4]).strip() if row[4] is not None else ""
                    status = str(row[5]).strip().upper() if row[5] is not None else ""
                    if not role.startswith("stat:"):
                        continue
                    key = role.split(":", 1)[1]
                    # striking keys: prefer stats sheet entries
                    if sheet_name == stats_sheet_name and key not in dynamic_strike_keys:
                        dynamic_strike_keys.append(key)
                    # overrides
                    if status == "OK" and sheet_name:
                        col_index: Optional[int] = None
                        try:
                            if col_text:
                                col_index = int(col_text)
                        except Exception:
                            col_index = None
                        if not col_index and found:
                            # resolve against that sheet's headers
                            hdr = hdr_stats if sheet_name == stats_sheet_name else hdr_profiles
                            col_index = find_col(hdr, found)
                        if col_index:
                            if sheet_name not in connector_overrides:
                                connector_overrides[sheet_name] = {}
                            connector_overrides[sheet_name][key] = col_index
                            connector_sheets_for_stat[key] = sheet_name

        # fallback: any stat:* rows
        if not dynamic_strike_keys and "Connector" in [s.name for s in wb.sheets]:
            conn = wb.sheets["Connector"]
            values = conn.range("A1").expand().value or []
            for row in values[1:]:
                if not row or not isinstance(row, list):
                    continue
                role = str(row[0]).strip() if row[0] is not None else ""
                if role.startswith("stat:"):
                    key = role.split(":", 1)[1]
                    if key not in dynamic_strike_keys:
                        dynamic_strike_keys.append(key)

        # Layout Selected Fighter and sections
        dash.range("E1").value = "Selected Fighter"
        dash.range("E2").formula = "=" + "C2"

        # Measurables from Profiles only
        dash.range("D3").value = "MEASURABLES"
        r = 4
        for label, key in MEASURABLES:
            dash.range(f"D{r}").value = label
            if fighter_idx_profiles and key in profiles_colmap:
                dash.range(f"E{r}").formula = make_index_formula(args.profiles_sheet, profiles_colmap[key], fighter_idx_profiles)
            r += 1

        # Striking dynamic
        r += 1
        dash.range(f"D{r-1}").value = "STRIKING"
        for key in dynamic_strike_keys:
            dash.range(f"D{r}").value = key
            # connector override preference
            if key in connector_sheets_for_stat:
                sheet_for_key = connector_sheets_for_stat[key]
                hdr = hdr_stats if sheet_for_key == stats_sheet_name else hdr_profiles
                name_idx = fighter_idx_stats if sheet_for_key == stats_sheet_name else fighter_idx_profiles
                col_idx = connector_overrides.get(sheet_for_key, {}).get(key)
                if name_idx and col_idx:
                    dash.range(f"E{r}").formula = make_index_formula(sheet_for_key, col_idx, name_idx)
            elif fighter_idx_stats and key in stats_colmap:
                dash.range(f"E{r}").formula = make_index_formula(stats_sheet_name, stats_colmap[key], fighter_idx_stats)
            elif fighter_idx_profiles and key in profiles_colmap:
                dash.range(f"E{r}").formula = make_index_formula(args.profiles_sheet, profiles_colmap[key], fighter_idx_profiles)
            r += 1

        wb.save()
        print("Bound measurables (Profiles) and striking (FightsStats) via xlwings.")
    finally:
        try:
            if wb is not None:
                wb.close()
        finally:
            if app is not None:
                app.quit()


if __name__ == "__main__":
    main()


