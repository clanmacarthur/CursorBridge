"""
Seed required sessions tables that are currently empty.

This script is idempotent:
- It checks natural key combinations first.
- It inserts only missing rows.
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests


TASK_MANAGER_ENV = Path(r"C:\code\task-manager\.env")
REPORT_PATH = Path("docs/_sessions_seed_report.json")


@dataclass
class SupabaseConfig:
    url: str
    key: str


def load_env_file(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    values: Dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        values[k.strip().lstrip("\ufeff")] = v.strip()
    return values


def load_supabase_config() -> SupabaseConfig:
    def keys_from_env(env: Dict[str, str]) -> Tuple[str, List[str]]:
        url = (env.get("SUPABASE_URL") or "").strip().rstrip("/")
        keys = [
            (env.get("SUPABASE_SERVICE_ROLE_KEY") or "").strip(),
            (env.get("SUPABASE_SERVICE_KEY") or "").strip(),
            (env.get("SUPABASE_ANON_KEY") or "").strip(),
            (env.get("SUPABASE_KEY") or "").strip(),
        ]
        keys = [k for k in keys if k]
        return url, keys

    def works(url: str, key: str) -> bool:
        if not url or not key:
            return False
        try:
            resp = requests.get(
                f"{url}/rest/v1/",
                headers={
                    "apikey": key,
                    "Authorization": f"Bearer {key}",
                    "Accept": "application/openapi+json",
                },
                timeout=20,
            )
            return resp.status_code == 200
        except Exception:
            return False

    candidates: List[Tuple[str, str]] = []

    env_runtime = dict(os.environ)
    env_file = load_env_file(TASK_MANAGER_ENV)

    for source in (env_runtime, env_file):
        url, keys = keys_from_env(source)
        for key in keys:
            candidates.append((url, key))

    for url, key in candidates:
        if works(url, key):
            return SupabaseConfig(url=url, key=key)

    raise RuntimeError(
        "No working Supabase URL/key pair found from environment or task-manager .env."
    )


class SupabaseRest:
    def __init__(self, cfg: SupabaseConfig):
        self.base = cfg.url + "/rest/v1"
        self.key = cfg.key

    def _headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
        }
        if extra:
            headers.update(extra)
        return headers

    def get(
        self,
        table: str,
        *,
        select: str = "*",
        filters: Optional[Dict[str, str]] = None,
        order: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        params: Dict[str, str] = {"select": select}
        if filters:
            params.update(filters)
        if order:
            params["order"] = order
        if limit is not None:
            params["limit"] = str(limit)
        resp = requests.get(
            f"{self.base}/{table}",
            params=params,
            headers=self._headers({"Prefer": "count=exact"}),
            timeout=60,
        )
        if resp.status_code not in (200, 206):
            raise RuntimeError(
                f"GET {table} failed ({resp.status_code}): {resp.text[:300]}"
            )
        data = resp.json()
        if not isinstance(data, list):
            raise RuntimeError(f"GET {table} returned non-list payload")
        return data

    def insert(self, table: str, row: Dict[str, Any]) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base}/{table}",
            json=row,
            headers=self._headers(
                {"Content-Type": "application/json", "Prefer": "return=representation"}
            ),
            timeout=60,
        )
        if resp.status_code not in (200, 201):
            raise RuntimeError(
                f"INSERT {table} failed ({resp.status_code}): {resp.text[:300]}"
            )
        payload = resp.json()
        if isinstance(payload, list) and payload:
            return payload[0]
        if isinstance(payload, dict):
            return payload
        return {}

    def max_id(self, table: str) -> int:
        rows = self.get(table, select="id", order="id.desc", limit=1)
        if not rows:
            return 0
        value = rows[0].get("id")
        if isinstance(value, int):
            return value
        try:
            return int(value)
        except Exception:
            return 0


def index_by(rows: Iterable[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        if value is None:
            continue
        result[str(value)] = row
    return result


def main() -> None:
    cfg = load_supabase_config()
    db = SupabaseRest(cfg)

    report: Dict[str, Any] = {
        "supabase_url": cfg.url,
        "actions": [],
        "inserted": {},
        "skipped": {},
        "errors": [],
    }

    def note(action: str) -> None:
        report["actions"].append(action)

    def bump(bucket: str, table: str) -> None:
        report[bucket][table] = int(report[bucket].get(table, 0)) + 1

    # Load source tables used for lookup.
    controls = db.get("control_definitions", select="id,control_name")
    packs = db.get("control_packs", select="id,pack_slug,pack_name")
    profiles = db.get("programme_profiles", select="id,programme_profile___title")
    attrs = db.get("attribute_taxonomy", select="id,attribute")
    lenses = db.get("lens_definitions", select="id,lens_slug,lens_name,is_active")
    personas = db.get("archetypal_personas", select="id,persona")
    kbs = db.get("knowledge_bases", select="id,kb_slug,kb_name")

    control_by_name = index_by(controls, "control_name")
    pack_by_slug = index_by(packs, "pack_slug")
    profile_by_title = index_by(profiles, "programme_profile___title")
    attr_by_name = index_by(attrs, "attribute")
    lens_by_slug = index_by(lenses, "lens_slug")
    persona_by_name = index_by(personas, "persona")
    kb_by_slug = index_by(kbs, "kb_slug")

    # ------------------------------------------------------------------
    # 1) control_pack_items
    # ------------------------------------------------------------------
    note("Seeding control_pack_items")
    existing_cpi = db.get("control_pack_items", select="pack_id,control_id")
    cpi_set = {(str(r.get("pack_id")), str(r.get("control_id"))) for r in existing_cpi}

    control_pack_seed = [
        ("daily-essentials", "Hydration", 1),
        ("daily-essentials", "Sleep Duration", 2),
        ("daily-essentials", "Movement", 3),
        ("daily-essentials", "Mood", 4),
        ("stress-management", "Meditation", 1),
        ("stress-management", "Sleep Quality", 2),
        ("stress-management", "Mood", 3),
        ("insomnia-support", "Sleep Duration", 1),
        ("insomnia-support", "Sleep Quality", 2),
        ("insomnia-support", "Caffeine Intake", 3),
        ("trauma-safe", "Mood", 1),
        ("trauma-safe", "Meditation", 2),
    ]

    for pack_slug, control_name, display_order in control_pack_seed:
        pack = pack_by_slug.get(pack_slug)
        control = control_by_name.get(control_name)
        if not pack or not control:
            report["errors"].append(
                f"control_pack_items lookup failed: pack={pack_slug} control={control_name}"
            )
            continue
        key = (str(pack["id"]), str(control["id"]))
        if key in cpi_set:
            bump("skipped", "control_pack_items")
            continue
        db.insert(
            "control_pack_items",
            {
                "id": str(uuid.uuid4()),
                "pack_id": pack["id"],
                "control_id": control["id"],
                "display_order": display_order,
            },
        )
        cpi_set.add(key)
        bump("inserted", "control_pack_items")

    # ------------------------------------------------------------------
    # 2) profile_pack_map
    # ------------------------------------------------------------------
    note("Seeding profile_pack_map")
    existing_ppm = db.get("profile_pack_map", select="programme_profile_id,pack_id")
    ppm_set = {(str(r.get("programme_profile_id")), str(r.get("pack_id"))) for r in existing_ppm}

    profile_pack_seed = [
        ("Yoga Practitioner", "daily-essentials", True, 1),
        ("Mindfulness / Vipassana", "stress-management", True, 1),
        ("Trauma-Safe Regulation", "trauma-safe", True, 1),
        ("General Wellness", "daily-essentials", True, 1),
        ("Endurance Athlete", "endurance-athlete", True, 1),
        ("Swimmer", "endurance-athlete", True, 1),
        ("Athlete", "endurance-athlete", True, 1),
    ]

    for profile_title, pack_slug, is_required, display_order in profile_pack_seed:
        profile = profile_by_title.get(profile_title)
        pack = pack_by_slug.get(pack_slug)
        if not profile or not pack:
            report["errors"].append(
                f"profile_pack_map lookup failed: profile={profile_title} pack={pack_slug}"
            )
            continue
        profile_id_text = str(profile["id"])
        key = (profile_id_text, str(pack["id"]))
        if key in ppm_set:
            bump("skipped", "profile_pack_map")
            continue
        db.insert(
            "profile_pack_map",
            {
                "id": str(uuid.uuid4()),
                "programme_profile_id": profile_id_text,
                "pack_id": pack["id"],
                "display_order": display_order,
                "is_required": is_required,
                "notes": "seeded sessions map",
            },
        )
        ppm_set.add(key)
        bump("inserted", "profile_pack_map")

    # ------------------------------------------------------------------
    # 3) default_weights
    # ------------------------------------------------------------------
    note("Seeding default_weights")
    existing_dw = db.get("default_weights", select="programme_profile_id,attribute_id")
    dw_set = {(str(r.get("programme_profile_id")), str(r.get("attribute_id"))) for r in existing_dw}

    default_weight_seed = [
        ("Yoga Practitioner", "Emotional Regulation", 0.90, "high", "emotion"),
        ("Yoga Practitioner", "Integration Capacity", 0.80, "high", "integration"),
        ("Trauma-Safe Regulation", "Stress Recovery", 1.00, "critical", "safety"),
        ("Trauma-Safe Regulation", "Anxiety Modulation", 0.90, "high", "safety"),
        ("General Wellness", "Food Quality & Sensitivities", 0.70, "medium", "nutrition"),
        ("Endurance Athlete", "Coordination", 0.80, "high", "performance"),
        ("Endurance Athlete", "Glycemic Regulation", 0.80, "high", "performance"),
    ]

    for profile_title, attr_name, weight, weight_label, domain in default_weight_seed:
        profile = profile_by_title.get(profile_title)
        attr = attr_by_name.get(attr_name)
        if not profile or not attr:
            report["errors"].append(
                f"default_weights lookup failed: profile={profile_title} attribute={attr_name}"
            )
            continue
        profile_id_text = str(profile["id"])
        attr_id_text = str(attr["id"])
        key = (profile_id_text, attr_id_text)
        if key in dw_set:
            bump("skipped", "default_weights")
            continue
        db.insert(
            "default_weights",
            {
                "id": str(uuid.uuid4()),
                "programme_profile_id": profile_id_text,
                "attribute_id": attr_id_text,
                "weight": weight,
                "weight_label": weight_label,
                "domain": domain,
                "notes": "seeded sessions defaults",
            },
        )
        dw_set.add(key)
        bump("inserted", "default_weights")

    # ------------------------------------------------------------------
    # 4) persona_lens_compatibility
    # ------------------------------------------------------------------
    note("Seeding persona_lens_compatibility")
    existing_plc = db.get("persona_lens_compatibility", select="id,persona_id,lens_id")
    plc_set = {(int(r.get("persona_id")), int(r.get("lens_id"))) for r in existing_plc if r.get("persona_id") is not None and r.get("lens_id") is not None}
    plc_next_id = max([int(r.get("id", 0)) for r in existing_plc] + [0]) + 1

    persona_lens_seed = [
        ("Clinical Guide", "western", 92, "clinical language fit"),
        ("Clinical Guide", "clinical", 96, "core clinical persona"),
        ("Clinical Guide", "polyvagal", 88, "regulation aligned"),
        ("Somatic Companion", "somatic", 97, "body-first fit"),
        ("Somatic Companion", "polyvagal", 90, "nervous-system framing"),
        ("Somatic Companion", "spiritual", 65, "allowed but secondary"),
        ("Alan Watts–like", "spiritual", 95, "poetic-spiritual fit"),
        ("Alan Watts–like", "contemplative", 88, "reflective framing"),
        ("Alan Watts–like", "yogic", 82, "compatible doctrine voice"),
    ]

    for persona_name, lens_slug, score, notes in persona_lens_seed:
        persona = persona_by_name.get(persona_name)
        lens = lens_by_slug.get(lens_slug)
        if not persona or not lens:
            report["errors"].append(
                f"persona_lens_compatibility lookup failed: persona={persona_name} lens={lens_slug}"
            )
            continue
        key = (int(persona["id"]), int(lens["id"]))
        if key in plc_set:
            bump("skipped", "persona_lens_compatibility")
            continue
        db.insert(
            "persona_lens_compatibility",
            {
                "id": plc_next_id,
                "persona_id": key[0],
                "lens_id": key[1],
                "compatibility_score": score,
                "notes": notes,
            },
        )
        plc_next_id += 1
        plc_set.add(key)
        bump("inserted", "persona_lens_compatibility")

    # ------------------------------------------------------------------
    # 5) programme_knowledge_map
    # ------------------------------------------------------------------
    note("Seeding programme_knowledge_map")
    existing_pkm = db.get("programme_knowledge_map", select="id,programme_profile_id,kb_id")
    pkm_set = {
        (str(r.get("programme_profile_id")), int(r.get("kb_id")))
        for r in existing_pkm
        if r.get("programme_profile_id") is not None and r.get("kb_id") is not None
    }
    pkm_next_id = max([int(r.get("id", 0)) for r in existing_pkm] + [0]) + 1

    programme_kb_seed = [
        ("Yoga Practitioner", "yoga_sutras", True, True, 100),
        ("Mindfulness / Vipassana", "zen_koans", True, True, 100),
        ("Trauma-Safe Regulation", "pubmed_psychology", True, True, 100),
        ("General Wellness", "cochrane_reviews", False, True, 80),
        ("Endurance Athlete", "pubmed_neuroscience", True, True, 90),
    ]

    for profile_title, kb_slug, is_required, is_default, weight in programme_kb_seed:
        profile = profile_by_title.get(profile_title)
        kb = kb_by_slug.get(kb_slug)
        if not profile or not kb:
            report["errors"].append(
                f"programme_knowledge_map lookup failed: profile={profile_title} kb={kb_slug}"
            )
            continue
        profile_id_text = str(profile["id"])
        kb_id = int(kb["id"])
        key = (profile_id_text, kb_id)
        if key in pkm_set:
            bump("skipped", "programme_knowledge_map")
            continue
        db.insert(
            "programme_knowledge_map",
            {
                "id": pkm_next_id,
                "programme_profile_id": profile_id_text,
                "kb_id": kb_id,
                "is_required": is_required,
                "is_default": is_default,
                "weight": weight,
            },
        )
        pkm_next_id += 1
        pkm_set.add(key)
        bump("inserted", "programme_knowledge_map")

    # ------------------------------------------------------------------
    # 6) questionnaires + questionnaire_questions
    # ------------------------------------------------------------------
    note("Seeding questionnaires and questionnaire_questions")
    questionnaire_slug = "sessions-core-intake-v1"
    questionnaire_name = "Sessions Core Intake"
    questionnaire_rows = db.get(
        "questionnaires",
        select="id,questionnaire_slug",
        filters={"questionnaire_slug": f"eq.{questionnaire_slug}"},
        limit=1,
    )
    if questionnaire_rows:
        questionnaire_id = str(questionnaire_rows[0]["id"])
        bump("skipped", "questionnaires")
    else:
        questionnaire_id = str(uuid.uuid4())
        db.insert(
            "questionnaires",
            {
                "id": questionnaire_id,
                "questionnaire_name": questionnaire_name,
                "questionnaire_slug": questionnaire_slug,
                "description": "Baseline intake for deterministic session planning.",
                "version": 1,
                "is_active": True,
                "is_onboarding": True,
                "scoring_method": "weighted",
                "notes": "seeded for sessions-first runtime",
            },
        )
        bump("inserted", "questionnaires")

    existing_questions = db.get(
        "questionnaire_questions",
        select="id,questionnaire_id,display_order",
        filters={"questionnaire_id": f"eq.{questionnaire_id}"},
    )
    existing_q_orders = {
        int(row.get("display_order"))
        for row in existing_questions
        if row.get("display_order") is not None
    }

    question_seed = [
        (
            1,
            "How stressed do you feel right now?",
            "scale",
            None,
            0,
            10,
            {"min": "calm", "max": "overloaded"},
            1.0,
        ),
        (
            2,
            "How much physical energy do you have right now?",
            "scale",
            None,
            0,
            10,
            {"min": "depleted", "max": "high"},
            1.0,
        ),
        (
            3,
            "What is your main session intention today?",
            "single_select",
            ["regulate", "focus", "recovery", "sleep", "grounding"],
            None,
            None,
            None,
            1.0,
        ),
        (
            4,
            "Do you want gentle language and low intensity today?",
            "boolean",
            None,
            None,
            None,
            None,
            1.0,
        ),
        (
            5,
            "Do you want symbolic/spiritual framing in narration?",
            "boolean",
            None,
            None,
            None,
            None,
            0.7,
        ),
        (
            6,
            "Any constraints we should respect in this session?",
            "text",
            None,
            None,
            None,
            None,
            0.5,
        ),
    ]

    for display_order, text, qtype, options, smin, smax, labels, weight in question_seed:
        if display_order in existing_q_orders:
            bump("skipped", "questionnaire_questions")
            continue
        payload: Dict[str, Any] = {
            "id": str(uuid.uuid4()),
            "questionnaire_id": questionnaire_id,
            "question_text": text,
            "question_type": qtype,
            "display_order": display_order,
            "is_required": True if display_order <= 4 else False,
            "weight": weight,
            "notes": "seeded for sessions intake",
        }
        if options is not None:
            payload["options"] = options
        if smin is not None:
            payload["scale_min"] = smin
        if smax is not None:
            payload["scale_max"] = smax
        if labels is not None:
            payload["scale_labels"] = labels

        db.insert("questionnaire_questions", payload)
        existing_q_orders.add(display_order)
        bump("inserted", "questionnaire_questions")

    # questionnaire_responses intentionally left empty (runtime write table).
    note("questionnaire_responses intentionally not seeded (runtime user data table)")

    # Final counts snapshot for seeded targets.
    target_tables = [
        "control_pack_items",
        "default_weights",
        "persona_lens_compatibility",
        "profile_pack_map",
        "programme_knowledge_map",
        "questionnaires",
        "questionnaire_questions",
        "questionnaire_responses",
    ]
    final_counts: Dict[str, int] = {}
    for table in target_tables:
        rows = db.get(table, select="id", limit=1)
        # Use Content-Range would be cleaner, but list length is fine with limit=1 for existence.
        # We fetch full count quickly through order+limit path:
        full = db.get(table, select="id")
        final_counts[table] = len(full)
    report["final_counts"] = final_counts

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Seeding complete.")
    print("Inserted:", report["inserted"])
    print("Skipped:", report["skipped"])
    print("Errors:", len(report["errors"]))
    print("Final counts:", final_counts)
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
