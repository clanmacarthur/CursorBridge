# Lens System Setup Guide

This document explains how to set up and test the Evidence Sources + Techniques "lens" system.

---

## Step 1: Apply SQL Schema to Supabase

Go to your Supabase Dashboard → SQL Editor → New Query and paste the contents of:

```
evidence_techniques_schema.sql
```

This will:
1. Create the `evidence_sources` table
2. Create the `techniques` table
3. Seed 4 evidence sources
4. Seed 4 techniques (NSDR, EFT Tapping, Wim Hof, TCM Qigong)
5. Create a flagship demo session template

---

## Step 2: Restart the API Servers

```bash
# Terminal 1 - Core API
cd C:\code\CursorBridge
set SUPABASE_URL=https://dshwdxhycdrtemaxrupu.supabase.co
set SUPABASE_KEY=your_key_here
set NOTION_TOKEN=your_token_here
python run_api.py

# Terminal 2 - Sandbox API
cd C:\code\CursorBridge
set SUPABASE_URL=https://dshwdxhycdrtemaxrupu.supabase.co
set SUPABASE_KEY=your_key_here
python run_sandbox.py
```

---

## Step 3: Test the Lens System

### A. Get Demo Info
```bash
curl http://localhost:3001/sandbox/demo/lens-test
```

### B. Generate Flagship Demo with Different Lenses

**Western Lens:**
```bash
curl -X POST "http://localhost:3001/sandbox/demo/generate-flagship?lens=western"
```

**TCM Lens:**
```bash
curl -X POST "http://localhost:3001/sandbox/demo/generate-flagship?lens=tcm"
```

**Hybrid Lens (Both):**
```bash
curl -X POST "http://localhost:3001/sandbox/demo/generate-flagship?lens=hybrid"
```

### C. Query Techniques
```bash
# List all techniques
curl http://localhost:3001/sandbox/techniques

# Filter by lens availability
curl "http://localhost:3001/sandbox/techniques?lens=tcm"

# Filter by category
curl "http://localhost:3001/sandbox/techniques?category=Movement"
```

### D. Query Evidence Sources
```bash
curl http://localhost:3001/sandbox/evidence-sources
```

### E. Full Session Generation with Lens
```bash
curl -X POST http://localhost:3001/sandbox/generate-session \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "programme_profile_id": "1",
    "session_template_id": "1",
    "duration_min": 30,
    "lens": "hybrid",
    "explanation_level": "plain"
  }'
```

---

## What You Should See

### Same Session, Different Explanations

**Western Lens Output:**
```
Section 1: TCM Liver Flow Qigong
Instructions: "Gentle movement + breathing can reduce muscle guarding and support a calmer baseline."

Section 2: NSDR
Instructions: "This practice shifts attention inward, reduces cognitive load, and supports parasympathetic settling..."
```

**TCM Lens Output:**
```
Section 1: TCM Liver Flow Qigong
Instructions: "Supports Liver Qi flow: smooth movement, soft eyes, relaxed ribs; avoid strain and keep breath easy."

Section 2: NSDR
Instructions: "In TCM language, this supports Shen settling and smooths overactive mind activity..."
```

**Hybrid Lens Output:**
```
Section 1: TCM Liver Flow Qigong
Instructions: "[Western] Gentle movement + breathing can reduce muscle guarding... [TCM] Supports Liver Qi flow: smooth movement, soft eyes..."

Section 2: NSDR
Instructions: "[Western] This practice shifts attention inward... [TCM] In TCM language, this supports Shen settling..."
```

---

## Tables Created

| Table | Rows | Purpose |
|-------|------|---------|
| `evidence_sources` | 4 | Research, guidelines, and traditional references |
| `techniques` | 4 | Core techniques with lens-specific templates |

---

## New API Endpoints

### Sandbox API (Port 3001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sandbox/demo/lens-test` | GET | Info about the flagship demo |
| `/sandbox/demo/generate-flagship` | POST | Generate demo with lens param |
| `/sandbox/techniques` | GET | List all techniques |
| `/sandbox/techniques?lens=tcm` | GET | Filter by lens |
| `/sandbox/techniques/{id}` | GET | Get single technique |
| `/sandbox/evidence-sources` | GET | List all evidence sources |
| `/sandbox/generate-session` | POST | Now accepts `lens` and `explanation_level` |

### Core API (Port 3000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/query/techniques` | GET | Query techniques table |
| `/api/query/evidence_sources` | GET | Query evidence sources table |
| `/api/schema/techniques` | GET | Field documentation |
| `/api/schema/evidence_sources` | GET | Field documentation |

---

## Architecture Notes

The lens system works by storing multiple explanation templates per technique:

```
Technique: NSDR (Non-Sleep Deep Rest)
├── lens_explanation_western: "This practice shifts attention inward..."
├── lens_explanation_tcm: "In TCM language, this supports Shen settling..."
└── mechanism_notes_simple: "Low-demand guided rest state; suitable for beginners."
```

When generating a session:
1. Request includes `lens: "western" | "tcm" | "hybrid"`
2. Session builder fetches technique data
3. `get_lens_explanation()` selects the appropriate template
4. Output includes the lens-specific explanation in `instructions`
5. All three templates are also returned for UI flexibility

---

## Success Criteria

✅ Same session phases, different explanation paragraphs based on lens
✅ Technique row displays linked Evidence Sources
✅ Evidence Sources show reverse-linked Techniques
✅ A single button produces a session that feels meaningfully different by lens
✅ No new databases needed - just two new tables

---

## Next Steps

1. Apply the SQL schema
2. Restart the servers
3. Run the test commands
4. Verify lens-switching works
5. Inform Main App AI of the new capabilities




