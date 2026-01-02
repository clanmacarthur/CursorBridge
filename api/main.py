"""
Core App API - FastAPI Application

Endpoints:
- POST /api/sync/notion - Sync content from Notion to Supabase
- POST /api/logs/checkin - Log a daily check-in
- GET /api/query/{table} - Query any table
"""

import os
import sys
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.database import get_db
from shared.auth import validate_jwt, optional_jwt
from shared.realtime import publish_content_update, publish_sync_complete
from shared.templates import get_all_templates, get_template_by_id, get_templates_by_category
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Wellness App API",
    description="Core API for the wellness application",
    version="0.1.0",
)

# CORS middleware for Main App access
ALLOWED_ORIGINS = [
    "http://localhost:8080",      # Main App dev
    "http://localhost:3000",      # Local testing
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

class SyncRequest(BaseModel):
    scope: List[str]  # List of table names to sync


class SyncResponse(BaseModel):
    success: bool
    synced: Dict[str, int]  # table -> row count
    errors: List[str]


class CheckinRequest(BaseModel):
    user_id: str
    date: str  # YYYY-MM-DD
    block_id: str
    values: Dict[str, Any]  # {"completed": [...], "magnitude": {...}}


class CheckinResponse(BaseModel):
    success: bool
    checkin_id: Optional[int] = None


class QueryResponse(BaseModel):
    table: str
    count: int
    data: List[Dict[str, Any]]


# =============================================================================
# Health Check
# =============================================================================

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "wellness-api", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Detailed health check."""
    try:
        db = get_db()
        # Quick test query
        db.client.table("system_manifest").select("id").limit(1).execute()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
    }


# =============================================================================
# Sync Endpoints
# =============================================================================

@app.post("/api/sync/notion", response_model=SyncResponse)
async def sync_notion(request: SyncRequest):
    """
    Sync content from Notion to Supabase.
    
    This triggers the CursorBridge sync for specified tables.
    """
    from cb.bridge import notion_to_db
    
    # Mapping of table names to Notion database IDs
    NOTION_DB_IDS = {
        "system_manifest": "2d7c47c61e2180fd9c68f8a73fd28232",
        "attribute_taxonomy": "2d5c47c61e2180ae9a53d844719cbcd7",
        "programme_profiles": "2d5c47c61e21802caf3be7cd77aef164",
        "dashboard_blocks": "2d4c47c61e2180d486e8f69ad99e1e87",
        "safety_rules": "2c8c47c61e2180bf8277e229b86ce5b3",
        "session_templates": "2d6c47c61e21803da929dac07cfdc8d8",
        "breath_library": "2cac47c61e21807381dcf0f9fbb653b6",
        "movements_system": "2cdc47c61e2180c2a4a5c5690d74daa2",
        "archetypal_personas": "2cdc47c6-1e21-80c9-bc28-efc7737d8646",
        "nutrition_and_food": "2d6c47c61e2180abafddfb3004456856",
        # Add more as needed
    }
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise HTTPException(status_code=500, detail="Supabase credentials not configured")
    
    connection_string = f"{supabase_url}|{supabase_key}"
    
    synced = {}
    errors = []
    
    for table in request.scope:
        if table not in NOTION_DB_IDS:
            errors.append(f"Unknown table: {table}")
            continue
        
        try:
            result = notion_to_db(
                database_id=NOTION_DB_IDS[table],
                target="supabase",
                connection_string=connection_string,
                table_name=table,
                dry_run=False,
            )
            synced[table] = result["rows_inserted"]
        except Exception as e:
            errors.append(f"{table}: {str(e)}")
    
    # Publish realtime event for Main App
    if synced:
        publish_sync_complete(
            tables_synced=list(synced.keys()),
            total_rows=sum(synced.values()),
        )
    
    return SyncResponse(
        success=len(errors) == 0,
        synced=synced,
        errors=errors,
    )


# =============================================================================
# Logging Endpoints
# =============================================================================

@app.post("/api/logs/checkin", response_model=CheckinResponse)
async def log_checkin(
    request: CheckinRequest,
    user: dict = Depends(optional_jwt),  # Optional auth - uses request.user_id if no JWT
):
    """
    Log a daily check-in (checkboxes + sliders/knobs).
    
    Example request:
    {
        "user_id": "USER123",
        "date": "2025-12-30",
        "block_id": "BLOCK_NUTRITION_CHECKIN",
        "values": {
            "completed": ["hydration", "protein_target"],
            "magnitude": {"sleep_quality": 7, "stress_level": 4}
        }
    }
    """
    # Use authenticated user_id if available, otherwise use request.user_id
    user_id = user["id"] if user else request.user_id
    
    db = get_db()
    
    # First, ensure the user_checkins table exists
    # For now, we'll store as JSON in a generic logs table
    try:
        checkin_data = {
            "user_id": user_id,
            "checkin_date": request.date,
            "block_id": request.block_id,
            "completed_items": request.values.get("completed", []),
            "magnitude_values": request.values.get("magnitude", {}),
            "created_at": datetime.utcnow().isoformat(),
        }
        
        # Insert into user_checkins table (you'll need to create this)
        result = db.insert("user_checkins", checkin_data)
        
        return CheckinResponse(success=True, checkin_id=result.get("id"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# Query Endpoints
# =============================================================================

@app.get("/api/query/{table}", response_model=QueryResponse)
async def query_table(table: str, limit: int = 100):
    """
    Query any table in the database.
    
    Example: GET /api/query/attribute_taxonomy?limit=50
    """
    ALLOWED_TABLES = [
        # Library backbone
        "system_manifest", "attribute_taxonomy", "programme_profiles",
        "dashboard_blocks", "safety_rules", "session_templates",
        "breath_library", "movements_system", "archetypal_personas",
        "nutrition_and_food", "nutrition_intake", "supplement_interactions",
        "mappings", "rules_gating", "session_types", "sound_vibration",
        "light_colour", "symbols_index", "sacred_geometry",
        "deities_archetypes", "elemental_framework", "organ_emotion_system",
        "nutrition_protocols", "chakra_systems", "meridian_system",
        # Automation backbone (new)
        "control_definitions", "control_packs", "control_pack_items",
        "profile_pack_map", "default_weights", "coupling_rules",
        "derived_metrics", "questionnaires", "questionnaire_questions",
    ]
    
    if table not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail=f"Table '{table}' not allowed")
    
    db = get_db()
    data = db.get_all(table, limit=limit)
    
    return QueryResponse(table=table, count=len(data), data=data)


@app.get("/api/query/{table}/{id}")
async def query_table_by_id(table: str, id: int):
    """Get a specific row by ID."""
    db = get_db()
    row = db.get_by_id(table, id)
    
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    
    return row


# =============================================================================
# Template Endpoints
# =============================================================================

@app.get("/api/templates")
async def list_templates(category: Optional[str] = None):
    """
    List available dashboard templates.
    
    Query params:
        category: Optional filter (wellness, fitness, meditation, nutrition)
    
    Returns:
        List of template definitions with blocks
    """
    if category:
        templates = get_templates_by_category(category)
    else:
        templates = get_all_templates()
    
    return {
        "count": len(templates),
        "templates": templates,
    }


@app.get("/api/templates/{template_id}")
async def get_template(template_id: str):
    """Get a specific dashboard template by ID."""
    template = get_template_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
    
    return template


# =============================================================================
# Content Field Documentation
# =============================================================================

@app.get("/api/schema/{table}")
async def get_table_schema(table: str):
    """
    Get field documentation for a content table.
    
    Useful for Main App to understand what fields are available.
    """
    SCHEMAS = {
        "programme_profiles": {
            "description": "Wellness programme definitions (lenses/doctrine presets)",
            "fields": {
                "id": "Auto-generated Supabase ID",
                "notion_page_id": "Original Notion page ID (for relations)",
                "programme_profile___title": "Programme name (e.g., 'Yoga Practitioner')",
                "primary_doctrine___select": "Primary approach (Clinical, Athletic, Somatic, Ritual, Spiritual)",
                "default_depth___select": "Attribute depth (Category, Subcategory, Capability, Parameter)",
                "default_strictness___select": "Rule strictness (Loose, Normal, Strict)",
                "notes___text": "Additional notes",
                "primary_attribute_focus___relation___attribute_taxonomy__db_": "Related attribute (Notion page ID)",
                "secondary_attribute_focus___relation___attribute_taxonomy__db_": "Secondary attribute (Notion page ID)",
            },
            "sample_query": "GET /api/query/programme_profiles?limit=5"
        },
        "breath_library": {
            "description": "Breath protocol library for sessions",
            "fields": {
                "id": "Auto-generated Supabase ID",
                "notion_page_id": "Original Notion page ID",
                "protocol_name": "Name of breath protocol (e.g., 'Physiological Sigh')",
                "typical_use": "When to use this protocol",
                "activation_level": "Energy level (Calming, Neutral, Activating)",
                "primary_element": "TCM element association",
                "safety_tier": "Safety classification",
                "contraindications": "Who should avoid this",
                "notes": "Additional guidance",
            },
            "sample_query": "GET /api/query/breath_library?limit=5"
        },
        "movements_system": {
            "description": "Movement and practice library",
            "fields": {
                "id": "Auto-generated Supabase ID",
                "notion_page_id": "Original Notion page ID",
                "movement___practice": "Name of movement (e.g., 'Qigong Silk Reeling')",
                "movement_family": "Category (Yoga, Tai Chi, Qigong, etc.)",
                "primary_effect": "Main benefit",
                "intensity": "Physical intensity level",
                "primary_body_region": "Target area",
                "nervous_system_bias": "Parasympathetic/Sympathetic",
                "contraindications___safety_notes": "Safety considerations",
                "notes": "Additional guidance",
            },
            "sample_query": "GET /api/query/movements_system?limit=5"
        },
        "session_templates": {
            "description": "Session recipes for the sandbox generator",
            "fields": {
                "id": "Auto-generated Supabase ID",
                "notion_page_id": "Original Notion page ID",
                "column_name": "Template name",
                "session_type____l1_": "Type of session (linked)",
                "style____nl_": "Persona style (linked)",
                "primary_intent____l1_": "Primary goal (linked)",
                "breath_protocols____nl_": "Breath protocols (linked)",
                "movements____nl_": "Movements (linked)",
                "default_duration__min_": "Default duration in minutes",
                "pause_style": "Pause between sections (Minimal, Moderate, Long)",
                "script_strictness": "How closely to follow script",
            },
            "sample_query": "GET /api/query/session_templates?limit=5"
        },
        "archetypal_personas": {
            "description": "AI persona styles for script generation",
            "fields": {
                "id": "Auto-generated Supabase ID",
                "notion_page_id": "Original Notion page ID",
                "persona": "Persona name (e.g., 'Alan Watts-like')",
                "cognitive_style": "Thinking approach (Analytical, Narrative, Minimal, Reflective)",
                "language_tone": "Speaking style (Clinical-calm, Warm, Poetic, Direct)",
                "metaphor_density": "Use of metaphors (None, Low, Medium, High)",
                "lineage___influence": "Philosophical influences",
                "notes": "Character notes",
            },
            "sample_query": "GET /api/query/archetypal_personas?limit=5"
        },
    }
    
    if table not in SCHEMAS:
        raise HTTPException(
            status_code=404, 
            detail=f"Schema not documented for '{table}'. Available: {list(SCHEMAS.keys())}"
        )
    
    return SCHEMAS[table]


# =============================================================================
# Run the app
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)



