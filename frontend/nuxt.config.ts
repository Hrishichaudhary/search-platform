export default defineNuxtConfig({
  compatibilityDate: '2025-07-10',
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxt/content'
  ],
  css: ['~/assets/css/tailwind.css'],
  pages: true,
  content: {
    experimental: {
      search: true
    }
  }
})
