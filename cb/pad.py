import json
import os
from typing import Any, Dict

import requests
import yaml


def _load_flows() -> Dict[str, Any]:
    config_path = os.path.join(os.getcwd(), "config", "flows.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Missing config: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("flows", {})


def run_flow(flow_name: str, params: Dict[str, str]) -> Dict[str, Any]:
    flows = _load_flows()
    if flow_name not in flows:
        raise KeyError(f"Flow '{flow_name}' not defined in config/flows.yaml")
    flow_cfg = flows[flow_name]
    url = flow_cfg["url"]
    timeout_seconds = int(flow_cfg.get("timeout_seconds", 600))

    headers = {"Content-Type": "application/json"}
    payload = {"inputs": params}

    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout_seconds)
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError:
        return {"status": resp.status_code, "text": resp.text}


