<template>
  <div class="composer-page">
    <header class="top-subjects">
      <h1>Sessions Composer Prototype</h1>
      <div class="subject-row">
        <button
          v-for="subject in subjects"
          :key="subject"
          :class="{ active: selectedSubject === subject }"
          @click="selectedSubject = subject"
        >
          {{ subject }}
        </button>
      </div>
      <p class="source-note">
        Source: <code>docs/SESSIONS_UI_PAYLOAD_2026-03-05.json</code>
      </p>
    </header>

    <main class="composer-grid">
      <section class="wheel-pane">
        <div v-if="pending" class="status">Loading composer payload...</div>
        <div v-else-if="loadError" class="status error">
          Failed to load payload: {{ loadError }}
        </div>
        <div v-else class="wheel-wrap">
          <svg class="wheel" viewBox="0 0 620 620" role="img" aria-label="Domain wheel">
            <circle cx="310" cy="310" r="288" fill="#111827" />
            <path
              v-for="segment in wheelSegments"
              :key="segment.table"
              :d="segment.path"
              :fill="segment.fill"
              :stroke="segment.table === selectedDomainTable ? '#f59e0b' : '#0f172a'"
              :stroke-width="segment.table === selectedDomainTable ? 4 : 1.4"
              class="segment"
              @click="openDomain(segment.table)"
            />
            <circle cx="310" cy="310" r="145" fill="#0b1220" />
            <text x="310" y="296" text-anchor="middle" fill="#e5e7eb" font-size="20" font-weight="700">
              Domains
            </text>
            <text x="310" y="324" text-anchor="middle" fill="#93a0b5" font-size="12">
              Click a segment to open drawer
            </text>
            <text
              v-for="segment in wheelSegments"
              :key="`${segment.table}-label`"
              :x="segment.labelX"
              :y="segment.labelY"
              text-anchor="middle"
              dominant-baseline="middle"
              fill="#f8fafc"
              font-size="11"
              class="wheel-label"
              @click="openDomain(segment.table)"
            >
              {{ segment.label }}
            </text>
          </svg>
        </div>
      </section>

      <aside class="drawer" :class="{ open: drawerOpen }">
        <div class="drawer-header">
          <h2>{{ currentDomain?.domain_label || 'Domain' }}</h2>
          <button class="close-btn" @click="drawerOpen = false">Close</button>
        </div>

        <div v-if="!currentDomain" class="drawer-empty">Select a domain on the wheel.</div>
        <div v-else class="drawer-content">
          <div class="search-row">
            <label>Search</label>
            <input v-model="searchTerm" type="text" placeholder="Search live rows..." />
          </div>

          <div class="filters">
            <div
              v-for="column in currentDomain.visible_filter_columns"
              :key="column"
              class="filter"
            >
              <label>{{ column }}</label>
              <select v-model="activeFilters[column]">
                <option value="">All</option>
                <option
                  v-for="value in currentDomain.visible_filter_values[column] || []"
                  :key="`${column}-${value}`"
                  :value="value"
                >
                  {{ value }}
                </option>
              </select>
            </div>
          </div>

          <div class="row-list">
            <h3>Rows ({{ filteredRows.length }})</h3>
            <ul>
              <li
                v-for="(row, rowIndex) in filteredRows"
                :key="rowKey(row, rowIndex)"
                :class="{ selected: rowKey(row, rowIndex) === selectedRowId }"
                @click="selectedRowId = rowKey(row, rowIndex)"
              >
                <div class="row-title">
                  {{ displayValue(row[currentDomain.label_column]) }}
                </div>
                <div class="row-sub">
                  {{ displayValue(row[currentDomain.subject_grouping_column]) }}
                </div>
              </li>
            </ul>
          </div>

          <div class="detail" v-if="selectedRow">
            <h3>Detail</h3>
            <dl>
              <template v-for="field in currentDomain.detail_fields" :key="field">
                <dt>{{ field }}</dt>
                <dd>{{ displayValue(selectedRow[field]) }}</dd>
              </template>
            </dl>
            <button class="add-btn" @click="addSelectedRow">Add To Session Stack</button>
          </div>
        </div>
      </aside>
    </main>

    <section class="stack-preview">
      <div class="stack">
        <h2>Session Stack</h2>
        <p class="hint">Ordered selections to be used for generation and save.</p>
        <ul v-if="stack.length">
          <li v-for="(item, index) in stack" :key="item.id">
            <span class="order">{{ index + 1 }}</span>
            <span class="label">{{ item.domain_label }}: {{ item.label }}</span>
            <span class="actions">
              <button @click="moveUp(index)" :disabled="index === 0">Up</button>
              <button @click="moveDown(index)" :disabled="index === stack.length - 1">Down</button>
              <button @click="removeItem(index)">Remove</button>
            </span>
          </li>
        </ul>
        <p v-else class="hint">No items added yet.</p>
      </div>

      <div class="preview">
        <h2>Preview</h2>
        <div class="preview-block">
          <h3>Warnings</h3>
          <ul>
            <li v-for="(warning, idx) in previewWarnings" :key="`warning-${idx}`">{{ warning }}</li>
          </ul>
        </div>
        <div class="preview-block">
          <h3>Combined Output Structure</h3>
          <pre>{{ JSON.stringify(combinedOutput, null, 2) }}</pre>
        </div>
        <button class="save-btn" :disabled="!stack.length || saving" @click="saveSession">
          {{ saving ? 'Saving...' : 'Save Composer Session' }}
        </button>
        <div v-if="saveResult" class="save-result">
          <p><strong>Route:</strong> {{ saveRoute }}</p>
          <p><strong>session_runs id:</strong> {{ saveResult.session_run_id || '(none)' }}</p>
          <p>
            <strong>session_outputs id(s):</strong>
            {{ (saveResult.session_output_ids || []).length ? saveResult.session_output_ids.join(', ') : '(none)' }}
          </p>
          <p v-if="saveResult.blocker"><strong>Blocker:</strong> {{ saveResult.blocker.table }} - {{ saveResult.blocker.issue }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
interface DomainPayload {
  table: string
  domain_label: string
  row_count: number
  label_column: string
  search_columns: string[]
  visible_filter_columns: string[]
  visible_filter_values: Record<string, string[]>
  hidden_dead_columns: string[]
  detail_fields: string[]
  snapping_fields: string[]
  subject_grouping_column: string
  first_drill_down_column: string
  second_drill_down_column: string
  rows: Record<string, any>[]
}

interface ComposerPayload {
  top_level_subjects: string[]
  domains: DomainPayload[]
  support_tables: {
    safety_rules: Record<string, any>[]
    mappings: Record<string, any>[]
    cross_domain_mappings: Record<string, any>[]
  }
}

interface StackItem {
  id: string
  domain_table: string
  domain_label: string
  label: string
  notion_page_id?: string
  row: Record<string, any>
}

const { data, pending } = await useFetch<{ ok: boolean; payload: ComposerPayload; message?: string }>(
  '/api/session/composer-payload'
)
const route = useRoute()

const loadError = computed(() => (data.value?.ok ? '' : data.value?.message || 'unknown error'))
const payload = computed(() => data.value?.payload || null)
const subjects = computed(() => payload.value?.top_level_subjects || [])
const domains = computed(() => payload.value?.domains || [])

const selectedSubject = ref('')
const selectedDomainTable = ref('')
const drawerOpen = ref(true)
const searchTerm = ref('')
const activeFilters = ref<Record<string, string>>({})
const selectedRowId = ref('')
const stack = ref<StackItem[]>([])
const saving = ref(false)
const saveResult = ref<any | null>(null)
const saveRoute = '/sessions-composer-prototype'

watch(
  subjects,
  (list) => {
    if (!selectedSubject.value && list.length) {
      selectedSubject.value = list[0]
    }
  },
  { immediate: true }
)

watch(
  domains,
  (list) => {
    if (!selectedDomainTable.value && list.length) {
      selectedDomainTable.value = list[0].table
      drawerOpen.value = true
    }
  },
  { immediate: true }
)

const currentDomain = computed(() => domains.value.find(d => d.table === selectedDomainTable.value) || null)

watch(currentDomain, (domain) => {
  searchTerm.value = ''
  selectedRowId.value = ''
  const nextFilters: Record<string, string> = {}
  if (domain) {
    for (const col of domain.visible_filter_columns) {
      nextFilters[col] = ''
    }
  }
  activeFilters.value = nextFilters
})

const displayValue = (value: unknown) => {
  if (value === null || value === undefined) return ''
  if (typeof value === 'string') return value
  if (typeof value === 'number' || typeof value === 'boolean') return String(value)
  return JSON.stringify(value)
}

const normalize = (value: unknown) => displayValue(value).toLowerCase().trim()

const rowKey = (row: Record<string, any>, index: number) =>
  `${row.notion_page_id || row.id || row[currentDomain.value?.label_column || ''] || 'row'}-${index}`

const makeStackItem = (domain: DomainPayload | null, row: Record<string, any> | null): StackItem | null => {
  if (!domain || !row) return null
  const label = displayValue(row[domain.label_column])
  if (!label) return null
  return {
    id: `${Date.now()}-${Math.random().toString(16).slice(2, 10)}`,
    domain_table: domain.table,
    domain_label: domain.domain_label,
    label,
    notion_page_id: row.notion_page_id,
    row,
  }
}

const firstRowForDomain = (table: string) => {
  const domain = domains.value.find(d => d.table === table) || null
  if (!domain || !domain.rows?.length) return null
  const labelledRow = domain.rows.find((row) => Boolean(displayValue(row[domain.label_column])))
  if (!labelledRow) return null
  return {
    domain,
    row: labelledRow,
  }
}

const applyPresetFlow = (flowRaw: string) => {
  const flow = String(flowRaw || '').trim().toLowerCase()
  if (!flow) return

  const next: StackItem[] = []

  const pushFirst = (table: string) => {
    const picked = firstRowForDomain(table)
    const item = makeStackItem(picked?.domain || null, picked?.row || null)
    if (item) next.push(item)
  }

  if (flow === 'breath-only' || flow === 'breath_only') {
    pushFirst('breath_library')
  }

  if (flow === 'breath-movement' || flow === 'breath_movement') {
    pushFirst('breath_library')
    pushFirst('movements_system')
  }

  if (
    flow === 'breath-colour-sound-movement-nutrition' ||
    flow === 'breath_colour_sound_movement_nutrition'
  ) {
    pushFirst('breath_library')
    if (firstRowForDomain('light_colour')) {
      pushFirst('light_colour')
    } else {
      pushFirst('sound_vibration')
    }
    pushFirst('movements_system')
    if (firstRowForDomain('nutrition_and_food')) {
      pushFirst('nutrition_and_food')
    } else {
      pushFirst('nutrition_protocols')
    }
  }

  if (next.length) {
    stack.value = next
  }
}

const filteredRows = computed(() => {
  const domain = currentDomain.value
  if (!domain) return []

  let rows = [...domain.rows]
  const term = searchTerm.value.trim().toLowerCase()
  if (term) {
    rows = rows.filter((row) =>
      domain.search_columns.some((col) => normalize(row[col]).includes(term))
    )
  }

  for (const col of domain.visible_filter_columns) {
    const selected = activeFilters.value[col]
    if (!selected) continue
    rows = rows.filter((row) => displayValue(row[col]) === selected)
  }

  return rows
})

const selectedRow = computed(() => {
  if (!selectedRowId.value) return null
  return filteredRows.value.find((row, index) => rowKey(row, index) === selectedRowId.value) || null
})

const openDomain = (table: string) => {
  selectedDomainTable.value = table
  drawerOpen.value = true
}

const addSelectedRow = () => {
  const domain = currentDomain.value
  const row = selectedRow.value
  if (!domain || !row) return

  const item = makeStackItem(domain, row)
  if (!item) return
  stack.value.push(item)
}

const moveUp = (index: number) => {
  if (index <= 0) return
  const copy = [...stack.value]
  const [item] = copy.splice(index, 1)
  copy.splice(index - 1, 0, item)
  stack.value = copy
}

const moveDown = (index: number) => {
  if (index >= stack.value.length - 1) return
  const copy = [...stack.value]
  const [item] = copy.splice(index, 1)
  copy.splice(index + 1, 0, item)
  stack.value = copy
}

const removeItem = (index: number) => {
  stack.value.splice(index, 1)
}

const previewWarnings = computed(() => {
  const safetyRules = payload.value?.support_tables?.safety_rules || []
  return safetyRules
    .slice(0, 6)
    .map((rule) => {
      const severity = displayValue(rule.severity || 'Info')
      const name = displayValue(rule.rule_name || '')
      const description = displayValue(rule.description || '')
      return `${severity}: ${name}${description ? ` - ${description}` : ''}`
    })
})

const combinedOutput = computed(() => {
  const mappings = payload.value?.support_tables?.mappings || []
  const crossDomain = payload.value?.support_tables?.cross_domain_mappings || []
  return {
    subject: selectedSubject.value,
    stack_order: stack.value.map((item, index) => ({
      order: index + 1,
      domain_table: item.domain_table,
      domain_label: item.domain_label,
      label: item.label,
      notion_page_id: item.notion_page_id || null,
    })),
    warnings: previewWarnings.value,
    structure: {
      total_items: stack.value.length,
      domains_selected: Array.from(new Set(stack.value.map(s => s.domain_table))),
      mapping_rows_available: mappings.length,
      cross_domain_rows_available: crossDomain.length,
    },
  }
})

const saveSession = async () => {
  if (!stack.value.length) return
  saving.value = true
  saveResult.value = null
  try {
    const response = await $fetch('/api/session/composer-save', {
      method: 'POST',
      body: {
        subject: selectedSubject.value,
        stack: stack.value,
        preview: combinedOutput.value,
        warnings: previewWarnings.value,
        duration_minutes: Math.max(10, stack.value.length * 5),
      },
    })
    saveResult.value = response
  } catch (error: any) {
    saveResult.value = error?.data || { message: error?.message || 'save failed' }
  } finally {
    saving.value = false
  }
}

watch(
  [domains, () => route.query.flow],
  ([list, flow]) => {
    if (!list.length) return
    const flowValue = String(flow || '').trim()
    if (!flowValue) return
    applyPresetFlow(flowValue)
  },
  { immediate: true }
)

const colors = [
  '#2563eb',
  '#0ea5e9',
  '#0891b2',
  '#0d9488',
  '#16a34a',
  '#65a30d',
  '#ca8a04',
  '#ea580c',
  '#dc2626',
  '#9333ea',
  '#7c3aed',
  '#0369a1',
]

const polarToCartesian = (cx: number, cy: number, r: number, angleDeg: number) => {
  const angle = ((angleDeg - 90) * Math.PI) / 180
  return {
    x: cx + r * Math.cos(angle),
    y: cy + r * Math.sin(angle),
  }
}

const donutSlicePath = (
  cx: number,
  cy: number,
  outerR: number,
  innerR: number,
  startAngle: number,
  endAngle: number
) => {
  const startOuter = polarToCartesian(cx, cy, outerR, endAngle)
  const endOuter = polarToCartesian(cx, cy, outerR, startAngle)
  const startInner = polarToCartesian(cx, cy, innerR, endAngle)
  const endInner = polarToCartesian(cx, cy, innerR, startAngle)
  const largeArcFlag = endAngle - startAngle <= 180 ? 0 : 1

  return [
    `M ${startOuter.x} ${startOuter.y}`,
    `A ${outerR} ${outerR} 0 ${largeArcFlag} 0 ${endOuter.x} ${endOuter.y}`,
    `L ${endInner.x} ${endInner.y}`,
    `A ${innerR} ${innerR} 0 ${largeArcFlag} 1 ${startInner.x} ${startInner.y}`,
    'Z',
  ].join(' ')
}

const wheelSegments = computed(() => {
  const list = domains.value
  if (!list.length) return []
  const step = 360 / list.length
  const cx = 310
  const cy = 310
  const outerR = 282
  const innerR = 158
  const labelR = 222

  return list.map((domain, i) => {
    const start = i * step
    const end = start + step
    const mid = start + step / 2
    const labelPoint = polarToCartesian(cx, cy, labelR, mid)
    return {
      table: domain.table,
      label: domain.domain_label,
      path: donutSlicePath(cx, cy, outerR, innerR, start, end),
      fill: colors[i % colors.length],
      labelX: labelPoint.x,
      labelY: labelPoint.y,
    }
  })
})
</script>

<style scoped>
.composer-page {
  min-height: 100vh;
  background: radial-gradient(circle at 20% 0%, #1f2937, #05070d 60%);
  color: #f8fafc;
  padding: 1rem 1rem 2rem;
}

.top-subjects h1 {
  margin: 0 0 0.7rem;
  font-size: 1.6rem;
}

.subject-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.subject-row button {
  border: 1px solid #334155;
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 999px;
  padding: 0.45rem 0.8rem;
  cursor: pointer;
}

.subject-row button.active {
  border-color: #f59e0b;
  background: #3f2a03;
  color: #fde68a;
}

.source-note {
  margin: 0.7rem 0 0;
  color: #94a3b8;
  font-size: 0.85rem;
}

.composer-grid {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: 1fr minmax(320px, 420px);
  gap: 1rem;
  align-items: start;
}

.wheel-pane {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid #1f2937;
  border-radius: 14px;
  min-height: 660px;
  padding: 1rem;
}

.status {
  color: #e2e8f0;
}

.status.error {
  color: #fda4af;
}

.wheel-wrap {
  display: grid;
  place-items: center;
}

.wheel {
  width: min(96vw, 660px);
  max-width: 100%;
  height: auto;
}

.segment {
  cursor: pointer;
  opacity: 0.94;
}

.segment:hover {
  opacity: 1;
}

.wheel-label {
  pointer-events: none;
  font-weight: 600;
}

.drawer {
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid #1f2937;
  border-radius: 14px;
  min-height: 660px;
  padding: 0.75rem;
  transition: opacity 0.2s ease;
}

.drawer:not(.open) {
  opacity: 0.5;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.drawer-header h2 {
  margin: 0;
  font-size: 1.1rem;
}

.close-btn,
.add-btn,
.save-btn {
  border: 1px solid #334155;
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 8px;
  padding: 0.45rem 0.7rem;
  cursor: pointer;
}

.add-btn {
  margin-top: 0.8rem;
  width: 100%;
}

.save-btn {
  width: 100%;
  margin-top: 0.8rem;
  background: #14532d;
  border-color: #166534;
}

.search-row,
.filter {
  margin-top: 0.7rem;
}

.search-row label,
.filter label {
  display: block;
  font-size: 0.82rem;
  color: #94a3b8;
  margin-bottom: 0.2rem;
}

.search-row input,
.filter select {
  width: 100%;
  border-radius: 8px;
  border: 1px solid #334155;
  background: #020617;
  color: #e2e8f0;
  padding: 0.45rem 0.55rem;
}

.row-list {
  margin-top: 0.8rem;
}

.row-list ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0;
  max-height: 230px;
  overflow: auto;
  border: 1px solid #1f2937;
  border-radius: 10px;
}

.row-list li {
  border-bottom: 1px solid #1f2937;
  padding: 0.5rem 0.6rem;
  cursor: pointer;
}

.row-list li:hover {
  background: #0b1220;
}

.row-list li.selected {
  background: #1e293b;
  border-left: 3px solid #f59e0b;
}

.row-title {
  font-size: 0.9rem;
}

.row-sub {
  font-size: 0.75rem;
  color: #94a3b8;
}

.detail {
  margin-top: 0.8rem;
  border: 1px solid #1f2937;
  border-radius: 10px;
  padding: 0.5rem 0.6rem;
}

.detail dl {
  margin: 0;
}

.detail dt {
  color: #94a3b8;
  font-size: 0.74rem;
}

.detail dd {
  margin: 0 0 0.45rem;
  font-size: 0.84rem;
  word-break: break-word;
}

.stack-preview {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.stack,
.preview {
  background: rgba(15, 23, 42, 0.78);
  border: 1px solid #1f2937;
  border-radius: 14px;
  padding: 0.8rem;
}

.stack h2,
.preview h2 {
  margin: 0 0 0.45rem;
  font-size: 1.12rem;
}

.hint {
  color: #94a3b8;
  font-size: 0.82rem;
}

.stack ul {
  list-style: none;
  padding: 0;
  margin: 0.7rem 0 0;
}

.stack li {
  display: grid;
  grid-template-columns: 24px 1fr auto;
  gap: 0.4rem;
  align-items: center;
  padding: 0.45rem;
  border: 1px solid #1f2937;
  border-radius: 8px;
  margin-bottom: 0.45rem;
}

.order {
  width: 22px;
  height: 22px;
  border-radius: 999px;
  background: #1e293b;
  display: grid;
  place-items: center;
  font-size: 0.78rem;
}

.label {
  font-size: 0.85rem;
}

.actions button {
  margin-left: 0.3rem;
  border: 1px solid #334155;
  border-radius: 6px;
  background: #020617;
  color: #e2e8f0;
  padding: 0.2rem 0.45rem;
  cursor: pointer;
}

.preview-block {
  margin-bottom: 0.7rem;
}

.preview-block h3 {
  margin: 0 0 0.3rem;
  font-size: 0.9rem;
}

.preview pre {
  max-height: 220px;
  overflow: auto;
  background: #020617;
  border: 1px solid #1f2937;
  border-radius: 10px;
  padding: 0.6rem;
  font-size: 0.75rem;
}

.save-result {
  margin-top: 0.7rem;
  font-size: 0.84rem;
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 0.55rem;
}

@media (max-width: 1100px) {
  .composer-grid,
  .stack-preview {
    grid-template-columns: 1fr;
  }
}
</style>
