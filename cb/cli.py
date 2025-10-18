import argparse
import os
from typing import List, Optional

from . import excel as excel_mod
from . import pad as pad_mod
from . import notion as notion_mod
from .bridge import excel_to_notion
from .dashboard import build_dashboard
from dotenv import load_dotenv


def _excel_run(args: argparse.Namespace) -> None:
    if not os.path.exists(args.workbook):
        raise SystemExit(f"Workbook not found: {args.workbook}")
    if not args.macro and not args.py:
        raise SystemExit("Provide --macro or --py")
    if args.macro and args.py:
        raise SystemExit("Provide only one of --macro or --py")
    if args.macro:
        excel_mod.run_macro(args.workbook, args.macro)
    else:
        excel_mod.run_python(args.workbook, args.py)


def _pad_run(args: argparse.Namespace) -> None:
    params: dict[str, str] = {}
    for kv in args.param or []:
        if "=" not in kv:
            raise SystemExit(f"Invalid param: {kv}")
        k, v = kv.split("=", 1)
        params[k] = v
    result = pad_mod.run_flow(args.flow_name, params)
    print(result)


def _notion_edit(args: argparse.Namespace) -> None:
    prop_map: dict[str, str] = {}
    for nv in args.property or []:
        if "=" not in nv:
            raise SystemExit(f"Invalid property: {nv}")
        n, v = nv.split("=", 1)
        prop_map[n] = v
    notion_mod.edit_page(args.page_id, append_text=args.append, properties=prop_map)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cb", description="CursorBridge CLI")
    sub = parser.add_subparsers(dest="command")

    # excel
    p_excel = sub.add_parser("excel", help="Excel automation")
    sub_excel = p_excel.add_subparsers(dest="excel_command")
    p_excel_run = sub_excel.add_parser("run", help="Run Excel macro or Python task")
    p_excel_run.add_argument("--workbook", required=True, help="Path to workbook (.xlsm/.xlsx)")
    p_excel_run.add_argument("--macro", required=False, help="Macro name, e.g., Module1.DoThing")
    p_excel_run.add_argument("--py", required=False, help="Python callable, e.g., cb.excel:example_task")
    p_excel_run.set_defaults(func=_excel_run)

    p_excel_write = sub_excel.add_parser("write", help="Write a single cell using openpyxl")
    p_excel_write.add_argument("--workbook", required=True, help="Path to workbook (.xlsm/.xlsx)")
    p_excel_write.add_argument("--sheet", required=True, help="Sheet name or 1-based index")
    p_excel_write.add_argument("--cell", required=True, help="Cell address, e.g., A1")
    p_excel_write.add_argument("--value", required=True, help="Value to write")
    p_excel_write.set_defaults(func=lambda a: excel_mod.write_cell_openpyxl(a.workbook, a.sheet, a.cell, a.value))

    p_excel_append = sub_excel.add_parser("append", help="Append a row using openpyxl")
    p_excel_append.add_argument("--workbook", required=True, help="Path to workbook (.xlsm/.xlsx)")
    p_excel_append.add_argument("--sheet", required=True, help="Sheet name or 1-based index")
    p_excel_append.add_argument("--values", action="append", required=True, help="Value; repeat to add columns")
    p_excel_append.set_defaults(func=lambda a: excel_mod.append_row_openpyxl(a.workbook, a.sheet, a.values))

    # pad
    p_pad = sub.add_parser("pad", help="Power Automate Desktop via HTTP cloud flow")
    sub_pad = p_pad.add_subparsers(dest="pad_command")
    p_pad_run = sub_pad.add_parser("run", help="Run PAD flow by alias from config/flows.yaml")
    p_pad_run.add_argument("flow_name", help="Flow alias name")
    p_pad_run.add_argument("--param", action="append", default=[], help="key=value parameter, repeatable")
    p_pad_run.set_defaults(func=_pad_run)

    # notion
    p_notion = sub.add_parser("notion", help="Notion integration")
    sub_notion = p_notion.add_subparsers(dest="notion_command")
    p_notion_edit = sub_notion.add_parser("edit", help="Edit or append to a Notion page")
    p_notion_edit.add_argument("--page-id", required=True, help="Notion page ID")
    p_notion_edit.add_argument("--append", required=False, help="Append paragraph text")
    p_notion_edit.add_argument("--property", action="append", default=[], help="name=value property, repeatable")
    p_notion_edit.set_defaults(func=_notion_edit)

    p_notion_insert = sub_notion.add_parser("db-insert", help="Create a row in a Notion database")
    p_notion_insert.add_argument("--database-id", required=True, help="Notion database ID")
    p_notion_insert.add_argument("--property", action="append", default=[], help="name=value property, repeatable")
    def _notion_insert(args: argparse.Namespace) -> None:
        prop_map: dict[str, str] = {}
        for nv in args.property or []:
            if "=" not in nv:
                raise SystemExit(f"Invalid property: {nv}")
            n, v = nv.split("=", 1)
            prop_map[n] = v
        result = notion_mod.create_database_row(args.database_id, prop_map)
        print(result.get("id", "OK"))
    p_notion_insert.set_defaults(func=_notion_insert)

    # bridge
    p_bridge = sub.add_parser("bridge", help="Cross-app bridges")
    sub_bridge = p_bridge.add_subparsers(dest="bridge_command")
    p_bridge_e2n = sub_bridge.add_parser("excel-to-notion", help="Export an Excel sheet to a Notion database")
    p_bridge_e2n.add_argument("--workbook", required=True, help="Path to workbook (.xlsm/.xlsx)")
    p_bridge_e2n.add_argument("--sheet", required=True, help="Sheet name or 1-based index")
    p_bridge_e2n.add_argument("--database-id", required=True, help="Notion database ID")
    p_bridge_e2n.add_argument("--map", action="append", default=[], help="ExcelHeader=NotionProperty mapping; repeatable")
    p_bridge_e2n.add_argument("--max-rows", type=int, default=None, help="Limit number of rows to insert (default: all)")
    p_bridge_e2n.add_argument("--dry-run", action="store_true", help="Preview inserts without writing to Notion")
    def _bridge_e2n(args: argparse.Namespace) -> None:
        mapping: dict[str, str] = {}
        for m in args.map or []:
            if "=" not in m:
                raise SystemExit(f"Invalid mapping: {m}")
            k, v = m.split("=", 1)
            mapping[k] = v
        result = excel_to_notion(args.workbook, args.sheet, args.database_id, mapping, args.max_rows, args.dry_run)
        print(result)
    p_bridge_e2n.set_defaults(func=_bridge_e2n)

    p_bridge_profile = sub_bridge.add_parser("run-profile", help="Run a configured bridge profile from config/bridge.yaml")
    p_bridge_profile.add_argument("--profile", required=True, help="Profile name under profiles:")
    p_bridge_profile.add_argument("--max-rows", type=int, default=None, help="Limit number of rows to insert (default: all)")
    p_bridge_profile.add_argument("--dry-run", action="store_true", help="Preview inserts without writing to Notion")
    def _bridge_profile(args: argparse.Namespace) -> None:
        from .bridge import excel_to_notion_from_profile
        result = excel_to_notion_from_profile(args.profile, args.max_rows, args.dry_run)
        print(result)
    p_bridge_profile.set_defaults(func=_bridge_profile)

    p_bridge_prev = sub_bridge.add_parser("excel-preview", help="Preview headers and first rows from an Excel sheet")
    p_bridge_prev.add_argument("--workbook", required=True, help="Path to workbook (.xlsm/.xlsx)")
    p_bridge_prev.add_argument("--sheet", required=True, help="Sheet name or 1-based index")
    p_bridge_prev.add_argument("--max-rows", type=int, default=5, help="Rows to show (default 5)")
    def _bridge_prev(args: argparse.Namespace) -> None:
        from .bridge import excel_preview
        result = excel_preview(args.workbook, args.sheet, args.max_rows)
        print(result)
    p_bridge_prev.set_defaults(func=_bridge_prev)

    # dashboard
    p_dash = sub.add_parser("dashboard", help="Build an Excel dashboard with dynamic dropdowns and a demo pie chart")
    p_dash.add_argument("--workbook", required=True, help="Path to workbook (.xlsm/.xlsx)")
    def _dash(args: argparse.Namespace) -> None:
        build_dashboard(args.workbook)
        print("Dashboard created.")
    p_dash.set_defaults(func=_dash)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    # Load environment variables from .env if present
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()


