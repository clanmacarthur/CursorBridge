const fs = require('node:fs')
const path = require('node:path')
const { spawn } = require('node:child_process')

const repoRoot = path.resolve(__dirname, '..')
const appDir = path.join(repoRoot, 'main-app-starter')
const docsDir = path.join(repoRoot, 'docs')
const taskManagerEnvPath = path.join('C:', 'code', 'task-manager', '.env')
const baseUrl = 'http://127.0.0.1:3000'
const routePath = '/sessions-composer-prototype'

const outJsonPath = path.join(docsDir, '_sessions_prototype_flow_results_2026-03-05.json')
const screenshotDir = path.join(docsDir, 'screenshots', 'sessions-composer-2026-03-05')

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

async function waitForServer(url, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i += 1) {
    try {
      const response = await fetch(url)
      if (response.ok) return true
    } catch {
      // Keep waiting until process is up.
    }
    await sleep(1000)
  }
  return false
}

function pickRow(payload, domainTable) {
  const domain = (payload.domains || []).find((d) => d.table === domainTable)
  if (!domain) return null

  const row = (domain.rows || []).find((entry) => {
    const label = String(entry?.[domain.label_column] || '').trim()
    return Boolean(label)
  })
  if (!row) return null
  const label = String(row[domain.label_column] || '').trim()

  return {
    domain_table: domain.table,
    domain_label: domain.domain_label,
    label,
    notion_page_id: row.notion_page_id || null,
    row,
  }
}

function parseSimpleEnvFile(filePath) {
  const out = {}
  if (!fs.existsSync(filePath)) return out
  const text = fs.readFileSync(filePath, 'utf8')
  for (const rawLine of text.split(/\r?\n/g)) {
    const line = rawLine.trim()
    if (!line || line.startsWith('#')) continue
    const idx = line.indexOf('=')
    if (idx < 1) continue
    const key = line.slice(0, idx).trim()
    const value = line.slice(idx + 1).trim().replace(/^['"]|['"]$/g, '')
    out[key] = value
  }
  return out
}

async function postJson(url, body) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  const raw = await response.text()
  let parsed = null
  try {
    parsed = JSON.parse(raw)
  } catch {
    parsed = { raw }
  }

  return {
    ok: response.ok,
    status: response.status,
    body: parsed,
  }
}

async function runProcess(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { ...options, shell: false })
    let stdout = ''
    let stderr = ''
    child.stdout?.on('data', (chunk) => {
      stdout += chunk.toString()
    })
    child.stderr?.on('data', (chunk) => {
      stderr += chunk.toString()
    })
    child.on('error', reject)
    child.on('close', (code) => {
      if (code === 0) {
        resolve({ code, stdout, stderr })
      } else {
        reject(new Error(`Process failed (${command} ${args.join(' ')}): ${stderr || stdout}`))
      }
    })
  })
}

async function main() {
  const tmEnv = parseSimpleEnvFile(taskManagerEnvPath)
  const supabaseUrl = String(tmEnv.SUPABASE_URL || '').trim()
  const supabaseKey = String(tmEnv.SUPABASE_KEY || '').trim()

  const server = spawn('node', ['.output/server/index.mjs'], {
    cwd: appDir,
    env: {
      ...process.env,
      SUPABASE_URL: supabaseUrl || process.env.SUPABASE_URL || '',
      SUPABASE_KEY: supabaseKey || process.env.SUPABASE_KEY || '',
    },
    stdio: ['ignore', 'pipe', 'pipe'],
  })

  let stdout = ''
  let stderr = ''
  server.stdout.on('data', (chunk) => {
    stdout += chunk.toString()
  })
  server.stderr.on('data', (chunk) => {
    stderr += chunk.toString()
  })

  try {
    fs.mkdirSync(screenshotDir, { recursive: true })

    const up = await waitForServer(`${baseUrl}/api/session/composer-payload`)
    if (!up) {
      throw new Error('Server did not become ready in time.')
    }

    const payloadResp = await fetch(`${baseUrl}/api/session/composer-payload`)
    const payloadJson = await payloadResp.json()
    if (!payloadResp.ok || !payloadJson?.ok || !payloadJson?.payload) {
      throw new Error('Failed to load composer payload.')
    }

    const payload = payloadJson.payload

    const flow1Stack = [pickRow(payload, 'breath_library')].filter(Boolean)
    const flow2Stack = [pickRow(payload, 'breath_library'), pickRow(payload, 'movements_system')].filter(Boolean)
    const colourOrSound = pickRow(payload, 'light_colour') || pickRow(payload, 'sound_vibration')
    const nutritionAny = pickRow(payload, 'nutrition_and_food') || pickRow(payload, 'nutrition_protocols')
    const flow3Stack = [
      pickRow(payload, 'breath_library'),
      colourOrSound,
      pickRow(payload, 'movements_system'),
      nutritionAny,
    ].filter(Boolean)

    const flows = [
      {
        key: 'flow_1_breath_only',
        subject: 'Breath Awareness',
        stack: flow1Stack,
        screenshot_url: `${baseUrl}${routePath}?flow=breath_only`,
        screenshot_file: path.join(screenshotDir, 'flow-1-breath-only.png'),
      },
      {
        key: 'flow_2_breath_movement',
        subject: 'Somatic Regulation',
        stack: flow2Stack,
        screenshot_url: `${baseUrl}${routePath}?flow=breath_movement`,
        screenshot_file: path.join(screenshotDir, 'flow-2-breath-movement.png'),
      },
      {
        key: 'flow_3_breath_colour_or_sound_movement_nutrition',
        subject: 'NSDR',
        stack: flow3Stack,
        screenshot_url: `${baseUrl}${routePath}?flow=breath_colour_sound_movement_nutrition`,
        screenshot_file: path.join(screenshotDir, 'flow-3-breath-colour-sound-movement-nutrition.png'),
      },
    ]

    const flowResults = {}

    for (const flow of flows) {
      let screenshotStatus = { ok: false, path: flow.screenshot_file, error: '' }
      try {
        const screenshotCmd = [
          'npx.cmd',
          '-y',
          'playwright@1.52.0',
          'screenshot',
          '--browser',
          'chromium',
          '--wait-for-timeout',
          '1800',
          '--full-page',
          flow.screenshot_url,
          flow.screenshot_file,
        ].join(' ')

        await runProcess(
          'cmd.exe',
          ['/c', screenshotCmd],
          { cwd: repoRoot }
        )
        screenshotStatus = { ok: true, path: flow.screenshot_file, error: '' }
      } catch (error) {
        screenshotStatus = {
          ok: false,
          path: flow.screenshot_file,
          error: error?.message || String(error),
        }
      }

      const response = await postJson(`${baseUrl}/api/session/composer-save`, {
        subject: flow.subject,
        stack: flow.stack,
        preview: {
          flow_key: flow.key,
          item_count: flow.stack.length,
          route: routePath,
        },
        warnings: [],
        duration_minutes: Math.max(10, flow.stack.length * 5),
      })
      flowResults[flow.key] = {
        subject: flow.subject,
        stack_count: flow.stack.length,
        stack_labels: flow.stack.map((item) => `${item.domain_table}:${item.label}`),
        screenshot: screenshotStatus,
        response,
      }
    }

    const routeResp = await fetch(`${baseUrl}${routePath}`)
    const routeHtml = await routeResp.text()

    const output = {
      route_path: routePath,
      generated_at: new Date().toISOString(),
      payload_source_file: payloadJson.source_file || null,
      top_level_subjects: payload.top_level_subjects || [],
      domain_tables: (payload.domains || []).map((d) => d.table),
      screenshot_dir: screenshotDir,
      route_fetch_status: routeResp.status,
      route_contains_title: routeHtml.includes('Sessions Composer Prototype'),
      route_html_excerpt: routeHtml.slice(0, 1200),
      flow_results: flowResults,
      server_stdout_tail: stdout.slice(-2000),
      server_stderr_tail: stderr.slice(-2000),
    }

    fs.writeFileSync(outJsonPath, JSON.stringify(output, null, 2), 'utf8')
    process.stdout.write(`${outJsonPath}\n`)
  } finally {
    server.kill('SIGTERM')
    await sleep(500)
    if (!server.killed) {
      server.kill('SIGKILL')
    }
  }
}

main().catch((error) => {
  process.stderr.write(`${error?.message || String(error)}\n`)
  process.exitCode = 1
})
