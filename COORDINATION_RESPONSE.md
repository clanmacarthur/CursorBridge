# COORDINATION RESPONSE - CursorBridge → Main App
=====================================

## 1. DASHBOARD TEMPLATES ✅ IMPLEMENTED

**New Endpoint:** `GET /api/templates`

```bash
# List all templates
curl http://localhost:3000/api/templates

# Filter by category
curl http://localhost:3000/api/templates?category=wellness

# Get specific template
curl http://localhost:3000/api/templates/daily-wellness-check
```

**Available Templates:**

| ID | Name | Category | Blocks |
|----|------|----------|--------|
| `daily-wellness-check` | Daily Wellness Check | wellness | 5 blocks (mood, sleep, energy, stress sliders + trends chart) |
| `breath-movement` | Breath & Movement | fitness | 3 blocks (session player + feeling + type) |
| `meditation-journal` | Meditation Journal | meditation | 7 blocks (timer, quality, technique, notes, stats) |
| `nutrition-tracker` | Nutrition Tracker | nutrition | 4 blocks (hydration toggles, meals, protein, timeline) |
| `sleep-tracker` | Sleep Tracker | wellness | 6 blocks (times, quality, energy, chart) |

**Template Format:**
```json
{
  "id": "daily-wellness-check",
  "name": "Daily Wellness Check",
  "description": "Track your daily mood, sleep quality, energy, and stress levels",
  "category": "wellness",
  "icon": "heart",
  "blocks": [
    {
      "block_type": "slider",
      "config": {
        "label": "Mood",
        "min": 1,
        "max": 10,
        "step": 1,
        "default": 5,
        "low_label": "Low",
        "high_label": "Great",
        "color": "#f59e0b"
      },
      "position": {"x": 0, "y": 0, "w": 6, "h": 2}
    }
    // ... more blocks
  ]
}
```

---

## 2. SESSION PLAYER DATA ✅ UPDATED

**Endpoint:** `POST /sandbox/generate-session`

**Output Format (matches your request!):**
```json
{
  "id": "uuid-here",
  "name": "Morning Energy Flow",
  "duration_minutes": 15,
  "persona_style": "Alan Watts-like",
  "sections": [
    {
      "type": "breathwork",
      "name": "Physiological Sigh",
      "duration_minutes": 2.5,
      "instructions": "Begin with Physiological Sigh. Find a comfortable position...",
      "audio_url": null,
      "cues": [
        "0:00 - Begin Physiological Sigh",
        "0:30 - Deepen your breath",
        "1:30 - Prepare to transition"
      ]
    },
    {
      "type": "movement",
      "name": "Qigong Silk Reeling",
      "duration_minutes": 7.5,
      "instructions": "Practice Qigong Silk Reeling. Move mindfully...",
      "cues": [
        "0:00 - Begin Qigong Silk Reeling",
        "3:00 - Find your rhythm",
        "5:30 - Begin to slow down"
      ]
    },
    {
      "type": "breathwork",
      "name": "Box Breathing",
      "duration_minutes": 5,
      "instructions": "Return to your natural breath. Allow the practice to integrate.",
      "cues": [
        "0:00 - Return to natural breathing",
        "4:00 - Begin to return to the room",
        "5:00 - Session complete"
      ]
    }
  ],
  "safety_warnings": ["Avoid if experiencing acute anxiety", "..."],
  "user_id": "user-uuid",
  "template_name": "Morning Energy Flow",
  "breath_protocols": ["Physiological Sigh", "Box Breathing", "4-7-8"],
  "movements": ["Qigong Silk Reeling", "Sun Salutation", "Joint Mobility"],
  "created_at": "2025-12-30T15:30:00Z"
}
```

**Section Types:**
- `breathwork` - Breath protocol sections
- `movement` - Movement/exercise sections
- `meditation` - Stillness/awareness sections
- `transition` - Brief transitions between sections

**Cues Format:**
- Timed cues for your player UI
- Format: `"MM:SS - Instruction text"`
- Perfect for displaying prompts during playback

---

## 3. CONTENT BLOCK DATA ✅ DOCUMENTED

**New Endpoint:** `GET /api/schema/{table}`

Returns field documentation for content tables:

```bash
curl http://localhost:3000/api/schema/programme_profiles
curl http://localhost:3000/api/schema/breath_library
curl http://localhost:3000/api/schema/movements_system
```

### Programme Profiles Fields:
| Field | Description |
|-------|-------------|
| `id` | Supabase UUID |
| `notion_page_id` | Original Notion page ID |
| `programme_profile___title` | Programme name (e.g., 'Yoga Practitioner') |
| `primary_doctrine___select` | Primary approach (Clinical, Athletic, Somatic, Ritual, Spiritual) |
| `default_depth___select` | Attribute depth level |
| `default_strictness___select` | Rule strictness (Loose, Normal, Strict) |
| `primary_attribute_focus___relation___*` | Related attribute (Notion page ID) |

### Breath Library Fields:
| Field | Description |
|-------|-------------|
| `id` | Supabase UUID |
| `protocol_name` | Name (e.g., 'Physiological Sigh', 'Box Breathing') |
| `typical_use` | When to use this protocol |
| `activation_level` | Calming, Neutral, or Activating |
| `primary_element` | TCM element association |
| `safety_tier` | Safety classification |
| `contraindications` | Who should avoid this |

### Movements System Fields:
| Field | Description |
|-------|-------------|
| `id` | Supabase UUID |
| `movement___practice` | Name (e.g., 'Qigong Silk Reeling') |
| `movement_family` | Category (Yoga, Tai Chi, Qigong, etc.) |
| `primary_effect` | Main benefit |
| `intensity` | Physical intensity level |
| `primary_body_region` | Target body area |
| `nervous_system_bias` | Parasympathetic/Sympathetic |

---

## 4. INSIGHTS/CORRELATIONS

**Current Status:** No analytics endpoints yet.

**Recommendation:** Main App should calculate correlations locally from `block_data`.

**Why:**
- Block data lives in your tables (you own it)
- Correlations are user-specific
- Real-time feedback is better calculated client-side or in Nuxt server routes
- Supabase has great aggregate functions you can use directly

**Future Option:** If you need cross-user analytics (anonymized trends), we can add:
```
GET /api/insights/trends?metric=mood&period=30d
GET /api/insights/correlations?block1=sleep&block2=energy
```

Let us know if you want these added!

---

## 5. TEMPLATE STORAGE

**Answer:** Templates are stored in CursorBridge (`shared/templates.py`)

**Why:**
- Templates reference our content (programmes, breath protocols, movements)
- Keeps content and templates in sync
- You fetch via API, we maintain

**Your Workflow:**
1. `GET /api/templates` → List available templates
2. User picks one → You create a dashboard in your DB with copied blocks
3. Dashboard is now yours to modify

**Adding New Templates:**
- Request via coordination, we add to `shared/templates.py`
- Or: Store custom templates in your `dashboards` table with `is_template: true`

---

## ANSWERS TO YOUR QUESTIONS

### Which templates make sense to start with?
1. **Daily Wellness Check** - Most universal, good for testing sliders + charts
2. **Meditation Journal** - Tests timer component + stats
3. **Breath & Movement** - Tests session player integration

### Content to know for blocks?
- All content has `notion_page_id` for relation tracking
- Use `GET /api/schema/{table}` to discover fields
- Use `GET /api/query/{table}?limit=5` to see sample data

### Template storage approach?
- **Static templates:** We store, you fetch via API
- **User-created templates:** You store in your `dashboards` table
- **Hybrid:** Fork our templates into your DB when user customizes

---

## NEW ENDPOINTS SUMMARY

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/templates` | List all dashboard templates |
| GET | `/api/templates?category=X` | Filter templates by category |
| GET | `/api/templates/{id}` | Get specific template |
| GET | `/api/schema/{table}` | Get field documentation |
| POST | `/sandbox/generate-session` | Generate session (updated format!) |

---

## NEXT STEPS

1. **Test the templates endpoint:**
   ```bash
   curl http://localhost:3000/api/templates
   ```

2. **Test session generation with new format:**
   ```bash
   curl -X POST http://localhost:3000/sandbox/generate-session \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test", "template_id": "your-template-id", "duration_min": 15}'
   ```

3. **Let us know if you need:**
   - Additional templates
   - More fields in session output
   - Analytics endpoints
   - Content filtering/search

Ready to help build the player UI! 🎯



