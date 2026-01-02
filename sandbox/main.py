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
    # LENS SYSTEM - New parameters for multi-paradigm explanations
    lens: str = "western"  # "western" | "tcm" | "hybrid"
    explanation_level: str = "plain"  # "plain" | "clinical"
    # Optional: specify techniques directly
    technique_ids: Optional[List[str]] = None


class SessionSection(BaseModel):
    """A section within a generated session."""
    type: str  # "breathwork" | "movement" | "meditation" | "transition"
    name: str
    duration_minutes: float
    instructions: str
    audio_url: Optional[str] = None
    cues: Optional[List[str]] = None  # Timed cues for the player
    # LENS SYSTEM - Explanation templates by paradigm
    lens_explanation: Optional[str] = None  # The active lens explanation
    lens_explanation_western: Optional[str] = None
    lens_explanation_tcm: Optional[str] = None
    mechanism_notes: Optional[str] = None
    technique_id: Optional[str] = None  # Reference to the technique


class SessionOutput(BaseModel):
    """Full session output for the player UI."""
    id: str
    name: str
    duration_minutes: int
    persona_style: Optional[str] = None
    sections: List[SessionSection]
    safety_warnings: List[str]
    # LENS SYSTEM - Active lens for this session
    lens: str = "western"  # "western" | "tcm" | "hybrid"
    explanation_level: str = "plain"  # "plain" | "clinical"
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

def get_lens_explanation(technique: Dict[str, Any], lens: str) -> str:
    """
    Get the appropriate explanation based on the requested lens.
    
    Supports 14+ lenses with intelligent fallback:
    - scientific: western, clinical, athletic
    - traditional: tcm, ayurvedic, yogic
    - somatic: somatic, polyvagal
    - spiritual: spiritual, contemplative
    - practical: plain, motivational
    - adaptive: hybrid, personalized
    """
    # Primary explanations from technique table
    western = technique.get("lens_explanation_western") or technique.get("mechanism_notes_simple", "")
    tcm = technique.get("lens_explanation_tcm", "")
    mechanism = technique.get("mechanism_notes_simple", "")
    
    # Lens-specific templates (expandable)
    LENS_TEMPLATES = {
        # Scientific paradigm
        "western": western,
        "clinical": western,  # Uses same base, can be enhanced
        "athletic": western,  # Performance framing
        
        # Traditional paradigm
        "tcm": tcm if tcm else western,
        "ayurvedic": tcm if tcm else western,  # Falls back to TCM/Western
        "yogic": tcm if tcm else western,
        
        # Somatic paradigm
        "somatic": mechanism if mechanism else western,
        "polyvagal": mechanism if mechanism else western,
        
        # Spiritual paradigm
        "spiritual": tcm if tcm else mechanism,  # TCM often more poetic
        "contemplative": mechanism if mechanism else western,
        
        # Practical paradigm
        "plain": mechanism if mechanism else western,
        "motivational": western,
        
        # Adaptive (special handling)
        "hybrid": None,  # Special: combines multiple
        "personalized": None,  # Special: user-defined
    }
    
    lens = lens.lower()
    
    if lens == "hybrid":
        # Combine available explanations
        parts = []
        if western:
            parts.append(f"[Western] {western}")
        if tcm:
            parts.append(f"[TCM] {tcm}")
        return " ".join(parts) if parts else mechanism or "Follow the practice with gentle attention."
    
    elif lens == "personalized":
        # Would use user preferences - for now, blend western + somatic
        return mechanism if mechanism else western
    
    elif lens in LENS_TEMPLATES:
        explanation = LENS_TEMPLATES[lens]
        return explanation if explanation else western or mechanism or "Follow the practice with gentle attention."
    
    else:
        # Unknown lens, default to western
        return western or mechanism or "Follow the practice with gentle attention."


def build_technique_section(
    technique: Dict[str, Any], 
    duration: float, 
    lens: str,
    section_type: str = None
) -> SessionSection:
    """Build a session section from a technique with lens-specific explanation."""
    # Determine section type from technique category
    category = technique.get("technique_category", "").lower()
    if section_type is None:
        if "breath" in category:
            section_type = "breathwork"
        elif "movement" in category or "qigong" in category:
            section_type = "movement"
        elif "meditation" in category or "nsdr" in category:
            section_type = "meditation"
        elif "tapping" in category or "somatic" in category:
            section_type = "somatic"
        else:
            section_type = "meditation"
    
    # Get lens-specific explanation
    active_explanation = get_lens_explanation(technique, lens)
    
    return SessionSection(
        type=section_type,
        name=technique.get("technique", "Unknown Technique"),
        duration_minutes=duration,
        instructions=active_explanation,
        cues=[
            f"0:00 - Begin {technique.get('technique', 'practice')}",
            f"{int(duration)//2}:00 - Find your rhythm",
            f"{int(duration)-1}:00 - Prepare to transition",
        ],
        # Lens system fields
        lens_explanation=active_explanation,
        lens_explanation_western=technique.get("lens_explanation_western"),
        lens_explanation_tcm=technique.get("lens_explanation_tcm"),
        mechanism_notes=technique.get("mechanism_notes_simple"),
        technique_id=technique.get("notion_page_id") or str(technique.get("id", "")),
    )


@app.post("/sandbox/generate-session", response_model=SessionOutput)
async def generate_session(request: GenerateSessionRequest):
    """
    Generate a session from a template with LENS-SPECIFIC explanations.
    
    This is the core "engine" that:
    1. Loads Session Template with all relations
    2. Loads Techniques from the new techniques table
    3. Applies the requested LENS (western/tcm/hybrid) to explanations
    4. Applies Safety Rules (hard stops + warnings)
    5. Emits structured output with lens-specific content
    
    LENS SYSTEM:
    - lens="western": Uses Lens Explanation Template (Western)
    - lens="tcm": Uses Lens Explanation Template (TCM)
    - lens="hybrid": Combines both explanations
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
    
    # 3. Load techniques from the new techniques table
    techniques = db.get_techniques()
    
    # 4. Load safety rules
    safety_rules = db.get_safety_rules()
    
    # 5. Load personas for style
    personas = db.get_archetypal_personas()
    persona_style = personas[0].get("persona") if personas else None
    
    # 6. Apply safety rules - collect warnings
    safety_warnings = []
    for rule in safety_rules:
        severity = rule.get("severity", "")
        if severity and severity.lower() in ["high", "warning"]:
            safety_warnings.append(f"{rule.get('rule_name', 'Unknown')}: {rule.get('description', '')}")
    
    # 7. Build session sections using LENS SYSTEM
    sections: List[SessionSection] = []
    remaining_time = request.duration_min
    
    # Normalize lens parameter
    lens = request.lens.lower() if request.lens else "western"
    if lens not in ["western", "tcm", "hybrid"]:
        lens = "western"
    
    # Check for flagship demo: "Hybrid Lens Demo" template
    is_hybrid_demo = "hybrid" in template.get("column_name", "").lower() or "demo" in template.get("column_name", "").lower()
    
    if is_hybrid_demo and techniques:
        # FLAGSHIP DEMO: Movement (TCM Qigong) -> NSDR
        # Find the specific techniques
        qigong = next((t for t in techniques if "qigong" in t.get("technique", "").lower()), None)
        nsdr = next((t for t in techniques if "nsdr" in t.get("technique", "").lower()), None)
        
        if qigong:
            movement_duration = request.duration_min // 2
            sections.append(build_technique_section(qigong, movement_duration, lens, "movement"))
            remaining_time -= movement_duration
        
        if nsdr:
            nsdr_duration = remaining_time
            sections.append(build_technique_section(nsdr, nsdr_duration, lens, "meditation"))
    
    elif techniques:
        # Standard session: use available techniques
        # Opening technique (30% of time)
        opening_duration = max(3, int(request.duration_min * 0.3))
        opening_technique = techniques[0]
        sections.append(build_technique_section(opening_technique, opening_duration, lens))
        remaining_time -= opening_duration
        
        # Main technique (50% of time)
        if len(techniques) > 1:
            main_duration = max(5, int(request.duration_min * 0.5))
            main_technique = techniques[1]
            sections.append(build_technique_section(main_technique, main_duration, lens))
            remaining_time -= main_duration
        
        # Closing (remaining time)
        if remaining_time > 2:
            closing_technique = techniques[0]  # Use first technique for closing
            sections.append(SessionSection(
                type="transition",
                name="Integration & Close",
                duration_minutes=remaining_time,
                instructions="Return to your natural rhythm. Allow the practice to integrate. When ready, gently return to the room.",
                cues=[
                    "0:00 - Begin closing",
                    f"{remaining_time-1}:00 - Session complete",
                ],
                lens_explanation="Take a moment to notice any shifts in your body, breath, or mind.",
            ))
    
    else:
        # Fallback: no techniques available, use legacy breath/movement
        breath_library = db.get_breath_library()
        movements = db.get_movements()
        
        if breath_library:
            opening_duration = max(2, int(request.duration_min * 0.15))
            opening_breath = breath_library[0]
            sections.append(SessionSection(
                type="breathwork",
                name=opening_breath.get("protocol_name", "Centering Breath"),
                duration_minutes=opening_duration,
                instructions=f"Begin with {opening_breath.get('protocol_name', 'deep breathing')}.",
                cues=[f"0:00 - Begin breathing"],
            ))
            remaining_time -= opening_duration
        
        if movements:
            movement_duration = max(5, remaining_time - 2)
            movement = movements[0]
            sections.append(SessionSection(
                type="movement",
                name=movement.get("movement___practice", "Gentle Movement"),
                duration_minutes=movement_duration,
                instructions=f"Practice {movement.get('movement___practice', 'gentle movement')}.",
                cues=[f"0:00 - Begin movement"],
            ))
    
    # 8. Build output with lens information
    breath_library = db.get_breath_library()
    movements = db.get_movements()
    
    return SessionOutput(
        id=str(uuid4()),
        name=template.get("column_name", "Wellness Session"),
        duration_minutes=request.duration_min,
        persona_style=persona_style,
        sections=sections,
        safety_warnings=safety_warnings[:5],
        # LENS SYSTEM - include active lens in output
        lens=lens,
        explanation_level=request.explanation_level or "plain",
        # Legacy fields
        user_id=request.user_id,
        template_name=template.get("column_name", "Unknown"),
        breath_protocols=[b.get("protocol_name", "") for b in (breath_library or [])[:3]],
        movements=[m.get("movement___practice", "") for m in (movements or [])[:3]],
        created_at=datetime.utcnow().isoformat(),
    )


# =============================================================================
# Flagship Demo: Lens System Test
# =============================================================================

@app.get("/sandbox/demo/lens-test")
async def lens_demo_info():
    """
    Information about the flagship lens demo.
    
    This demo proves the lens system works end-to-end by generating
    the same session with different explanatory frameworks.
    """
    return {
        "demo_name": "Hybrid Lens Demo: Movement to Rest",
        "description": "TCM Liver Flow Qigong (15min) -> NSDR (15min)",
        "available_lenses": ["western", "tcm", "hybrid"],
        "usage": {
            "western": "POST /sandbox/demo/generate-flagship?lens=western",
            "tcm": "POST /sandbox/demo/generate-flagship?lens=tcm",
            "hybrid": "POST /sandbox/demo/generate-flagship?lens=hybrid",
        },
        "expected_behavior": "Same session phases, different explanation paragraphs based on lens",
    }


@app.post("/sandbox/demo/generate-flagship")
async def generate_flagship_demo(
    lens: str = "hybrid",
    user_id: str = "demo-user",
    duration_min: int = 30
):
    """
    Generate the flagship lens demo session.
    
    This creates a 2-phase session:
    1. TCM Liver Flow Qigong (Movement) - 15 min
    2. NSDR (Non-Sleep Deep Rest) - 15 min
    
    The explanations change based on the lens parameter:
    - western: Western/mechanistic explanations
    - tcm: Traditional Chinese Medicine framing
    - hybrid: Both explanations included
    """
    db = get_db()
    techniques = db.get_techniques()
    
    # Find the specific techniques
    qigong = next((t for t in techniques if "qigong" in t.get("technique", "").lower()), None)
    nsdr = next((t for t in techniques if "nsdr" in t.get("technique", "").lower()), None)
    
    sections: List[SessionSection] = []
    
    # Phase 1: Movement (TCM Liver Flow Qigong)
    if qigong:
        sections.append(build_technique_section(qigong, duration_min // 2, lens, "movement"))
    else:
        # Fallback if technique not in DB
        sections.append(SessionSection(
            type="movement",
            name="TCM Liver Flow Qigong (Beginner)",
            duration_minutes=duration_min // 2,
            instructions=get_lens_explanation({
                "lens_explanation_western": "Gentle movement + breathing can reduce muscle guarding and support a calmer baseline.",
                "lens_explanation_tcm": "Supports Liver Qi flow: smooth movement, soft eyes, relaxed ribs; avoid strain and keep breath easy.",
                "mechanism_notes_simple": "Gentle mobility + breath synchrony; good for tension patterns."
            }, lens),
            lens_explanation_western="Gentle movement + breathing can reduce muscle guarding and support a calmer baseline.",
            lens_explanation_tcm="Supports Liver Qi flow: smooth movement, soft eyes, relaxed ribs; avoid strain and keep breath easy.",
        ))
    
    # Phase 2: NSDR (Non-Sleep Deep Rest)
    if nsdr:
        sections.append(build_technique_section(nsdr, duration_min // 2, lens, "meditation"))
    else:
        # Fallback if technique not in DB
        sections.append(SessionSection(
            type="meditation",
            name="NSDR (Non-Sleep Deep Rest)",
            duration_minutes=duration_min // 2,
            instructions=get_lens_explanation({
                "lens_explanation_western": "This practice shifts attention inward, reduces cognitive load, and supports parasympathetic settling. Expect calmer breathing, reduced mental chatter, and easier transition into rest.",
                "lens_explanation_tcm": "In TCM language, this supports Shen settling and smooths overactive mind activity; keep gentle, consistent, and avoid forcing.",
                "mechanism_notes_simple": "Low-demand guided rest state; suitable for beginners."
            }, lens),
            lens_explanation_western="This practice shifts attention inward, reduces cognitive load, and supports parasympathetic settling. Expect calmer breathing, reduced mental chatter, and easier transition into rest.",
            lens_explanation_tcm="In TCM language, this supports Shen settling and smooths overactive mind activity; keep gentle, consistent, and avoid forcing.",
        ))
    
    return SessionOutput(
        id=str(uuid4()),
        name="Hybrid Lens Demo: Movement to Rest",
        duration_minutes=duration_min,
        persona_style="Gentle Guide",
        sections=sections,
        safety_warnings=[],  # Low intensity, no warnings needed
        lens=lens,
        explanation_level="plain",
        user_id=user_id,
        template_name="Hybrid Lens Demo",
        breath_protocols=[],
        movements=["TCM Liver Flow Qigong"],
        created_at=datetime.utcnow().isoformat(),
    )


@app.get("/sandbox/techniques")
async def list_techniques(
    category: Optional[str] = None,
    lens: Optional[str] = None
):
    """
    List available techniques, optionally filtered by category or lens.
    
    Categories: Breath, Movement, Somatic, Meditation/NSDR, Tapping, Cognitive, Ritual
    Lenses: Western, TCM, Hybrid
    """
    db = get_db()
    
    if category:
        techniques = db.get_techniques_by_category(category)
    elif lens:
        techniques = db.get_techniques_by_lens(lens)
    else:
        techniques = db.get_techniques()
    
    return {
        "count": len(techniques),
        "techniques": [
            {
                "id": t.get("id"),
                "notion_page_id": t.get("notion_page_id"),
                "technique": t.get("technique"),
                "category": t.get("technique_category"),
                "objective": t.get("objective"),
                "lens_availability": t.get("lens_availability"),
                "intensity_band": t.get("intensity_band"),
                "default_duration_min": t.get("default_duration_min"),
            }
            for t in techniques
        ]
    }


@app.get("/sandbox/techniques/{technique_id}")
async def get_technique(technique_id: str):
    """Get a single technique with all lens explanations."""
    db = get_db()
    techniques = db.get_techniques()
    
    technique = None
    for t in techniques:
        if str(t.get("id")) == technique_id or t.get("notion_page_id") == technique_id:
            technique = t
            break
    
    if not technique:
        raise HTTPException(status_code=404, detail="Technique not found")
    
    return technique


@app.get("/sandbox/evidence-sources")
async def list_evidence_sources():
    """List all evidence sources."""
    db = get_db()
    evidence = db.get_evidence_sources()
    
    return {
        "count": len(evidence),
        "evidence_sources": evidence
    }


# =============================================================================
# Lens Registry - Infinite, User-Creatable Lenses
# =============================================================================

@app.get("/sandbox/lenses")
async def list_lenses(active_only: bool = True):
    """
    List all available lenses.
    
    The lens system supports infinite, user-creatable explanatory frameworks.
    Each lens provides a different way to explain the same technique.
    """
    db = get_db()
    
    try:
        lenses = db.get_all_lenses(active_only=active_only)
        
        return {
            "count": len(lenses),
            "paradigm_families": ["scientific", "traditional", "somatic", "spiritual", "practical", "adaptive"],
            "lenses": [
                {
                    "slug": l.get("lens_slug"),
                    "name": l.get("lens_name"),
                    "description": l.get("lens_description"),
                    "paradigm": l.get("paradigm_family"),
                    "language_style": l.get("language_style"),
                    "cultural_origin": l.get("cultural_origin"),
                    "icon": l.get("icon"),
                    "color": l.get("color"),
                    "is_system": l.get("is_system", True),
                }
                for l in lenses
            ]
        }
    except Exception:
        # Fallback if lens_definitions table doesn't exist yet
        return {
            "count": 14,
            "paradigm_families": ["scientific", "traditional", "somatic", "spiritual", "practical", "adaptive"],
            "lenses": [
                {"slug": "western", "name": "Western Scientific", "icon": "🔬", "paradigm": "scientific"},
                {"slug": "clinical", "name": "Clinical/Medical", "icon": "🏥", "paradigm": "scientific"},
                {"slug": "athletic", "name": "Athletic/Performance", "icon": "🏃", "paradigm": "performance"},
                {"slug": "tcm", "name": "Traditional Chinese Medicine", "icon": "☯️", "paradigm": "traditional"},
                {"slug": "ayurvedic", "name": "Ayurvedic", "icon": "🕉️", "paradigm": "traditional"},
                {"slug": "yogic", "name": "Yogic/Tantric", "icon": "🧘", "paradigm": "traditional"},
                {"slug": "somatic", "name": "Somatic/Body-Based", "icon": "🫀", "paradigm": "somatic"},
                {"slug": "polyvagal", "name": "Polyvagal-Informed", "icon": "🌊", "paradigm": "somatic"},
                {"slug": "spiritual", "name": "Spiritual/Energetic", "icon": "✨", "paradigm": "spiritual"},
                {"slug": "contemplative", "name": "Contemplative/Mindfulness", "icon": "🪷", "paradigm": "spiritual"},
                {"slug": "plain", "name": "Plain Language", "icon": "💬", "paradigm": "practical"},
                {"slug": "motivational", "name": "Motivational/Coaching", "icon": "🎯", "paradigm": "practical"},
                {"slug": "hybrid", "name": "Hybrid/Adaptive", "icon": "🔄", "paradigm": "adaptive"},
                {"slug": "personalized", "name": "Personalized", "icon": "👤", "paradigm": "adaptive"},
            ],
            "note": "Lens registry table not yet created. Run lens_registry_schema.sql in Supabase."
        }


@app.get("/sandbox/lenses/{lens_slug}")
async def get_lens(lens_slug: str):
    """Get details for a specific lens."""
    db = get_db()
    
    try:
        lens = db.get_lens_by_slug(lens_slug)
        if not lens:
            raise HTTPException(status_code=404, detail=f"Lens '{lens_slug}' not found")
        return lens
    except Exception as e:
        if "not found" in str(e).lower():
            raise
        # Fallback for missing table
        raise HTTPException(status_code=404, detail=f"Lens registry not yet created. Run lens_registry_schema.sql")


@app.get("/sandbox/techniques/{technique_id}/lenses")
async def get_technique_lenses(technique_id: str):
    """
    Get all lens explanations for a specific technique.
    
    Returns the technique with explanations in every available lens.
    """
    db = get_db()
    
    # Get base technique
    techniques = db.get_techniques()
    technique = None
    for t in techniques:
        if str(t.get("id")) == technique_id or t.get("notion_page_id") == technique_id:
            technique = t
            break
    
    if not technique:
        raise HTTPException(status_code=404, detail="Technique not found")
    
    try:
        # Get all lens explanations
        explanations = db.get_technique_lens_explanations(technique["id"])
        
        return {
            "technique": technique.get("technique"),
            "technique_id": technique.get("id"),
            "category": technique.get("technique_category"),
            "explanations": {
                exp.get("lens_definitions", {}).get("lens_slug"): {
                    "lens_name": exp.get("lens_definitions", {}).get("lens_name"),
                    "explanation": exp.get("explanation_template"),
                    "mechanism_notes": exp.get("mechanism_notes"),
                    "icon": exp.get("lens_definitions", {}).get("icon"),
                }
                for exp in explanations
            }
        }
    except Exception:
        # Fallback: return explanations from technique table columns
        return {
            "technique": technique.get("technique"),
            "technique_id": technique.get("id"),
            "category": technique.get("technique_category"),
            "explanations": {
                "western": {
                    "lens_name": "Western Scientific",
                    "explanation": technique.get("lens_explanation_western"),
                    "mechanism_notes": technique.get("mechanism_notes_simple"),
                    "icon": "🔬"
                },
                "tcm": {
                    "lens_name": "Traditional Chinese Medicine",
                    "explanation": technique.get("lens_explanation_tcm"),
                    "icon": "☯️"
                }
            },
            "note": "Lens registry not yet created. Only Western/TCM available from technique table."
        }


@app.post("/sandbox/user/lens-preferences")
async def update_user_lens_preferences(
    user_id: str,
    preferred_lenses: List[str],
    avoided_lenses: Optional[List[str]] = None
):
    """
    Update a user's lens preferences.
    
    Used by the adaptive AI to select appropriate lenses.
    """
    db = get_db()
    
    # This would update user_lens_preferences table
    # For now, return acknowledgment
    return {
        "user_id": user_id,
        "preferred_lenses": preferred_lenses,
        "avoided_lenses": avoided_lenses or [],
        "status": "preferences_recorded",
        "note": "Preferences will influence AI lens selection"
    }


@app.post("/sandbox/user/lens-context")
async def update_user_lens_context(
    user_id: str,
    mood_state: Optional[str] = None,
    energy_level: Optional[int] = None,
    receptivity: Optional[str] = None
):
    """
    Update user context for adaptive lens selection.
    
    The AI uses this context to select the most appropriate lens(es).
    """
    context_data = {}
    if mood_state:
        context_data["mood_state"] = mood_state
    if energy_level:
        context_data["energy_level"] = energy_level
    if receptivity:
        context_data["receptivity"] = receptivity
    
    # Suggest lens based on context
    suggested_lens = "plain"  # Default
    reasoning = "Default selection"
    
    if energy_level and energy_level < 4:
        suggested_lens = "somatic"
        reasoning = "Low energy suggests body-based, gentle approach"
    elif energy_level and energy_level > 7:
        suggested_lens = "athletic"
        reasoning = "High energy aligned with performance framing"
    elif mood_state and mood_state.lower() in ["low", "sad", "anxious"]:
        suggested_lens = "somatic"
        reasoning = "Current mood benefits from body-based, trauma-informed language"
    elif receptivity == "high":
        suggested_lens = "spiritual"
        reasoning = "High receptivity opens space for deeper frameworks"
    
    context_data["ai_suggested_lens"] = suggested_lens
    context_data["ai_reasoning"] = reasoning
    
    return {
        "user_id": user_id,
        "context_date": datetime.utcnow().date().isoformat(),
        "ai_suggested_lens": suggested_lens,
        "ai_reasoning": reasoning,
        "context_received": context_data,
        "note": "AI suggestion can be overridden by user preference"
    }


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



