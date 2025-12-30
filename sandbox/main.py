"""
Sandbox Runner - FastAPI Application

This is the controlled execution environment for:
- Session generation
- Dashboard building
- Rule evaluation
- Risk gating

Runs separately from the main API for safety isolation.
"""

import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.database import get_db
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Wellness Sandbox Runner",
    description="Controlled execution environment for session generation",
    version="0.1.0",
)

# CORS for Main App access
ALLOWED_ORIGINS = [
    "http://localhost:8080",      # Main App dev
    "http://localhost:3000",      # API (internal calls)
    "https://yourdomain.com",     # Main App prod (update when known)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)


# =============================================================================
# Request/Response Models
# =============================================================================

class GenerateSessionRequest(BaseModel):
    user_id: str
    programme_profile_id: str  # Notion page ID or internal ID
    session_template_id: str
    duration_min: int = 20


class SessionSection(BaseModel):
    """A section within a generated session."""
    type: str  # "breathwork" | "movement" | "meditation" | "transition"
    name: str
    duration_minutes: float
    instructions: str
    audio_url: Optional[str] = None
    cues: Optional[List[str]] = None  # Timed cues for the player


class SessionOutput(BaseModel):
    """Full session output for the player UI."""
    id: str
    name: str
    duration_minutes: int
    persona_style: Optional[str] = None
    sections: List[SessionSection]
    safety_warnings: List[str]
    # Legacy fields for backwards compatibility
    user_id: str
    template_name: str
    breath_protocols: List[str]
    movements: List[str]
    created_at: str


class BuildDashboardRequest(BaseModel):
    user_id: str
    programme_profile_id: str


class DashboardBlock(BaseModel):
    block_id: str
    block_name: str
    block_type: str
    attributes: List[str]
    settings: Dict[str, Any]


class DashboardOutput(BaseModel):
    user_id: str
    programme_profile: str
    blocks: List[DashboardBlock]
    generated_at: str


# =============================================================================
# Health Check
# =============================================================================

@app.get("/")
async def root():
    return {"status": "ok", "service": "wellness-sandbox", "version": "0.1.0"}


# =============================================================================
# Session Generation
# =============================================================================

@app.post("/sandbox/generate-session", response_model=SessionOutput)
async def generate_session(request: GenerateSessionRequest):
    """
    Generate a session from a template.
    
    This is the core "engine" that:
    1. Loads Session Template with all relations
    2. Expands intents via Attribute Taxonomy
    3. Applies Safety Rules (hard stops + warnings)
    4. Assembles the script using chosen Persona lens
    5. Emits structured output
    """
    db = get_db()
    
    # 1. Load session template
    templates = db.get_session_templates()
    template = None
    for t in templates:
        if t.get("notion_page_id") == request.session_template_id or str(t.get("id")) == request.session_template_id:
            template = t
            break
    
    if not template:
        raise HTTPException(status_code=404, detail="Session template not found")
    
    # 2. Load programme profile for defaults
    profiles = db.get_programme_profiles()
    profile = None
    for p in profiles:
        if p.get("notion_page_id") == request.programme_profile_id or str(p.get("id")) == request.programme_profile_id:
            profile = p
            break
    
    # 3. Load related content
    breath_library = db.get_breath_library()
    movements = db.get_movements()
    safety_rules = db.get_safety_rules()
    personas = db.get_archetypal_personas()
    
    # 4. Apply safety rules
    safety_warnings = []
    for rule in safety_rules:
        # Basic safety check - in production, this would be more sophisticated
        severity = rule.get("severity", "")
        if severity and severity.lower() in ["high", "warning"]:
            safety_warnings.append(f"{rule.get('rule_name', 'Unknown')}: {rule.get('description', '')}")
    
    # 5. Select persona style
    persona_style = None
    if personas:
        persona_style = personas[0].get("persona")
    
    # 6. Build session sections (new format for player UI)
    sections: List[SessionSection] = []
    remaining_time = request.duration_min
    
    # Opening breath section (15% of time, min 2 min)
    opening_duration = max(2, int(request.duration_min * 0.15))
    remaining_time -= opening_duration
    
    opening_breath = breath_library[0] if breath_library else None
    sections.append(SessionSection(
        type="breathwork",
        name=opening_breath.get("protocol_name", "Centering Breath") if opening_breath else "Centering Breath",
        duration_minutes=opening_duration,
        instructions=f"Begin with {opening_breath.get('protocol_name', 'deep breathing')}. "
                     f"Find a comfortable position and settle into your breath." if opening_breath 
                     else "Take slow, deep breaths to center yourself.",
        cues=[
            f"0:00 - Begin {opening_breath.get('protocol_name', 'breathing') if opening_breath else 'breathing'}",
            f"0:30 - Deepen your breath",
            f"{opening_duration-1}:00 - Prepare to transition",
        ]
    ))
    
    # Movement section (50% of time)
    movement_duration = max(5, int(request.duration_min * 0.5))
    remaining_time -= movement_duration
    
    if movements:
        movement = movements[0]
        sections.append(SessionSection(
            type="movement",
            name=movement.get("movement___practice", "Gentle Movement"),
            duration_minutes=movement_duration,
            instructions=f"Practice {movement.get('movement___practice', 'gentle movement')}. "
                        f"{movement.get('notes', 'Move mindfully and with awareness.')}",
            cues=[
                f"0:00 - Begin {movement.get('movement___practice', 'movement')}",
                f"{movement_duration//2}:00 - Find your rhythm",
                f"{movement_duration-2}:00 - Begin to slow down",
            ]
        ))
    else:
        sections.append(SessionSection(
            type="meditation",
            name="Mindful Awareness",
            duration_minutes=movement_duration,
            instructions="Rest in open awareness. Notice sensations, thoughts, and feelings without judgment.",
            cues=[
                "0:00 - Settle into stillness",
                f"{movement_duration//2}:00 - Deepen your awareness",
                f"{movement_duration-1}:00 - Begin to return",
            ]
        ))
    
    # Closing section (remaining time)
    closing_duration = max(2, remaining_time)
    closing_breath = breath_library[1] if len(breath_library) > 1 else breath_library[0] if breath_library else None
    
    sections.append(SessionSection(
        type="breathwork",
        name=closing_breath.get("protocol_name", "Integration Breath") if closing_breath else "Integration Breath",
        duration_minutes=closing_duration,
        instructions="Return to your natural breath. Allow the practice to integrate. "
                    "When ready, gently open your eyes.",
        cues=[
            "0:00 - Return to natural breathing",
            f"{closing_duration-1}:00 - Begin to return to the room",
            f"{closing_duration}:00 - Session complete",
        ]
    ))
    
    # 7. Build output (new format)
    return SessionOutput(
        id=str(uuid4()),
        name=template.get("column_name", "Wellness Session"),
        duration_minutes=request.duration_min,
        persona_style=persona_style,
        sections=sections,
        safety_warnings=safety_warnings[:5],
        # Legacy fields
        user_id=request.user_id,
        template_name=template.get("column_name", "Unknown"),
        breath_protocols=[b.get("protocol_name", "") for b in breath_library[:3]],
        movements=[m.get("movement___practice", "") for m in movements[:3]],
        created_at=datetime.utcnow().isoformat(),
    )


# =============================================================================
# Dashboard Building
# =============================================================================

@app.post("/sandbox/build-dashboard", response_model=DashboardOutput)
async def build_dashboard(request: BuildDashboardRequest):
    """
    Build dashboard blocks for a user based on their programme profile.
    
    This:
    1. Loads the programme profile
    2. Gets applicable dashboard blocks
    3. Applies rules/gating
    4. Expands taxonomy attributes
    5. Returns configured blocks
    """
    db = get_db()
    
    # 1. Load programme profile
    profiles = db.get_programme_profiles()
    profile = None
    profile_name = "Default"
    
    for p in profiles:
        if p.get("notion_page_id") == request.programme_profile_id or str(p.get("id")) == request.programme_profile_id:
            profile = p
            profile_name = p.get("programme_profile___title", "Unknown")
            break
    
    # 2. Load dashboard blocks
    all_blocks = db.get_dashboard_blocks()
    
    # 3. Load gating rules
    gating_rules = db.get_rules_gating()
    
    # 4. Load attribute taxonomy for expansion
    taxonomy = db.get_attribute_taxonomy()
    
    # 5. Build blocks for this profile
    output_blocks = []
    
    for block in all_blocks:
        # Check if block is linked to this profile (simplified)
        block_name = block.get("column", "") or block.get("block_name", "Unknown")
        block_type = block.get("block_type", "checkboxes")
        
        # Get required attributes
        required_attrs = block.get("required_attributes", "")
        attrs_list = [a.strip() for a in required_attrs.split(",")] if required_attrs else []
        
        # Expand attributes from taxonomy
        expanded_attrs = []
        for attr in attrs_list:
            expanded_attrs.append(attr)
            # In production: walk taxonomy tree to expand
        
        output_blocks.append(DashboardBlock(
            block_id=block.get("notion_page_id", str(block.get("id", ""))),
            block_name=block_name,
            block_type=block_type,
            attributes=expanded_attrs if expanded_attrs else [block_name],
            settings={
                "default_depth": block.get("default_depth"),
                "default_strictness": block.get("default_strictness"),
                "display_depth": block.get("display_depth"),
            },
        ))
    
    return DashboardOutput(
        user_id=request.user_id,
        programme_profile=profile_name,
        blocks=output_blocks,
        generated_at=datetime.utcnow().isoformat(),
    )


# =============================================================================
# Rule Evaluation (internal helper)
# =============================================================================

@app.get("/sandbox/rules/evaluate")
async def evaluate_rules(
    user_id: str,
    context: str = "session",  # session, dashboard, intake
):
    """
    Evaluate all applicable rules for a given context.
    Returns warnings and blocks.
    """
    db = get_db()
    rules = db.get_rules_gating()
    safety = db.get_safety_rules()
    
    warnings = []
    blocks = []
    
    for rule in rules:
        rule_type = rule.get("rule_type", "")
        applies_to = rule.get("applies_to", "")
        
        if context.lower() in applies_to.lower():
            action = rule.get("action", "")
            if "block" in action.lower():
                blocks.append({
                    "rule": rule.get("column_name", "Unknown"),
                    "action": action,
                })
            elif "warn" in action.lower() or "flag" in action.lower():
                warnings.append({
                    "rule": rule.get("column_name", "Unknown"),
                    "message": rule.get("notes", ""),
                })
    
    return {
        "context": context,
        "warnings": warnings,
        "blocks": blocks,
        "evaluated_at": datetime.utcnow().isoformat(),
    }


# =============================================================================
# Run the app
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)  # Different port from main API



