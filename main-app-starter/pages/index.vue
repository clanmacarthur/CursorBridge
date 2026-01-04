<template>
  <div class="landing">
    <div class="hero">
      <h1>Your Personal<br><span class="accent">Wellness Dashboard</span></h1>
      <p class="subtitle">
        Track your daily habits, generate guided sessions, and unlock insights 
        about your wellbeing with our adaptive wellness engine.
      </p>
      <div class="cta-buttons">
        <NuxtLink to="/dashboard" class="btn-primary btn-large">
          Get Started
        </NuxtLink>
        <NuxtLink to="/session" class="btn-secondary btn-large">
          Try a Session
        </NuxtLink>
      </div>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">🎛️</div>
        <h3>Adaptive Controls</h3>
        <p>Personalized sliders and check-ins that learn from your patterns</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🧘</div>
        <h3>Guided Sessions</h3>
        <p>AI-generated breathwork, movement, and meditation sessions</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Smart Insights</h3>
        <p>See how your habits influence each other with coupling rules</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.landing {
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 4rem 0;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 700;
  color: #fff;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.accent {
  background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.6);
  max-width: 600px;
  margin: 0 auto 2rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
}

.feature-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #fff;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: rgba(255, 255, 255, 0.6);
}
</style>




