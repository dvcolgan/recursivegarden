<template>
  <div
    ref="container"
    class="relative h-full w-full overflow-hidden bg-green-700"
    @mousedown="startPan"
    @mousemove="handleMouseMove"
    @mouseup="handleMouseUp"
    @wheel.prevent="handleZoom">
    <div
      class="absolute h-full w-full"
      :style="{
        transform: `translate(${viewPosition.x}px, ${viewPosition.y}px) scale(${viewPosition.zoom})`,
        transformOrigin: '0 0',
      }">
      <ZettleCard
        v-for="card in cards"
        :key="card.uuid"
        :card="card"
        :isDragging="isDragging && activeCard?.uuid === card.uuid"
        @dragStart="startDrag($event, card)" />
    </div>

    <!-- Overlay container for UI elements -->
    <div class="pointer-events-none absolute inset-0">
      <!-- Loading State -->
      <div
        v-if="loading"
        class="pointer-events-auto absolute top-4 right-4 rounded-lg bg-white p-4 shadow-lg">
        <div
          class="h-5 w-5 animate-spin rounded-full border-2 border-green-900 border-t-transparent">
        </div>
      </div>

      <!-- Error State -->
      <div
        v-if="error"
        class="pointer-events-auto absolute top-4 right-4 rounded-lg bg-red-100 p-4 text-red-900 shadow-lg">
        {{ error }}
      </div>

      <!-- Debug Info -->
      <div
        class="pointer-events-auto absolute right-4 bottom-4 rounded-lg bg-white p-4 text-sm shadow-lg">
        <div>Zoom: {{ viewPosition.zoom }}</div>
        <div>View: {{ Math.round(viewPosition.x) }}, {{ Math.round(viewPosition.y) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ZettleCard from './ZettleCard.vue'
import type { ZettleCardData } from './types'

const route = useRoute()
const router = useRouter()

// Computed view position from route query
const viewPosition = computed(() => ({
  x: Number(route.query.x) || 0,
  y: Number(route.query.y) || 0,
  zoom: ZOOM_LEVELS.includes(Number(route.query.zoom)) ? Number(route.query.zoom) : 1,
}))

// Constants
const ZOOM_LEVELS = [0.25, 0.5, 1, 2, 4]

// State
const cards = ref<ZettleCardData[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const container = ref<HTMLElement | null>(null)

// Dragging state
const isDragging = ref(false)
const dragStart = reactive({
  x: 0,
  y: 0,
  viewX: 0,
  viewY: 0,
  cardX: 0,
  cardY: 0,
})
const activeCard = ref<ZettleCardData | null>(null)

// Get mouse position relative to container
function getRelativeMousePosition(e: MouseEvent) {
  if (!container.value) return { x: 0, y: 0 }
  const rect = container.value.getBoundingClientRect()
  return {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top,
  }
}

// Pan handling
function startPan(e: MouseEvent) {
  if (activeCard.value) return

  isDragging.value = true
  const { x, y } = getRelativeMousePosition(e)
  dragStart.x = x
  dragStart.y = y
  dragStart.viewX = viewPosition.value.x
  dragStart.viewY = viewPosition.value.y
}

// Card drag handling
function startDrag(e: MouseEvent, card: ZettleCardData) {
  isDragging.value = true
  activeCard.value = card
  const { x, y } = getRelativeMousePosition(e)
  dragStart.x = x
  dragStart.y = y
  dragStart.cardX = card.x
  dragStart.cardY = card.y
}

function handleMouseMove(e: MouseEvent) {
  if (!isDragging.value) return

  const { x, y } = getRelativeMousePosition(e)

  if (activeCard.value) {
    // Card dragging - scale movement by zoom level
    const dx = (x - dragStart.x) / viewPosition.value.zoom
    const dy = (y - dragStart.y) / viewPosition.value.zoom
    activeCard.value.x = dragStart.cardX + dx
    activeCard.value.y = dragStart.cardY + dy
  } else {
    // Canvas panning
    const dx = x - dragStart.x
    const dy = y - dragStart.y
    updateRouteQuery({
      x: dragStart.viewX + dx,
      y: dragStart.viewY + dy,
    })
  }
}

function updateRouteQuery(updates: Partial<typeof viewPosition.value>) {
  router.replace({
    query: {
      ...route.query,
      ...updates,
    },
  })
}

async function handleMouseUp() {
  if (activeCard.value) {
    try {
      const response = await fetch(`/api/cards/${activeCard.value.uuid}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': window.CSRF_TOKEN,
        },
        body: JSON.stringify({
          x: Math.round(activeCard.value.x),
          y: Math.round(activeCard.value.y),
        }),
      })

      if (!response.ok) throw new Error('Failed to update card position')
    } catch (e) {
      error.value = 'Failed to save card position'
      console.error(e)
    }
  }

  isDragging.value = false
  activeCard.value = null
}

function handleZoom(e: WheelEvent) {
  if (!container.value) return

  const oldZoom = viewPosition.value.zoom

  // Calculate new zoom level
  const currentZoomIndex = ZOOM_LEVELS.indexOf(oldZoom)
  const newZoomIndex =
    e.deltaY > 0
      ? Math.max(0, currentZoomIndex - 1)
      : Math.min(ZOOM_LEVELS.length - 1, currentZoomIndex + 1)
  const newZoom = ZOOM_LEVELS[newZoomIndex]

  if (newZoom === oldZoom) return

  // Get mouse position relative to container
  const { x: mouseX, y: mouseY } = getRelativeMousePosition(e)

  // Calculate the point to zoom around (in world space)
  const worldX = (mouseX - viewPosition.value.x) / oldZoom
  const worldY = (mouseY - viewPosition.value.y) / oldZoom

  // Update view position to zoom around mouse point
  updateRouteQuery({
    zoom: newZoom,
    x: mouseX - worldX * newZoom,
    y: mouseY - worldY * newZoom,
  })
}

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
    error.value = e instanceof Error ? e.message : 'Unknown error'
    console.error('Error fetching cards:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Center the view if no coordinates are provided
  if (!route.query.x && !route.query.y && container.value) {
    const rect = container.value.getBoundingClientRect()
    updateRouteQuery({
      x: rect.width / 2,
      y: rect.height / 2,
      zoom: 1,
    })
  }
  fetchCards()
})
</script>
