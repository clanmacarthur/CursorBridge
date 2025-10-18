import importlib
import os
import time
from typing import Any, Callable


def _open_book(path: str) -> Any:
    # Lazy import to avoid requiring xlwings for non-Excel commands
    import xlwings as xw  # type: ignore
    visible_env = os.getenv("XLWINGS_VISIBLE", "false").lower() == "true"
    app = xw.App(visible=visible_env, add_book=False)
    try:
        book = app.books.open(path)
    except Exception:
        app.quit()
        raise
    return book


def run_macro(workbook_path: str, macro_name: str) -> None:
    book = _open_book(workbook_path)
    try:
        macro = book.macro(macro_name)
        macro()
        book.save()
    finally:
        book.close()
        book.app.quit()


def run_python(workbook_path: str, callable_path: str) -> None:
    try:
        module_name, func_name = callable_path.split(":", 1)
    except ValueError:
        raise ValueError("callable path must be in the form 'module:function'")

    # Try the xlwings path first
    try:
        module = importlib.import_module(module_name)
        func: Callable[[Any], None] = getattr(module, func_name)
        book = _open_book(workbook_path)
        try:
            func(book)
            book.save()
        finally:
            book.close()
            book.app.quit()
        return
    except ModuleNotFoundError as e:
        if e.name != "xlwings":
            # Module of the callable is missing, bubble up
            raise
        # Fall through to openpyxl fallback

    # Fallback: minimal write to A1 using openpyxl while keeping macros
    if module_name == "cb.excel" and func_name == "example_task":
        try:
            from openpyxl import load_workbook  # type: ignore
        except Exception as ex:
            raise RuntimeError("openpyxl not installed; run: python -m pip install openpyxl") from ex
        wb = load_workbook(workbook_path, keep_vba=True)
        ws = wb.worksheets[0]
        ws["A1"] = f"Updated by CursorBridge at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        wb.save(workbook_path)
        return

    raise RuntimeError(
        "xlwings is not available and no fallback is defined for this callable. "
        "Install xlwings: python -m pip install xlwings"
    )


def example_task(book: Any) -> None:
    sheet = book.sheets[0]
    sheet.range("A1").value = f"Updated by CursorBridge at {time.strftime('%Y-%m-%d %H:%M:%S')}"


def _openpyxl_get_worksheet(workbook, sheet: str):
    # sheet can be a name or 1-based index as string
    if sheet.isdigit():
        idx = int(sheet)
        if idx <= 0:
            raise ValueError("Sheet index must be >= 1")
        return workbook.worksheets[idx - 1]
    if sheet in workbook.sheetnames:
        return workbook[sheet]
    raise KeyError(f"Worksheet '{sheet}' not found")


def write_cell_openpyxl(workbook_path: str, sheet: str, cell: str, value: str) -> None:
    try:
        from openpyxl import load_workbook  # type: ignore
    except Exception as ex:
        raise RuntimeError("openpyxl not installed; run: python -m pip install openpyxl") from ex
    wb = load_workbook(workbook_path, keep_vba=True)
    ws = _openpyxl_get_worksheet(wb, sheet)
    ws[cell] = value
    wb.save(workbook_path)


def append_row_openpyxl(workbook_path: str, sheet: str, values: list[str]) -> None:
    try:
        from openpyxl import load_workbook  # type: ignore
    except Exception as ex:
        raise RuntimeError("openpyxl not installed; run: python -m pip install openpyxl") from ex
    wb = load_workbook(workbook_path, keep_vba=True)
    ws = _openpyxl_get_worksheet(wb, sheet)
    ws.append(values)
    wb.save(workbook_path)


