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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.database import get_db
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Wellness App API",
    description="Core API for the wellness application",
    version="0.1.0",
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    
    return SyncResponse(
        success=len(errors) == 0,
        synced=synced,
        errors=errors,
    )


# =============================================================================
# Logging Endpoints
# =============================================================================

@app.post("/api/logs/checkin", response_model=CheckinResponse)
async def log_checkin(request: CheckinRequest):
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
    db = get_db()
    
    # First, ensure the user_checkins table exists
    # For now, we'll store as JSON in a generic logs table
    try:
        checkin_data = {
            "user_id": request.user_id,
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
        "system_manifest", "attribute_taxonomy", "programme_profiles",
        "dashboard_blocks", "safety_rules", "session_templates",
        "breath_library", "movements_system", "archetypal_personas",
        "nutrition_and_food", "nutrition_intake", "supplement_interactions",
        "mappings", "rules_gating", "session_types", "sound_vibration",
        "light_colour", "symbols_index", "sacred_geometry",
        "deities_archetypes", "elemental_framework", "organ_emotion_system",
        "nutrition_protocols", "chakra_systems", "meridian_system",
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
# Run the app
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)

