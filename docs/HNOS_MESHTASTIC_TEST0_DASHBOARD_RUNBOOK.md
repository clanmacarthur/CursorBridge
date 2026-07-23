# HNOS Meshtastic TEST 0 → Dashboard Manager Runbook

**Status:** canonical test sequence for the current Dashboard Manager API and HNOS Meshtastic proof  
**Dashboard Manager repository state checked:** current `main` at commit `0ef2b08f8c66ec06ec82119fb5bf85fa54e76c84`

## Decision

Dashboard Manager must be prepared before a mock or real Meshtastic packet can appear in it.

The sequence is:

```text
TEST 0A — mock packet → local Dashboard Manager payload
DM SETUP — exact datapoints + packet group + scoped API key
TEST 0B — mock packet → Dashboard Manager
TEST 0C — real packet → Windows capture only
TEST 2  — real packet → Dashboard Manager
TEST 1  — measured walking/range survey
```

`TEST 0A` and `TEST 0C` can run without Dashboard Manager configuration. `TEST 0B` and `TEST 2` cannot.

## Dashboard Manager prerequisites

The current external API writes one atomic Entry session using exact `dataPointKey` values and optional repeating `groupEntries`. The current UI exposes:

- Builder → Dashboard layout
- Builder → Entry layout
- Builder → Data points
- Profile → Third-Party API Keys
- Entry/Data → Add data or Data table

### Required current-state datapoints

```text
mesh_last_packet_at                  dateTime
mesh_last_source_node                text
mesh_last_rssi_dbm                   number, dBm
mesh_last_snr_db                     number, dB
mesh_last_hop_count                  number
site01_battery_percent               number, %
site01_battery_volts                 number, V
site01_channel_utilisation_percent   number, %
site01_airtime_tx_percent            number, %
site01_air_temperature_c             number, °C
site01_humidity_percent              number, %
site01_pressure_hpa                  number, hPa
```

### Required packet-history datapoints

```text
mesh_packet_time       dateTime
mesh_packet_id         text
mesh_source_node       text
mesh_destination       text
mesh_portnum           text
mesh_rssi_dbm          number, dBm
mesh_snr_db             number, dB
mesh_hop_count         number
mesh_payload_summary   text
```

### Required repeating group

```text
ref: mesh-packet-log
key: mesh_packet_log
title: Mesh Packet Log
mode: repeating_rows
columns: all nine packet-history datapoints above
```

The exact keys are mandatory. The API does not write by the friendly label.

## Fastest DM setup

Open the target dashboard Builder, expand the existing AI panel, and ask it to create the datapoints and repeating group above. Review and apply the proposal. The current AI tool contract supports `upsert_datapoints` and `upsert_entry_groups`.

Then verify:

```text
Builder → Data points: every exact key exists and is active
Builder → Entry layout: Mesh Packet Log exists as repeating rows
```

Recommended test widgets:

```text
Battery stat
Last RSSI stat
Last SNR stat
Temperature stat/gauge
Packet Log table
```

## API key

In Profile → Third-Party API Keys:

```text
Label: HNOS Meshtastic TEST 0
Scope: Selected dashboards
Allowed dashboard: the HNOS test dashboard
Permissions: dashboards.read + entries.write
Expiry: short test expiry where appropriate
```

Copy the secret immediately; the full key is displayed only once.

The dashboard ID is the value in:

```text
/dashboard/DASHBOARD_ID/builder
```

The API base is the Convex HTTP Actions URL plus `/api/v1`:

```text
https://DEPLOYMENT.convex.site/api/v1
```

Verify:

```powershell
Invoke-RestMethod -Method Get -Uri "https://DEPLOYMENT.convex.site/api/v1/health"
```

Expected result includes `ok: true` and `service: dashboard-manager`.

## TEST 0A — no DM required

From the extracted test pack in PowerShell:

```powershell
cd C:\HNOS\meshtastic-test
py -3 -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python test0_mock_packet.py
```

Pass output:

```text
PASS: mock packet was normalised.
Packet ID: 28914412
Source: !a1b2c3d4
Generated API payload: generated_dashboard_payload.json
DRY RUN: nothing was uploaded.
```

## Configure `.env`

```powershell
Copy-Item .env.example .env
notepad .env
```

```dotenv
DASHBOARD_API_BASE=https://DEPLOYMENT.convex.site/api/v1
DASHBOARD_ID=YOUR_DASHBOARD_ID
DASHBOARD_API_KEY=dm_prefix_secret
MESHTASTIC_PORT=COM4
```

## TEST 0B — mock packet into DM

```powershell
python test0_mock_packet.py --send
```

Pass output:

```text
PASS: Dashboard Manager accepted the entry session.
```

Verify in the target dashboard:

```text
Entry/Data → Data table
Session label: Meshtastic packet batch
Standalone telemetry values present
One Mesh Packet Log row present
Dashboard test widgets updated
```

## TEST 0C — real packet captured locally

Attach antennas before power. Connect one Seeed node to Windows over a USB data cable and power the second node separately. Both must use the same Meshtastic region, channel, and radio preset.

Find the port:

```powershell
python -m serial.tools.list_ports
```

Listen:

```powershell
python listen_meshtastic.py --port COM4 --once
```

Send `TEST-001` from the second node.

Pass output includes:

```text
CONNECTED: Meshtastic node database downloaded.
RECEIVED
Packet ID: ...
Source: ...
RSSI: ...
SNR: ...
Saved raw packet: captured_packets\...
```

## TEST 2 — real packet into DM

Only after TEST 0B passes:

```powershell
python listen_meshtastic.py --port COM4 --once --send
```

Send `TEST-002` from the second node.

Pass output:

```text
RECEIVED
UPLOADED: Dashboard Manager accepted the packet.
```

Verify the new Entry session and updated widgets.

## Stop conditions

```text
401 → invalid, missing, expired, or revoked API key
403 → missing entries.write or dashboard outside selected scope
404 → wrong API base or dashboard ID
422 → missing/wrong datapoint key, group key, column, or datatype
No COM port → charge-only cable, driver/device issue, or board not enumerating
Connected but no packet → region/channel/preset mismatch, missing antenna, or no transmission
```

Do not begin the walking range survey until the short-range packet exchange passes.
