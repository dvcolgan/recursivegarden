<template>
  <div class="h-full w-full">
    <!-- Header -->
    <Header
      :active-card="activeCard"
      :breadcrumbs="breadcrumbs"
      :card-count="displayedCards.length"
      @navigate-up="navigateUp"
      @navigate-to-root="navigateToRoot"
      @navigate-to="navigateToCard" />

    <!-- Main Content Area -->
    <div
      ref="container"
      class="relative h-full w-full overflow-hidden bg-green-700"
      :class="{ 'ml-72': activeCard }"
      @mousedown="startPan"
      @mousemove="handleMouseMove"
      @mouseup="handleMouseUp"
      @mouseleave="handleMouseUp"
      @wheel.prevent="handleZoom">
      <div
        class="absolute h-full w-full"
        :style="{
          transform: `translate(${viewPosition.x}px, ${viewPosition.y}px) scale(${viewPosition.zoom})`,
          transformOrigin: '0 0',
        }">
        <ZettleCard
          v-for="card in displayedCards"
          :key="card.uuid"
          :card="card"
          :isDragging="isDragging && draggedCard?.uuid === card.uuid"
          @click="navigateToCard(card)"
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
          <div>Cards: {{ displayedCards.length }}</div>
        </div>
      </div>
    </div>

    <!-- Sidebar -->
    <Sidebar
      :active-card="activeCard"
      :prev-card="prevCard"
      :next-card="nextCard"
      @navigate="navigateToCard" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ZettleCard from './ZettleCard.vue'
import Header from './Header.vue'
import Sidebar from './Sidebar.vue'
import type { ZettleCardData } from './types'

// Track mouse position globally
window.mouseX = 0
window.mouseY = 0

const route = useRoute()
const router = useRouter()

// Constants
const ZOOM_LEVELS = [0.25, 0.5, 1, 2, 4]

// State
const cards = ref<ZettleCardData[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const container = ref<HTMLElement | null>(null)

// Navigation state
const activeCard = ref<ZettleCardData | null>(null)
const breadcrumbs = ref<ZettleCardData[]>([])

// Computed view position from route query
const viewPosition = computed(() => ({
  x: Number(route.query.x) || 0,
  y: Number(route.query.y) || 0,
  zoom: ZOOM_LEVELS.includes(Number(route.query.zoom)) ? Number(route.query.zoom) : 1,
}))

// Filtered cards based on current context
const displayedCards = computed(() => {
  const parentUuid = route.query.parent as string | undefined
  return cards.value.filter((card) => {
    if (!parentUuid) {
      // In root view, show only cards without parents
      return !card.parent
    }
    // In focused view, show only direct children of current parent
    return card.parent === parentUuid
  })
})

// Navigation helpers
const prevCard = computed(() => {
  if (!activeCard.value) return null
  const index = displayedCards.value.findIndex((c) => c.uuid === activeCard.value?.uuid)
  return index > 0 ? displayedCards.value[index - 1] : null
})

const nextCard = computed(() => {
  if (!activeCard.value) return null
  const index = displayedCards.value.findIndex((c) => c.uuid === activeCard.value?.uuid)
  return index < displayedCards.value.length - 1 ? displayedCards.value[index + 1] : null
})

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
const draggedCard = ref<ZettleCardData | null>(null)

// Navigation functions
async function navigateToCard(card: ZettleCardData) {
  updateRouteQuery({ parent: card.uuid })
  await fetchCards()
  activeCard.value = card
  await updateBreadcrumbs(card)
}

async function navigateUp() {
  if (!activeCard.value?.parent) {
    navigateToRoot()
    return
  }
  const response = await fetch(`/api/cards/${activeCard.value.parent}/`)
  const parentCard = await response.json()
  navigateToCard(parentCard)
}

function navigateToRoot() {
  updateRouteQuery({ parent: undefined })
  fetchCards()
  activeCard.value = null
  breadcrumbs.value = []
}

async function updateBreadcrumbs(card: ZettleCardData) {
  const crumbs: ZettleCardData[] = [card]
  let current = card

  while (current.parent) {
    const response = await fetch(`/api/cards/${current.parent}/`)
    const parentCard = await response.json()
    crumbs.unshift(parentCard)
    current = parentCard
  }

  breadcrumbs.value = crumbs
}

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
  if (draggedCard.value) return

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
  draggedCard.value = card
  const { x, y } = getRelativeMousePosition(e)
  dragStart.x = x
  dragStart.y = y
  dragStart.cardX = card.x
  dragStart.cardY = card.y
}

function handleMouseMove(e: MouseEvent) {
  // Update global mouse position
  window.mouseX = e.clientX
  window.mouseY = e.clientY

  if (!isDragging.value) return

  const { x, y } = getRelativeMousePosition(e)

  if (draggedCard.value) {
    // Card dragging - scale movement by zoom level
    const dx = (x - dragStart.x) / viewPosition.value.zoom
    const dy = (y - dragStart.y) / viewPosition.value.zoom
    draggedCard.value.x = dragStart.cardX + dx
    draggedCard.value.y = dragStart.cardY + dy
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

function updateRouteQuery(updates: Partial<typeof viewPosition.value & { parent?: string }>) {
  router.replace({
    query: {
      ...route.query,
      ...updates,
    },
  })
}

async function handleMouseUp() {
  if (draggedCard.value) {
    try {
      const response = await fetch(`/api/cards/${draggedCard.value.uuid}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': window.CSRF_TOKEN,
        },
        body: JSON.stringify({
          x: Math.round(draggedCard.value.x),
          y: Math.round(draggedCard.value.y),
        }),
      })

      if (!response.ok) throw new Error('Failed to update card position')
    } catch (e) {
      error.value = 'Failed to save card position'
      console.error(e)
    }
  }

  isDragging.value = false
  draggedCard.value = null
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

// Fetch cards with optional parent filter
const fetchCards = async () => {
  try {
    loading.value = true
    const url = new URL('/api/cards/', window.location.origin)
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    cards.value = data.results || data

    // If we're focusing on a card, make sure it's in our card list
    const parentUuid = route.query.parent as string | undefined
    if (parentUuid && !cards.value.find((c) => c.uuid === parentUuid)) {
      const parentResponse = await fetch(`/api/cards/${parentUuid}/`)
      if (parentResponse.ok) {
        const parentCard = await parentResponse.json()
        cards.value = [parentCard, ...cards.value]
      }
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error'
    console.error('Error fetching cards:', e)
  } finally {
    loading.value = false
  }
}

// Initialize
onMounted(async () => {
  // Center the view if no coordinates are provided
  if (!route.query.x && !route.query.y && container.value) {
    const rect = container.value.getBoundingClientRect()
    updateRouteQuery({
      x: rect.width / 2,
      y: rect.height / 2,
      zoom: 1,
    })
  }

  // Load initial card if parent parameter is present
  const parentUuid = route.query.parent as string
  if (parentUuid) {
    const response = await fetch(`/api/cards/${parentUuid}/`)
    const card = await response.json()
    activeCard.value = card
    await updateBreadcrumbs(card)
  }

  fetchCards()
})
</script>
