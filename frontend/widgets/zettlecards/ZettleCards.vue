<template>
  <div class="min-h-screen bg-gray-500">
    <header class="bg-white shadow-sm">
      <div class="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <h1 class="text-2xl font-semibold text-gray-900">Zettle Cards</h1>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <!-- Loading State -->
      <div v-if="loading" class="py-8 text-center">
        <div class="mx-auto h-12 w-12 animate-spin rounded-full border-b-2 border-gray-900"></div>
        <p class="mt-2 text-gray-600">Loading cards...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="rounded-md bg-red-50 p-4">
        <div class="flex">
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error loading cards</h3>
            <p class="mt-1 text-sm text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Cards Grid -->
      <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <ZettleCard v-for="card in cards" :key="card.uuid" :card="card" />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ZettleCard from './ZettleCard.vue'

const cards = ref([])
const loading = ref(true)
const error = ref(null)

const fetchCards = async () => {
  try {
    loading.value = true
    const response = await fetch('/api/cards/')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    cards.value = data.results || data
  } catch (e) {
    error.value = e.message
    console.error('Error fetching cards:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCards()
})
</script>
