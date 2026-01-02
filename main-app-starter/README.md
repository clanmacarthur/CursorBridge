# Wellness App - Main App Starter

Vue 3 + Nuxt 3 starter template for the wellness application.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Open http://localhost:8080

## Project Structure

```
main-app-starter/
├── nuxt.config.ts          # Nuxt configuration
├── app.vue                  # Root component
├── pages/
│   ├── index.vue           # Home/landing page
│   ├── login.vue           # Login page
│   ├── dashboard.vue       # Main dashboard
│   └── session.vue         # Session player
├── components/
│   ├── BlockSlider.vue     # Slider control
│   ├── BlockCheckbox.vue   # Checkbox control
│   ├── BlockChart.vue      # Chart display
│   └── SessionPlayer.vue   # Session player
├── composables/
│   ├── useBridge.ts        # CursorBridge API client
│   └── useSupabase.ts      # Supabase client
├── server/
│   └── api/
│       ├── bridge/
│       │   ├── templates.get.ts
│       │   ├── controls.get.ts
│       │   └── session.post.ts
│       └── checkin.post.ts
└── types/
    └── index.ts            # TypeScript types
```

## Environment Variables

Create `.env`:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
CURSORBRIDGE_API=http://localhost:3000
CURSORBRIDGE_SANDBOX=http://localhost:3001
```

## Features

- Supabase Auth (email + social)
- Dashboard with drag-drop blocks
- Check-in forms with sliders/checkboxes
- Session player with guided instructions
- Real-time sync with CursorBridge

## CursorBridge Integration

All content comes from CursorBridge APIs:

```typescript
// Fetch templates
const { data } = await useFetch('/api/bridge/templates')

// Generate session
const session = await $fetch('/api/bridge/session', {
  method: 'POST',
  body: { programme_profile_id: '1', session_template_id: '1', duration_min: 15 }
})
```



