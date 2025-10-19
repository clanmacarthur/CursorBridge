import argparse
from typing import Dict, List, Optional, Tuple

from openpyxl import load_workbook  # type: ignore


ROLES = [
    ("event_key", "Events", ["EventId", "Event ID", "EventID", "Event Id", "eventId"]),
    ("event_display", "Events", ["Event", "Card", "EventName", "Name", "Card Name", "Event Name"]),
    ("fighter_name", "Profiles", ["Profile", "profile", "Name", "Fighter"]),
]

# Stats we bind
STAT_KEYS = [
    "Height", "Weight", "Reach", "Stance", "Record",
    "TSSL", "TSSA", "STRACC%", "SSL/M", "SSA/M", "DSL/M", "DSA/M", "KD/15mins",
]


def headers_of(ws) -> List[str]:
    return [str(c.value).strip() if c.value is not None else "" for c in ws[1]]


def detect_header(headers: List[str], candidates: List[str]) -> Tuple[str, int]:
    lower = {(h or "").strip().lower(): (h, i) for i, h in enumerate(headers, start=1)}
    for cand in candidates:
        r = lower.get(cand.strip().lower())
        if r:
            return r[0], r[1]
    return "", 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Create Connector sheet showing column mappings")
    ap.add_argument("--workbook", required=True)
    ap.add_argument("--events-sheet", default="Events")
    ap.add_argument("--profiles-sheet", default="Profiles")
    args = ap.parse_args()

    wb = load_workbook(args.workbook, keep_vba=True, data_only=False)

    if args.events_sheet not in wb.sheetnames:
        raise SystemExit(f"Sheet not found: {args.events_sheet}")
    if args.profiles_sheet not in wb.sheetnames:
        raise SystemExit(f"Sheet not found: {args.profiles_sheet}")

    ws_events = wb[args.events_sheet]
    ws_profiles = wb[args.profiles_sheet]

    ev_hdr = headers_of(ws_events)
    pf_hdr = headers_of(ws_profiles)

    rows: List[List[str]] = []
    # Core roles
    for role, sheet, candidates in ROLES:
        hdr_list = ev_hdr if sheet == args.events_sheet else pf_hdr
        found_name, col_idx = detect_header(hdr_list, candidates)
        rows.append([role, sheet, ", ".join(candidates), found_name or "", str(col_idx or ""), "OK" if col_idx else "MISSING"])

    # Stats
    for key in STAT_KEYS:
        found_name, col_idx = detect_header(pf_hdr, [key])
        rows.append([f"stat:{key}", args.profiles_sheet, key, found_name or "", str(col_idx or ""), "OK" if col_idx else "MISSING"])

    # Create/replace Connector sheet
    if "Connector" in wb.sheetnames:
        wb.remove(wb["Connector"])
    ws = wb.create_sheet("Connector")
    ws["A1"], ws["B1"], ws["C1"], ws["D1"], ws["E1"], ws["F1"] = (
        "role", "sheet", "expected", "found", "col", "status"
    )
    for i, r in enumerate(rows, start=2):
        for j, v in enumerate(r, start=1):
            ws.cell(row=i, column=j, value=v)

    wb.save(args.workbook)
    print(f"Connector sheet created with {len(rows)} rows.")


if __name__ == "__main__":
    main()


