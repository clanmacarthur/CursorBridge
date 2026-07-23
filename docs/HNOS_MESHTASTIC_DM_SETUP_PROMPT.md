# Dashboard Manager AI Setup Prompt — HNOS Meshtastic TEST 0

Paste the block below into the existing Dashboard Manager AI builder for the dashboard that will receive TEST 0. Review the proposal, then click **Apply**.

```text
Edit this dashboard for HNOS Meshtastic TEST 0. Preserve unrelated existing content. Create or update the following active datapoints using these exact keys. Set collection frequency to none and required to false.

Standalone/current-state datapoints:
- mesh_last_packet_at — Date and time
- mesh_last_source_node — Text
- mesh_last_rssi_dbm — Number, unit dBm
- mesh_last_snr_db — Number, unit dB
- mesh_last_hop_count — Number
- site01_battery_percent — Number, unit %
- site01_battery_volts — Number, unit V
- site01_channel_utilisation_percent — Number, unit %
- site01_airtime_tx_percent — Number, unit %
- site01_air_temperature_c — Number, unit °C
- site01_humidity_percent — Number, unit %
- site01_pressure_hpa — Number, unit hPa

Packet-history datapoints:
- mesh_packet_time — Date and time
- mesh_packet_id — Text
- mesh_source_node — Text
- mesh_destination — Text
- mesh_portnum — Text
- mesh_rssi_dbm — Number, unit dBm
- mesh_snr_db — Number, unit dB
- mesh_hop_count — Number
- mesh_payload_summary — Text

Create one active repeating Entry group with:
- ref: mesh-packet-log
- key: mesh_packet_log
- title: Mesh Packet Log
- description: Packets received by the HNOS Meshtastic connector
- mode: repeating_rows
- add-row label: Add packet
- minimum rows: 0
- maximum rows: 100
- columns: all nine packet-history datapoints above, in the order listed
- section heading: Mesh packets

Create a compact dashboard section named Mesh Test with:
- Stat: Battery, bound to site01_battery_percent, latest
- Stat: Last RSSI, bound to mesh_last_rssi_dbm, latest
- Stat: Last SNR, bound to mesh_last_snr_db, latest
- Compact text-feed or table: Last source, bound to mesh_last_source_node, latest
- Stat or gauge: Temperature, bound to site01_air_temperature_c, latest
- Table: Packet Log, bound to mesh_packet_time, mesh_source_node, mesh_portnum, mesh_rssi_dbm, mesh_snr_db, mesh_hop_count, and mesh_payload_summary

Do not add actuator controls, pump commands, automations, public publishing, or a geographic map in this TEST 0 setup. Exact datapoint keys and the exact group key mesh_packet_log are mandatory because the external API writes by key.
```

After applying the proposal, verify every exact key under **Builder → Data points** and verify `Mesh Packet Log` under **Builder → Entry layout** before creating the API key or sending a packet.
