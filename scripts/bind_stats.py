import argparse
from typing import Dict, List, Optional

from openpyxl import load_workbook  # type: ignore


MEASURABLES = [
    ("Height", "Height"),
    ("Weight", "Weight"),
    ("Reach", "Reach"),
    ("Stance", "Stance"),
    ("Record", "Record"),
]

STRIKING = [
    ("TSSL", "TSSL"),
    ("TSSA", "TSSA"),
    ("STRACC%", "STRACC%"),
    ("SSL/M", "SSL/M"),
    ("SSA/M", "SSA/M"),
    ("DSL/M", "DSL/M"),
    ("DSA/M", "DSA/M"),
    ("KD/15mins", "KD/15mins"),
]


def headers_of(ws) -> List[str]:
    return [str(c.value).strip() if c.value is not None else "" for c in ws[1]]


def find_col(headers: List[str], key: str) -> Optional[int]:
    k = key.strip().lower()
    for i, h in enumerate(headers, start=1):
        if (h or "").strip().lower() == k:
            return i
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Bind measurables and striking stats to Dashboard based on C2 selection")
    ap.add_argument("--workbook", required=True)
    ap.add_argument("--profiles-sheet", default="Profiles")
    args = ap.parse_args()

    wb = load_workbook(args.workbook, keep_vba=True, data_only=False)

    if args.profiles_sheet not in wb.sheetnames:
        raise SystemExit(f"Sheet not found: {args.profiles_sheet}")
    ws_p = wb[args.profiles_sheet]

    ws_dash = wb["Dashboard"] if "Dashboard" in wb.sheetnames else wb.create_sheet("Dashboard")

    hdr = headers_of(ws_p)
    # Required columns
    prof_idx = None
    for key in ["Profile", "profile", "Name", "Fighter"]:
        prof_idx = find_col(hdr, key)
        if prof_idx:
            break
    if not prof_idx:
        raise SystemExit("Profiles sheet missing Profile/Name/Fighter column")

    # Build a header->column map for stats we care about
    need = {k for _, k in MEASURABLES + STRIKING}
    colmap: Dict[str, int] = {}
    for name in need:
        idx = find_col(hdr, name)
        if idx:
            colmap[name] = idx

    # Layout sections on Dashboard
    ws_dash["E1"] = "Selected Fighter"
    ws_dash["E2"] = "=" + "C2"  # show selected fighter name

    start_row = 4
    ws_dash["D3"] = "MEASURABLES"
    r = start_row
    for label, key in MEASURABLES:
        ws_dash.cell(row=r, column=4, value=label)
        if key in colmap:
            # INDEX match against Profiles!Profile column using Dashboard!C2
            col_letter = ws_p.cell(row=1, column=colmap[key]).column_letter
            prof_col_letter = ws_p.cell(row=1, column=prof_idx).column_letter
            formula = f"=IFERROR(INDEX('{args.profiles_sheet}'!${col_letter}:${col_letter}, MATCH($C$2, '{args.profiles_sheet}'!${prof_col_letter}:${prof_col_letter}, 0)), \"\")"
            ws_dash.cell(row=r, column=5).value = formula
        r += 1

    r += 1
    ws_dash.cell(row=r-1, column=4, value="STRIKING")
    for label, key in STRIKING:
        ws_dash.cell(row=r, column=4, value=label)
        if key in colmap:
            col_letter = ws_p.cell(row=1, column=colmap[key]).column_letter
            prof_col_letter = ws_p.cell(row=1, column=prof_idx).column_letter
            formula = f"=IFERROR(INDEX('{args.profiles_sheet}'!${col_letter}:${col_letter}, MATCH($C$2, '{args.profiles_sheet}'!${prof_col_letter}:${prof_col_letter}, 0)), \"\")"
            ws_dash.cell(row=r, column=5).value = formula
        r += 1

    wb.save(args.workbook)
    print("Bound measurables and striking stats to Dashboard.")


if __name__ == "__main__":
    main()


