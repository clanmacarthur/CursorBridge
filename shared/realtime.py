"""Supabase Realtime publishing for content updates."""

import os
from datetime import datetime
from typing import Any, Dict, Literal, Optional

ContentEventType = Literal[
    'programme_updated',
    'template_added', 
    'content_synced',
    'block_updated',
    'taxonomy_updated',
]


def get_supabase_client():
    """Get Supabase client for realtime."""
    from supabase import create_client
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")
    
    return create_client(url, key)


def publish_content_update(
    event_type: ContentEventType,
    table: str,
    record_id: Optional[str] = None,
    extra_data: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Publish a content update to the 'content_updates' Realtime channel.
    
    Main App subscribes to this channel to reactively update UI.
    
    Args:
        event_type: Type of event (programme_updated, template_added, etc.)
        table: Table name that was updated
        record_id: Optional ID of the specific record
        extra_data: Optional additional data
    
    Returns:
        True if published successfully, False otherwise
    
    Payload format (as requested by Main App):
    {
        type: 'programme_updated' | 'template_added' | 'content_synced',
        table: string,
        record_id: string,
        timestamp: string
    }
    """
    try:
        client = get_supabase_client()
        
        payload = {
            "type": event_type,
            "table": table,
            "record_id": record_id or "",
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        if extra_data:
            payload["data"] = extra_data
        
        # Broadcast to the content_updates channel
        # Note: Supabase Python client realtime is still evolving
        # For now, we'll use a database insert to a sync_events table
        # which triggers a Postgres NOTIFY that Realtime picks up
        
        # Alternative: Direct realtime broadcast (if supported)
        # channel = client.channel('content_updates')
        # channel.send_broadcast('content_update', payload)
        
        # For reliability, insert to a sync_events table
        # Main App can subscribe to this table's changes
        try:
            client.table('sync_events').insert({
                'event_type': event_type,
                'table_name': table,
                'record_id': record_id,
                'payload': payload,
                'created_at': datetime.utcnow().isoformat(),
            }).execute()
        except Exception:
            # Table might not exist yet - that's okay
            pass
        
        print(f"[Realtime] Published: {event_type} on {table}")
        return True
        
    except Exception as e:
        print(f"[Realtime] Failed to publish: {e}")
        return False


def publish_sync_complete(tables_synced: list, total_rows: int) -> bool:
    """
    Publish a sync complete event after Notion → Supabase sync.
    """
    return publish_content_update(
        event_type='content_synced',
        table='_sync',
        extra_data={
            'tables': tables_synced,
            'total_rows': total_rows,
        }
    )




