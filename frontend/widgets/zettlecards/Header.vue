<template>
  <header class="fixed top-0 right-0 left-0 z-50 bg-white shadow-md">
    <div class="flex items-center justify-between px-4 py-2">
      <!-- Navigation Section -->
      <div class="flex items-center space-x-2">
        <button
          v-if="activeCard"
          @click="$emit('navigateUp')"
          class="rounded-lg bg-gray-100 p-2 hover:bg-gray-200">
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <!-- Breadcrumbs -->
        <div class="flex items-center space-x-2 text-sm">
          <button @click="$emit('navigateToRoot')" class="text-gray-600 hover:text-gray-900">
            Root
          </button>
          <template v-if="breadcrumbs.length">
            <span v-for="(crumb, index) in breadcrumbs" :key="crumb.uuid">
              <span class="text-gray-400">/</span>
              <button
                @click="$emit('navigateTo', crumb)"
                :class="{
                  'text-gray-600 hover:text-gray-900': index < breadcrumbs.length - 1,
                  'font-medium text-gray-900': index === breadcrumbs.length - 1,
                }">
                {{ crumb.title || 'Untitled' }}
              </button>
            </span>
          </template>
        </div>
      </div>

      <!-- Controls Section -->
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-600">{{ cardCount }} cards</span>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import type { ZettleCardData } from './types'

defineProps<{
  activeCard: ZettleCardData | null
  breadcrumbs: ZettleCardData[]
  cardCount: number
}>()

defineEmits<{
  navigateUp: []
  navigateToRoot: []
  navigateTo: [card: ZettleCardData]
}>()
</script>
