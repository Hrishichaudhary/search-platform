<template>
  <div class="container mx-auto p-6">
    <h1 class="text-4xl font-bold mb-6 text-center text-blue-800">Search Patents or Papers</h1>
    
    <!-- Search Bar and Filters -->
    <div class="mb-6 bg-gray-100 p-4 rounded-lg shadow">
      <form class="flex flex-col gap-4 md:flex-row md:items-end" @submit.prevent="search">
        <input
          v-model="query.text"
          type="text"
          placeholder="Type a keyword"
          class="border p-3 rounded w-full focus:outline-blue-400"
        >
        <select v-model="query.doc_type" class="border p-3 rounded w-full md:w-44">
          <option value="both">Both</option>
          <option value="paper">Papers</option>
          <option value="patent">Patents</option>
        </select>
        <input
          v-model="query.date_range_start"
          type="number"
          placeholder="Start Year"
          class="border p-3 rounded w-full md:w-32"
        />
        <input
          v-model="query.date_range_end"
          type="number"
          placeholder="End Year"
          class="border p-3 rounded w-full md:w-32"
        />
        <input
          v-model="query.citation_min"
          type="number"
          min="0"
          placeholder="Min Citations"
          class="border p-3 rounded w-full md:w-36"
        />
        
        <button
          type="submit"
          class="bg-blue-600 text-white p-3 rounded hover:bg-blue-700 transition w-full md:w-32"
        >Search</button>
      </form>
    </div>

    <!-- Gray Bee branding section (only when blank, not searching, no error) -->
    <div
      v-if="(!Array.isArray(results.documents) || !results.documents.length) && !loading && !results.error"
      class="flex flex-col items-center justify-center py-14 text-gray-500"
    >
      <!-- Big Bee above last 'e', resized proportionally -->
      <h2 class="text-5xl font-extrabold mb-2 tracking-tight flex justify-center items-end" style="color:#7b7b7c">
        Gray Be
        <span class="inline-block relative w-[1.2ch]">
          <span class="block relative">
            e
            <!-- CHANGED: w-24, -top-20, object-contain. No fixed height. -->
            <img
              src="/gray-bee.PNG"
              alt="Bee"
              class="absolute left-1/2 -top-5 object-contain grayscale drop-shadow animate-bounce-slow"
              style="width: 500px; transform: translateX(-50%);"
            >
          </span>
        </span>
      </h2>
      <p class="text-xl font-medium mb-4">Welcome to GrayB’s semantic document explorer</p>
      <span class="rounded-full px-4 py-2 bg-gray-100 text-gray-700 font-semibold shadow">
        Start searching to explore knowledge!
      </span>
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="flex flex-col items-center my-8">
      <span class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mb-2"></span>
      <span class="text-blue-700 font-semibold">Searching...</span>
    </div>

    <!-- Error Message -->
    <div v-if="results.error && !loading" class="mb-6 text-center text-red-600">
      {{ results.error }}
      <div v-if="results.error.includes('No results found')">
        <br>
        <span class="text-gray-700">
          Tip: Try using a more general question.
        </span>
      </div>
    </div>

    <!-- Results as beautiful cards -->
    <div v-if="Array.isArray(results.documents) && results.documents.length && !loading" class="mb-6">
      <h2 class="text-2xl font-semibold mb-4 text-blue-700">Results ({{ results.documents.length }})</h2>
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="doc in results.documents"
          :key="doc.id"
          class="bg-white border border-gray-200 rounded-xl shadow-lg hover:shadow-2xl transition-shadow duration-200 flex flex-col"
        >
          <div class="p-6 flex-1 flex flex-col">
            <h3 class="text-lg font-bold text-blue-800 mb-2 line-clamp-2 flex items-center">
              {{ doc.title || 'Untitled' }}
              <span
                v-if="doc.doc_type === 'patent'"
                class="ml-2 px-2 py-1 text-xs bg-green-100 text-green-800 rounded"
              >Patent</span>
              <span
                v-else
                class="ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded"
              >Paper</span>
            </h3>
            <div class="flex flex-wrap gap-x-4 gap-y-1 text-sm text-gray-700 mb-2">
              <span><span class="font-semibold">Type:</span> {{ doc.doc_type }}</span>
              <span><span class="font-semibold">Year:</span> {{ doc.pub_date }}</span>
              <span><span class="font-semibold">Citations:</span> {{ doc.citation_count }}</span>
            </div>
            <div class="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-600 mb-2">
              <span><span class="font-semibold">Field:</span> {{ doc.field_of_research || 'None' }}</span>
              <span><span class="font-semibold">Sub-topic:</span> {{ doc.sub_topic || 'None' }}</span>
            </div>
            <p class="text-gray-600 mt-2 text-sm line-clamp-4">{{ doc.abstract ? doc.abstract.slice(0, 200) : 'No abstract' }}...</p>
          </div>
          <div class="bg-blue-50 px-6 py-2 rounded-b-xl text-xs text-blue-700 font-semibold border-t border-blue-100">
            ID: {{ doc.id }}
          </div>
        </div>
      </div>
    </div>

    <!-- Stylish No Results message -->
    <div v-else-if="searched && !loading" class="mb-6 text-center">
      <span class="inline-block bg-red-100 text-red-700 px-4 py-2 rounded">No results found</span>
    </div>
    
    <!-- Heatmap Visualization -->
    <div v-if="results.trends && Object.keys(results.trends).length && !loading" class="mb-6">
      <h2 class="text-2xl font-semibold mb-4">Sub-topic Trends</h2>
      <div class="bg-white rounded-xl p-4 shadow">
        <canvas id="heatmap" style="width:100%;min-height:350px;max-height:500px;"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
import { MatrixController, MatrixElement } from 'chartjs-chart-matrix'
Chart.register(...registerables, MatrixController, MatrixElement)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/search'

const query = ref({
  text: '',
  doc_type: 'both',
  date_range_start: '',
  date_range_end: '',
  citation_min: '',
  field_of_research: ''
})
const results = ref({ documents: [], trends: {}, velocity: {} })
const searched = ref(false)
const loading = ref(false)
let chart = null

const search = async () => {
  loading.value = true
  try {
    if (!query.value.text) {
      searched.value = true
      results.value = { documents: [], trends: {}, velocity: {} }
      renderHeatmap()
      loading.value = false
      return
    }
    results.value = { documents: [], trends: {}, velocity: {} }
    searched.value = false

    const safeQuery = {
      text: query.value.text,
      doc_type: query.value.doc_type,
      date_range: (query.value.date_range_start && query.value.date_range_end)
        ? [String(query.value.date_range_start), String(query.value.date_range_end)]
        : undefined,
      citation_min: query.value.citation_min ? Number(query.value.citation_min) : undefined,
      field_of_research: query.value.field_of_research || undefined
    }

    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(safeQuery)
    })
    if (!response.ok) throw new Error(`API request failed: ${response.status}`)
    results.value = await response.json()
    searched.value = true
    await nextTick()
    renderHeatmap()
  } catch (error) {
    searched.value = true
    results.value = { documents: [], trends: {}, velocity: {}, error: error.message }
    renderHeatmap()
  } finally {
    loading.value = false
  }
}

const renderHeatmap = () => {
  const ctx = document.getElementById('heatmap')?.getContext('2d')
  if (!ctx) {
    if (chart) chart.destroy()
    return
  }
  if (chart) chart.destroy()

  const topics = Object.keys(results.value.trends || {})
  const years = [...new Set(Object.values(results.value.trends || {}).flatMap(t => Object.keys(t)))].sort()

  const hasData =
    topics.length > 0 &&
    years.length > 0 &&
    topics.some(topic => years.some(year => results.value.trends[topic][year]))

  if (!hasData) return

  const data = topics.map(topic =>
    years.map(year => results.value.trends[topic][year] || 0)
  )

  chart = new Chart(ctx, {
    type: 'matrix',
    data: {
      datasets: [{
        label: 'Documents per Sub-topic',
        data: data.flatMap((row, i) =>
          row.map((value, j) => ({ x: j, y: i, v: value }))
        ),
        backgroundColor: (ctx) => {
          const value = ctx.raw?.v || 0
          const max = Math.max(...data.flat())
          const alpha = max ? value / max : 0
          return `rgba(0, 128, 255, ${alpha})`
        },
        width: ({ chart }) => chart.chartArea ? chart.chartArea.width / years.length : 20,
        height: ({ chart }) => chart.chartArea ? chart.chartArea.height / topics.length : 20
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const topic = topics[ctx.raw.y]
              const year = years[ctx.raw.x]
              return `Sub-topic: ${topic}, Year: ${year}, Documents: ${ctx.raw.v}`
            }
          }
        },
        legend: { display: false }
      },
      scales: {
        x: {
          type: 'category',
          labels: years,
          title: { display: true, text: 'Year' }
        },
        y: {
          type: 'category',
          labels: topics,
          title: { display: true, text: 'Sub-topic' }
        }
      }
    }
  })
}

watch(() => results.value.trends, () => {
  nextTick().then(renderHeatmap)
})
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;  
  overflow: hidden;
}
.line-clamp-4 {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;  
  overflow: hidden;
}

/* Smooth bee bounce animation */
@keyframes bounce-slow {
  0%, 100% { transform: translateY(0px);}
  50% { transform: translateY(-12px);}
}
.animate-bounce-slow {
  animation: bounce-slow 2.8s infinite;
}
</style>
