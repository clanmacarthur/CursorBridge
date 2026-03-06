<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="header-content">
        <NuxtLink to="/" class="logo">Wellness</NuxtLink>
        <nav class="nav-links">
          <NuxtLink to="/dashboard">Dashboard</NuxtLink>
          <NuxtLink to="/session">Session</NuxtLink>
          <NuxtLink to="/sessions">Sessions (Planned)</NuxtLink>
        </nav>
        <div class="user-menu">
          <button v-if="user" @click="signOut" class="btn-secondary">
            Sign Out
          </button>
          <NuxtLink v-else to="/login" class="btn-primary">
            Sign In
          </NuxtLink>
        </div>
      </div>
    </header>
    
    <main class="app-main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
const user = useSupabaseUser()
const client = useSupabaseClient()

async function signOut() {
  await client.auth.signOut()
  navigateTo('/login')
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem 2rem;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #e94560;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #fff;
}

.app-main {
  flex: 1;
  background: #0f0f23;
}
</style>
















