import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import ZettleCards from './ZettleCards.vue'
import App from './App.vue'

// Create router instance
const router = createRouter({
  history: createWebHistory(window.location.pathname),
  routes: [
    {
      path: '',
      component: ZettleCards,
    },
  ],
})

// Initialize with current query parameters
router.replace({
  query: Object.fromEntries(new URLSearchParams(window.location.search).entries()),
})

// Handle navigation
router.beforeEach((to, from) => {
  // If only query params changed, allow the navigation
  if (to.path === from.path) {
    return true
  }
  // If the path changed, do a full page load
  window.location.href = to.fullPath
  return false
})

// Create and mount the app
const app = createApp(App)
app.use(router)
app.mount('#zettlecards-app')
