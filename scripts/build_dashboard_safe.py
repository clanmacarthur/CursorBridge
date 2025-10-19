import argparse
import subprocess
import sys
from pathlib import Path


def ensure_openpyxl() -> None:
    try:
        import openpyxl  # type: ignore
        return
    except Exception:
        pass
    print("Installing openpyxl ...")
    r = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "openpyxl"], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        sys.exit(r.returncode)
    try:
        import openpyxl  # type: ignore  # noqa: F401
    except Exception as ex:  # pragma: no cover
        print("Failed to import openpyxl after install:", ex)
        sys.exit(1)


def run_step(cmd: list[str], title: str) -> None:
    print(f"\n== {title} ==")
    print(" ", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stdout:
        print(r.stdout.strip())
    if r.returncode != 0:
        if r.stderr:
            print(r.stderr.strip())
        sys.exit(r.returncode)


def main() -> None:
    ap = argparse.ArgumentParser(description="One-shot safe dashboard builder: connector -> dropdowns -> stats -> charts")
    ap.add_argument("--workbook", required=True, help="Path to .xlsm/.xlsx workbook (Excel must be closed)")
    ap.add_argument("--events-sheet", default="Events")
    ap.add_argument("--profiles-sheet", default="Profiles")
    ap.add_argument("--stats-sheet", default="FightsStats", help="Preferred stats sheet; falls back to Profiles")
    ap.add_argument("--no-charts", action="store_true", help="Skip adding striking charts")
    ap.add_argument("--save-as", default=None, help="Optional: save a safe .xlsx copy to this path after building")
    args = ap.parse_args()

    wb_path = Path(args.workbook)
    if not wb_path.exists():
        sys.exit(f"Workbook not found: {wb_path}")

    ensure_openpyxl()

    # 1) Connector (uses stats sheet first, with fuzzy matching)
    run_step(
        [
            sys.executable,
            "scripts/add_connector.py",
            "--workbook",
            str(wb_path),
            "--events-sheet",
            args.events_sheet,
            "--profiles-sheet",
            args.profiles_sheet,
            "--stats-sheet",
            args.stats_sheet,
        ],
        "Generate Connector",
    )

    # 2) Dropdowns (Event B2 -> Fighter C2)
    run_step(
        [
            sys.executable,
            "scripts/cascade_dropdowns.py",
            "--workbook",
            str(wb_path),
            "--events-sheet",
            args.events_sheet,
            "--profiles-sheet",
            args.profiles_sheet,
        ],
        "Rebuild dropdowns",
    )

    # 3) Bind stats (reads Connector overrides; prefers stats sheet)
    run_step(
        [
            sys.executable,
            "scripts/bind_stats.py",
            "--workbook",
            str(wb_path),
            "--profiles-sheet",
            args.profiles_sheet,
            "--stats-sheet",
            args.stats_sheet,
        ],
        "Bind stats",
    )

    # 4) Charts (optional)
    if not args.no_charts:
        run_step(
            [
                sys.executable,
                "scripts/add_striking_charts.py",
                "--workbook",
                str(wb_path),
                "--profiles-sheet",
                args.profiles_sheet,
            ],
            "Add striking charts",
        )

    # Optional: save a clean .xlsx copy to avoid Excel auto-repair erasing validation
    if args.save_as:
        from openpyxl import load_workbook  # type: ignore

        print(f"\n== Save-as ==\n  {args.save_as}")
        wb = load_workbook(str(wb_path), keep_vba=False, data_only=False)
        wb.save(args.save_as)
        print("Saved safe .xlsx copy.")

    print("\nAll done. Open the workbook and check Dashboard B2/C2 and stats in column E.")


if __name__ == "__main__":
    main()


