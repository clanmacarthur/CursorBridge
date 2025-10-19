CursorBridge
============

Windows-first CLI to bridge Excel automation (with or without VBA), Power Automate Desktop (PAD), and Notion.

What is CursorBridge?
---------------------
CursorBridge is your one-command control panel for everyday workflows on Windows. Run Excel tasks without writing VBA, send data into Notion, and (optionally) trigger PAD flows — all from a simple, readable CLI. It’s designed to be safe-by-default (backups and dry-runs), easy to set up, and flexible enough to grow with your automations.

Why you’ll like it
- Excel without VBA: write cells or append rows using openpyxl; keep your macros untouched.
- Notion made simple: append text, set properties, or create database rows from name=value pairs.
- Bridge profiles: save a mapping once (e.g., Excel → Notion) and run it any time.
- Safe operations: dry-run to preview changes before writing; PAD integration is opt-in and off by default.

Quick start
-----------

1. Install Python 3.9+ on Windows.
2. In PowerShell:

```
pip install -e .
```

3. Copy `.env.template` to `.env` and fill secrets.
4. Configure `config/flows.yaml` with your cloud flow HTTP URL(s).

CLI usage
---------

```
cb --help
cb excel run --workbook "C:\path\file.xlsm" --macro "Module1.DoThing"
cb excel run --workbook "C:\path\file.xlsx" --py "cb.excel:example_task"
cb pad run my_desktop_flow --param customerId=123
cb notion edit --page-id <uuid> --append "Run complete" --property Status=Done
cb notion db-insert --database-id <uuid> --property Name="My item" --property Status=Open

# Excel openpyxl helpers (no macros needed)
cb excel write --workbook "C:\path\file.xlsm" --sheet 1 --cell A1 --value "Hello"
cb excel append --workbook "C:\path\file.xlsm" --sheet Sheet1 --values col1 --values col2 --values col3

Bridge profiles
---------------

Define a profile in `config/bridge.yaml` and run it:

```
Dashboard builder
-----------------

You can build the dashboard even if your sheet names differ. For example, if your fighters sheet is named `Profiles` and your events sheet is `Events`:

```
cb dashboard --workbook "C:\\path\\Ankalaev vs. Pereira 2 (partly2).xlsm" --events-sheet "Events" --fighters-sheet "Profiles" --visible
```

Flags:
- `--events-sheet`: sheet containing `EventId` (default `Events`)
- `--fighters-sheet`: sheet containing fighters with `EventId` and `Name`/`Fighter` (default `fighters`)
- `--fights-sheet`: optional sheet containing fights with `EventId` and `FightName`/`Bout` (default `fights`)

cb bridge run-profile --profile ufc_events --dry-run
```

Or run ad-hoc with mapping:

```
cb bridge excel-to-notion --workbook "C:\path\file.xlsm" --sheet 1 --database-id <uuid> --map "Event=Name" --map "Location=Location" --dry-run
```
```

If the `cb` command isn't on PATH, you can run via Python:

```
python -m cb.cli --help
```

Configuration
-------------

`.env` (copy from `.env.template`):

```
NOTION_TOKEN=
``` 

`config/flows.yaml` example:

```
flows:
  my_desktop_flow:
    url: "https://prod-00.westeurope.logic.azure.com:443/..."
    timeout_seconds: 600
```

Status
------

Initial scaffold. PAD connectors will be wired in next commits.


