<template>
  <div class="sessions-page">
    <div class="card">
      <h1>Sessions Builder (Planned)</h1>
      <p>
        This page is the planned home for the wheel-based builder.
      </p>
      <p>
        The live generation flow is still on <code>/session</code>.
      </p>

      <h2>Planned API Contract</h2>
      <ul>
        <li><code>GET /api/session/themes</code></li>
        <li><code>POST /api/session/preview</code></li>
        <li><code>POST /api/session/generate</code></li>
      </ul>

      <p>
        See <code>docs/HANDOVER_SESSIONS.md</code> for current-vs-target details.
      </p>
      <NuxtLink to="/session" class="go-live">Go to live session page</NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.sessions-page {
  min-height: calc(100vh - 80px);
  display: grid;
  place-items: center;
  padding: 2rem;
}

.card {
  width: min(760px, 100%);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
  color: #fff;
}

h1 {
  margin: 0 0 1rem;
}

h2 {
  margin-top: 1.5rem;
}

ul {
  margin: 0.75rem 0 1rem 1.25rem;
}

.go-live {
  display: inline-block;
  margin-top: 1rem;
  color: #fff;
  text-decoration: underline;
}
</style>
