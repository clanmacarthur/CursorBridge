<template>
  <div class="login-page">
    <div class="login-card">
      <h1>Welcome Back</h1>
      <p class="subtitle">Sign in to your wellness dashboard</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            id="email" 
            v-model="email" 
            type="email" 
            placeholder="you@example.com"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password" 
            v-model="password" 
            type="password" 
            placeholder="••••••••"
            required
          />
        </div>
        
        <button type="submit" class="btn-primary btn-full" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
        
        <p v-if="error" class="error">{{ error }}</p>
      </form>
      
      <div class="divider">
        <span>or continue with</span>
      </div>
      
      <button @click="handleGoogleLogin" class="btn-social">
        <span>🔵</span> Google
      </button>
      
      <p class="signup-link">
        Don't have an account? <NuxtLink to="/register">Sign up</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const client = useSupabaseClient()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  
  const { error: authError } = await client.auth.signInWithPassword({
    email: email.value,
    password: password.value,
  })
  
  if (authError) {
    error.value = authError.message
  } else {
    navigateTo('/dashboard')
  }
  
  loading.value = false
}

async function handleGoogleLogin() {
  await client.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${window.location.origin}/dashboard`
    }
  })
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 3rem;
  width: 100%;
  max-width: 420px;
}

.login-card h1 {
  color: #fff;
  font-size: 2rem;
  text-align: center;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  margin-bottom: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
}

.form-group input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 0.875rem 1rem;
  color: #fff;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #e94560;
}

.error {
  color: #e94560;
  font-size: 0.875rem;
  text-align: center;
}

.divider {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1.5rem 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.divider span {
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.875rem;
}

.btn-social {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 0.875rem;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-social:hover {
  background: rgba(255, 255, 255, 0.1);
}

.signup-link {
  text-align: center;
  margin-top: 1.5rem;
  color: rgba(255, 255, 255, 0.5);
}

.signup-link a {
  color: #e94560;
}
</style>



