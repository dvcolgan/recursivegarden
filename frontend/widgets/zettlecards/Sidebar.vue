<template>
  <aside
    class="fixed top-14 bottom-0 left-0 w-72 overflow-y-auto bg-white p-4 shadow-lg"
    :class="{ hidden: !activeCard }">
    <div v-if="activeCard" class="space-y-4">
      <!-- Card Type Badge -->
      <span
        class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize"
        :class="cardTypeClasses">
        {{ activeCard.card_type }}
      </span>

      <!-- Title -->
      <h2 class="text-xl font-bold">{{ activeCard.title || 'Untitled Card' }}</h2>

      <!-- Content -->
      <div class="space-y-4">
        <p v-if="activeCard.text" class="text-gray-600">{{ activeCard.text }}</p>
        <img
          v-if="activeCard.image"
          :src="activeCard.image"
          class="rounded-lg"
          :alt="activeCard.title || 'Card image'" />
        <a
          v-if="activeCard.url"
          :href="activeCard.url"
          class="block break-all text-blue-600 hover:text-blue-800">
          {{ activeCard.url }}
        </a>
      </div>

      <!-- Navigation -->
      <div class="flex justify-between pt-4">
        <button
          v-if="prevCard"
          @click="$emit('navigate', prevCard)"
          class="text-sm text-gray-600 hover:text-gray-900">
          ← {{ prevCard.title || 'Previous' }}
        </button>
        <button
          v-if="nextCard"
          @click="$emit('navigate', nextCard)"
          class="text-sm text-gray-600 hover:text-gray-900">
          {{ nextCard.title || 'Next' }} →
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ZettleCardData } from '../types'

const props = defineProps<{
  activeCard: ZettleCardData | null
  prevCard: ZettleCardData | null
  nextCard: ZettleCardData | null
}>()

defineEmits<{
  navigate: [card: ZettleCardData]
}>()

const cardTypeClasses = computed(
  () =>
    ({
      text: 'bg-blue-100 text-blue-800',
      image: 'bg-green-100 text-green-800',
      url: 'bg-purple-100 text-purple-800',
      model: 'bg-yellow-100 text-yellow-800',
      topic: 'bg-red-100 text-red-800',
    })[props.activeCard?.card_type || 'text']
)
</script>
