// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: [
    '@nuxtjs/supabase'
  ],
  
  supabase: {
    redirectOptions: {
      login: '/login',
      callback: '/confirm',
      exclude: ['/', '/login', '/register'],
    }
  },
  
  runtimeConfig: {
    // Server-side only
    cursorBridgeApi: process.env.CURSORBRIDGE_API || 'http://localhost:3000',
    cursorBridgeSandbox: process.env.CURSORBRIDGE_SANDBOX || 'http://localhost:3001',
    
    // Client-side (public)
    public: {
      supabaseUrl: process.env.SUPABASE_URL,
      supabaseKey: process.env.SUPABASE_KEY,
    }
  },
  
  app: {
    head: {
      title: 'Wellness App',
      meta: [
        { name: 'description', content: 'Your personal wellness dashboard' }
      ],
      link: [
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' }
      ]
    }
  },
  
  css: ['~/assets/css/main.css'],
})




