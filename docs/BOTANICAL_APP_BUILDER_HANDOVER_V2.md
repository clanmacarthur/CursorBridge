# Botanical App Builder Handover V2

Last updated: 2026-03-31

## Core Rule

This system is expandable. It is not a fixed botanical list.

## App Must Support

- adding new botanical entries
- adding new cultivars and named lines
- adding new branches
- extending product paths
- extending protocol libraries
- extending ecology and design overlays
- extending into fungi, moss, bryophyte, fauna, and future branches without schema break

## Critical Filters

The app must expose filtering for:

- branch
- zone
- microclimate
- production mode
- size
- tree height
- spread
- root volume
- root depth
- root architecture
- symbiotic role
- canonical layer
- season start
- season end
- rarity
- conservation relevance
- ecological value
- heritage value
- medicinal value
- product potential
- data confidence
- record completeness
- system role
- propagation difficulty
- invasiveness risk
- drought tolerance
- frost tolerance
- tea use
- edible flower use
- cut flower use
- medicinal flower use

## Critical UI Behaviors

- preserve cultivar-level rows
- do not default to species collapse
- allow branch-aware views
- allow generated flat operational view alongside normalized source layers
- support visual module/build planning that depends on size and root fields
- support filtering and planning by universal layer and symbiotic role
- support a two-way selection experience:
  - product -> matching varieties / trees / botanical entries
  - botanical entry / tree / variety -> valid product paths
- keep product-first discovery and botanical-first discovery symmetrical
- do not hide cultivar rows when the user starts from a product selection

## Compatibility Engine

Use:

- trait scoring
- curated compatibility rules
- user overrides
- policy filtering last

## Hard Rules

- restoration mode = native-first only
- experimental mode = contained only
- ecological restrictions can override user choices when required

Symbiosis must not be collapsed into companion planting in the UI or filter model.
