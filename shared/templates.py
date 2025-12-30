"""Dashboard Templates - Pre-built templates for the Main App."""

from typing import Any, Dict, List

# Dashboard template definitions
DASHBOARD_TEMPLATES: List[Dict[str, Any]] = [
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
            },
            {
                "block_type": "slider",
                "config": {
                    "label": "Sleep Quality",
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "default": 5,
                    "low_label": "Poor",
                    "high_label": "Excellent",
                    "color": "#6366f1"
                },
                "position": {"x": 6, "y": 0, "w": 6, "h": 2}
            },
            {
                "block_type": "slider",
                "config": {
                    "label": "Energy Level",
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "default": 5,
                    "low_label": "Exhausted",
                    "high_label": "Energized",
                    "color": "#22c55e"
                },
                "position": {"x": 0, "y": 2, "w": 6, "h": 2}
            },
            {
                "block_type": "slider",
                "config": {
                    "label": "Stress Level",
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "default": 5,
                    "low_label": "Calm",
                    "high_label": "Stressed",
                    "color": "#ef4444",
                    "invert_color": True  # High = bad
                },
                "position": {"x": 6, "y": 2, "w": 6, "h": 2}
            },
            {
                "block_type": "chart",
                "config": {
                    "chart_type": "line",
                    "title": "Weekly Trends",
                    "data_sources": ["mood", "sleep_quality", "energy_level", "stress_level"],
                    "group_by": "day"
                },
                "position": {"x": 0, "y": 4, "w": 12, "h": 4}
            }
        ]
    },
    {
        "id": "breath-movement",
        "name": "Breath & Movement",
        "description": "Guided sessions with breath work and movement practices",
        "category": "fitness",
        "icon": "wind",
        "blocks": [
            {
                "block_type": "session_player",
                "config": {
                    "label": "Today's Session",
                    "show_timer": True,
                    "show_instructions": True,
                    "auto_advance": True
                },
                "position": {"x": 0, "y": 0, "w": 12, "h": 6}
            },
            {
                "block_type": "slider",
                "config": {
                    "label": "How do you feel after?",
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "default": 3,
                    "emoji_scale": ["😔", "😐", "🙂", "😊", "🤩"]
                },
                "position": {"x": 0, "y": 6, "w": 6, "h": 2}
            },
            {
                "block_type": "select",
                "config": {
                    "label": "Session Type",
                    "options": [
                        {"value": "breath", "label": "Breathwork"},
                        {"value": "movement", "label": "Movement"},
                        {"value": "both", "label": "Both"}
                    ]
                },
                "position": {"x": 6, "y": 6, "w": 6, "h": 2}
            }
        ]
    },
    {
        "id": "meditation-journal",
        "name": "Meditation Journal",
        "description": "Track meditation sessions with timer, quality rating, and reflections",
        "category": "meditation",
        "icon": "lotus",
        "blocks": [
            {
                "block_type": "timer",
                "config": {
                    "label": "Meditation Timer",
                    "default_minutes": 10,
                    "presets": [5, 10, 15, 20, 30],
                    "show_bell": True,
                    "ambient_sound": "bowl"
                },
                "position": {"x": 0, "y": 0, "w": 12, "h": 4}
            },
            {
                "block_type": "slider",
                "config": {
                    "label": "Session Quality",
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "default": 3,
                    "labels": ["Distracted", "Okay", "Good", "Deep", "Profound"]
                },
                "position": {"x": 0, "y": 4, "w": 6, "h": 2}
            },
            {
                "block_type": "select",
                "config": {
                    "label": "Technique Used",
                    "options": [
                        {"value": "breath_focus", "label": "Breath Focus"},
                        {"value": "body_scan", "label": "Body Scan"},
                        {"value": "loving_kindness", "label": "Loving Kindness"},
                        {"value": "visualization", "label": "Visualization"},
                        {"value": "open_awareness", "label": "Open Awareness"}
                    ]
                },
                "position": {"x": 6, "y": 4, "w": 6, "h": 2}
            },
            {
                "block_type": "text",
                "config": {
                    "label": "Reflections",
                    "placeholder": "How was your practice today?",
                    "max_length": 500,
                    "multiline": True
                },
                "position": {"x": 0, "y": 6, "w": 12, "h": 3}
            },
            {
                "block_type": "stat",
                "config": {
                    "title": "This Week",
                    "aggregation": "sum",
                    "data_source": "meditation_minutes",
                    "unit": "minutes"
                },
                "position": {"x": 0, "y": 9, "w": 4, "h": 2}
            },
            {
                "block_type": "stat",
                "config": {
                    "title": "Streak",
                    "aggregation": "streak",
                    "data_source": "meditation_completed",
                    "unit": "days"
                },
                "position": {"x": 4, "y": 9, "w": 4, "h": 2}
            },
            {
                "block_type": "stat",
                "config": {
                    "title": "Avg Quality",
                    "aggregation": "avg",
                    "data_source": "session_quality",
                    "decimal_places": 1
                },
                "position": {"x": 8, "y": 9, "w": 4, "h": 2}
            }
        ]
    },
    {
        "id": "nutrition-tracker",
        "name": "Nutrition Tracker",
        "description": "Log meals, hydration, and nutritional habits",
        "category": "nutrition",
        "icon": "utensils",
        "blocks": [
            {
                "block_type": "toggle",
                "config": {
                    "label": "Hydration Goals",
                    "items": [
                        {"id": "water_1", "label": "Glass 1"},
                        {"id": "water_2", "label": "Glass 2"},
                        {"id": "water_3", "label": "Glass 3"},
                        {"id": "water_4", "label": "Glass 4"},
                        {"id": "water_5", "label": "Glass 5"},
                        {"id": "water_6", "label": "Glass 6"},
                        {"id": "water_7", "label": "Glass 7"},
                        {"id": "water_8", "label": "Glass 8"}
                    ]
                },
                "position": {"x": 0, "y": 0, "w": 12, "h": 2}
            },
            {
                "block_type": "toggle",
                "config": {
                    "label": "Meals",
                    "items": [
                        {"id": "breakfast", "label": "Breakfast"},
                        {"id": "lunch", "label": "Lunch"},
                        {"id": "dinner", "label": "Dinner"},
                        {"id": "snacks", "label": "Snacks"}
                    ]
                },
                "position": {"x": 0, "y": 2, "w": 6, "h": 2}
            },
            {
                "block_type": "slider",
                "config": {
                    "label": "Protein Intake",
                    "min": 0,
                    "max": 150,
                    "step": 10,
                    "unit": "g",
                    "default": 50
                },
                "position": {"x": 6, "y": 2, "w": 6, "h": 2}
            },
            {
                "block_type": "timeline",
                "config": {
                    "title": "Meal History",
                    "data_source": "meals",
                    "group_by": "day",
                    "show_last": 7
                },
                "position": {"x": 0, "y": 4, "w": 12, "h": 4}
            }
        ]
    },
    {
        "id": "sleep-tracker",
        "name": "Sleep Tracker",
        "description": "Track sleep patterns, quality, and morning energy",
        "category": "wellness",
        "icon": "moon",
        "blocks": [
            {
                "block_type": "time",
                "config": {
                    "label": "Bedtime",
                    "default": "22:00"
                },
                "position": {"x": 0, "y": 0, "w": 4, "h": 2}
            },
            {
                "block_type": "time",
                "config": {
                    "label": "Wake Time",
                    "default": "07:00"
                },
                "position": {"x": 4, "y": 0, "w": 4, "h": 2}
            },
            {
                "block_type": "stat",
                "config": {
                    "title": "Hours Slept",
                    "calculation": "wake_time - bedtime",
                    "unit": "hours"
                },
                "position": {"x": 8, "y": 0, "w": 4, "h": 2}
            },
            {
                "block_type": "slider",
                "config": {
                    "label": "Sleep Quality",
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "emoji_scale": ["😴", "😪", "😌", "😊", "🌟"]
                },
                "position": {"x": 0, "y": 2, "w": 6, "h": 2}
            },
            {
                "block_type": "slider",
                "config": {
                    "label": "Morning Energy",
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "emoji_scale": ["🔋", "🔋", "🔋", "⚡", "⚡"]
                },
                "position": {"x": 6, "y": 2, "w": 6, "h": 2}
            },
            {
                "block_type": "chart",
                "config": {
                    "chart_type": "bar",
                    "title": "Sleep Duration This Week",
                    "data_source": "hours_slept",
                    "group_by": "day"
                },
                "position": {"x": 0, "y": 4, "w": 12, "h": 4}
            }
        ]
    }
]


def get_all_templates() -> List[Dict[str, Any]]:
    """Get all available dashboard templates."""
    return DASHBOARD_TEMPLATES


def get_template_by_id(template_id: str) -> Dict[str, Any] | None:
    """Get a specific template by ID."""
    for template in DASHBOARD_TEMPLATES:
        if template["id"] == template_id:
            return template
    return None


def get_templates_by_category(category: str) -> List[Dict[str, Any]]:
    """Get templates filtered by category."""
    return [t for t in DASHBOARD_TEMPLATES if t["category"] == category]

