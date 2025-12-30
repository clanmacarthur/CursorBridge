import argparse
import difflib
from typing import List, Tuple

import xlwings as xw  # type: ignore


def detect_header(headers: List[str], candidates: List[str]) -> Tuple[str, int]:
    lower = {(h or "").strip().lower(): (h, i) for i, h in enumerate(headers, start=1)}
    for cand in candidates:
        r = lower.get(cand.strip().lower())
        if r:
            return r[0], r[1]
    return "", 0


def fuzzy_match_header(headers: List[str], target: str, threshold: float = 0.77) -> Tuple[str, int, float]:
    best_score = 0.0
    best_name = ""
    best_idx = 0
    for i, h in enumerate(headers, start=1):
        if not h:
            continue
        score = difflib.SequenceMatcher(None, h.strip().lower(), target.strip().lower()).ratio()
        if score > best_score:
            best_score = score
            best_name = h
            best_idx = i
    if best_score >= threshold:
        return best_name, best_idx, best_score
    return "", 0, 0.0


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


def main() -> None:
    ap = argparse.ArgumentParser(description="Create Connector sheet via xlwings (COM) with FightsStats-only striking and Profiles measurables")
    ap.add_argument("--workbook", required=True)
    ap.add_argument("--events-sheet", default="Events")
    ap.add_argument("--profiles-sheet", default="Profiles")
    ap.add_argument("--stats-sheet", default=None, help="Stats sheet (e.g., FightsStats)")
    args = ap.parse_args()

    app = None
    wb = None
    try:
        app = xw.App(visible=False, add_book=False)
        app.api.DisplayAlerts = False
        wb = app.books.open(args.workbook)

        if args.events_sheet not in [s.name for s in wb.sheets]:
            raise SystemExit(f"Sheet not found: {args.events_sheet}")
        if args.profiles_sheet not in [s.name for s in wb.sheets]:
            raise SystemExit(f"Sheet not found: {args.profiles_sheet}")

        stats_sheet_name = args.stats_sheet or args.profiles_sheet
        if stats_sheet_name not in [s.name for s in wb.sheets]:
            raise SystemExit(f"Sheet not found: {stats_sheet_name}")

        ws_events = wb.sheets[args.events_sheet]
        ws_profiles = wb.sheets[args.profiles_sheet]
        ws_stats = wb.sheets[stats_sheet_name]

        ev_hdr = read_headers(ws_events)
        pf_hdr = read_headers(ws_profiles)
        st_hdr = read_headers(ws_stats)

        # Build rows
        rows: List[List[str]] = []
        # Core roles
        ROLES = [
            ("event_key", args.events_sheet, ["EventId", "Event ID", "EventID", "Event Id", "eventId"]),
            (
                "event_display",
                args.events_sheet,
                [
                    "Event",
                    "Card",
                    "EventName",
                    "Name",
                    "Card Name",
                    "Event Name",
                    "Column3",
                    "Column 3",
                    "Card Events",
                    "Card events",
                    "Card Event",
                    "Card event",
                ],
            ),
            ("fighter_name", args.profiles_sheet, ["Profile", "profile", "Name", "Fighter"]),
        ]

        for role, sheet_name, candidates in ROLES:
            hdr_list = ev_hdr if sheet_name == args.events_sheet else pf_hdr
            found_name, col_idx = detect_header(hdr_list, candidates)
            note = "EXACT" if col_idx else ""
            if not col_idx and candidates:
                f_name, f_idx, score = fuzzy_match_header(hdr_list, candidates[0])
                if f_idx:
                    found_name, col_idx = f_name, f_idx
                    note = f"FUZZY:{score:.2f}"
            rows.append([role, sheet_name, ", ".join(candidates), found_name or "", str(col_idx or ""), "OK" if col_idx else "MISSING", note])

        # Measurables: Profiles only
        MEAS_KEYS = ["Height", "Weight", "Reach", "Stance", "Record"]
        for key in MEAS_KEYS:
            used_sheet = args.profiles_sheet
            found_name, col_idx = detect_header(pf_hdr, [key])
            note = "EXACT" if col_idx else ""
            if not col_idx:
                f_name, f_idx, score = fuzzy_match_header(pf_hdr, key)
                if f_idx:
                    found_name, col_idx = f_name, f_idx
                    note = f"FUZZY:{score:.2f}"
            rows.append([f"stat:{key}", used_sheet, key, found_name or "", str(col_idx or ""), "OK" if col_idx else "MISSING", note])

        # Striking: derive directly from stats sheet headers
        ignore_names = {"profile", "name", "fighter", "eventid", "event id", "event", "card", "card name", "event name", "column3", "column 3"}
        # figure out fighter name column to ignore
        name_idx_stats = 0
        for cand in ["Profile", "profile", "Name", "Fighter"]:
            _, idx = detect_header(st_hdr, [cand])
            if idx:
                name_idx_stats = idx
                break
        for i, h in enumerate(st_hdr, start=1):
            if not h:
                continue
            if i == name_idx_stats:
                continue
            if h.strip().lower() in ignore_names:
                continue
            rows.append([f"stat:{h}", stats_sheet_name, h, h, str(i), "OK", "EXACT"])

        # Write Connector sheet via xlwings
        # Remove if exists
        for s in wb.sheets:
            if s.name == "Connector":
                s.delete()
                break
        ws_conn = wb.sheets.add("Connector")
        headers = ["role", "sheet", "expected", "found", "col", "status", "note"]
        data = [headers] + rows
        ws_conn.range("A1").value = data
        wb.save()
        print(f"Connector sheet created with {len(rows)} rows via xlwings.")
    finally:
        try:
            if wb is not None:
                wb.close()
        finally:
            if app is not None:
                app.quit()


if __name__ == "__main__":
    main()



