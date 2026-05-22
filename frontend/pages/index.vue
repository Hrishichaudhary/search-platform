<template>
  <div class="container mx-auto p-6">
    <h1 class="text-4xl font-bold mb-6 text-center text-blue-800">
      RAG-powered research search engine
    </h1>

    <div class="mb-6 bg-gray-100 p-4 rounded-lg shadow">
      <form
        class="flex flex-col gap-4 md:flex-row md:items-end"
        @submit.prevent="search"
      >

        <input
          v-model="query.text"
          type="text"
          placeholder="Type a keyword....eg. machine learning"
          class="border p-3 rounded w-full focus:outline-blue-400"
        >

        <select
          v-model="query.doc_type"
          class="border p-3 rounded w-full md:w-44"
        >
          <option value="both">Both</option>
          <option value="paper">Papers</option>
          <option value="patent">Patents</option>
        </select>

        <input
          v-model="query.date_range_start"
          type="number"
          placeholder="Start Year"
          class="border p-3 rounded w-full md:w-32"
        >

        <input
          v-model="query.date_range_end"
          type="number"
          placeholder="End Year"
          class="border p-3 rounded w-full md:w-32"
        >

        <input
          v-model="query.citation_min"
          type="number"
          min="0"
          placeholder="Min Citations"
          class="border p-3 rounded w-full md:w-36"
        >

        <button
          type="submit"
          class="bg-blue-600 text-white p-3 rounded hover:bg-blue-700 transition"
        >
          Search
        </button>

      </form>

      <div
        v-if="results.citation_warning"
        class="text-red-600 text-xs mt-2"
      >
        {{ results.citation_warning }}
      </div>

    </div>

    <div
      v-if="loading"
      class="flex flex-col items-center my-8"
    >
      <span
        class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"
      />

      <span class="text-blue-700 mt-2">
        Searching...
      </span>

    </div>

    <div
      v-if="results.error && !loading"
      class="text-red-600 mb-4"
    >
      {{ results.error }}
    </div>

    <div
      v-if="results.documents?.length && !loading"
    >

      <h2
        class="text-2xl font-semibold mb-4 text-blue-700"
      >
        Results ({{ results.documents.length }})
      </h2>

      <div
        class="grid gap-6 md:grid-cols-2 lg:grid-cols-3"
      >

        <div
          v-for="doc in results.documents"
          :key="doc.id"
          class="bg-white border rounded-xl shadow-lg flex flex-col"
        >

          <div class="p-6 flex-1">

            <h3
              class="text-lg font-bold text-blue-800 mb-2"
            >
              {{ doc.title }}

              <span
                class="ml-2 px-2 py-1 text-xs bg-blue-100 rounded"
              >
                {{ doc.doc_type }}
              </span>

            </h3>

            <div
              class="text-sm mb-2"
            >
              Type:
              {{ doc.doc_type }}

              |

              Year:
              {{ doc.pub_date }}

              |

              Citations:
              {{ doc.citation_count }}
            </div>

            <div
              class="text-xs mb-3"
            >

              Field:

              {{ doc.field_of_research }}

              |

              Sub-topic:

              {{ doc.sub_topic }}

            </div>

            <p
              class="text-gray-600 text-sm"
            >
              {{ doc.abstract?.slice(0,200) }}
            </p>

          </div>

          <div
            class="bg-blue-50 px-4 py-2 text-xs"
          >
            ID:
            {{ doc.id }}
          </div>

        </div>

      </div>

    </div>

    <div
      v-if="results.trends && Object.keys(results.trends).length"
      class="mt-8"
    >

      <h2
        class="text-2xl font-semibold mb-4"
      >
        Sub-topic Trends
      </h2>

      <div
        class="bg-white rounded-xl shadow p-4"
      >

        <div
          style="height:400px"
        >

          <canvas
            id="heatmap"
          />

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>

import {
  ref,
  nextTick,
  watch
}
from 'vue'

import {
  Chart,
  registerables
}
from 'chart.js'

import {
  MatrixController,
  MatrixElement
}
from 'chartjs-chart-matrix'


Chart.register(
  ...registerables
)

Chart.register(
  MatrixController,
  MatrixElement
)

const API_URL =
  import.meta.env.VITE_API_URL
  ||
  'http://127.0.0.1:8000/search'


const query = ref({

  text:'',

  doc_type:'both',

  date_range_start:'',

  date_range_end:'',

  citation_min:''

})


const results = ref({

  documents:[],

  trends:{},

  velocity:{},

  error:null,

  citation_warning:''

})


const loading = ref(false)

let chart = null


const search = async()=>{

  loading.value = true

  try{

    const payload={

      text:
      query.value.text,

      doc_type:
      query.value.doc_type,

      citation_min:

      query.value.citation_min

      ?

      Number(
        query.value.citation_min
      )

      :

      undefined

    }

    const response=

      await fetch(

        API_URL,

        {

          method:'POST',

          headers:{

            'Content-Type':

            'application/json'

          },

          body:

          JSON.stringify(

            payload

          )

        }

      )

    results.value=

      await response.json()

    await nextTick()

    renderHeatmap()

  }

  catch(err){

    results.value.error=

      err.message

  }

  finally{

    loading.value=false

  }

}


const renderHeatmap=()=>{

  const canvas=

    document.getElementById(

      'heatmap'

    )

  if(!canvas)return

  const ctx=

    canvas.getContext(

      '2d'

    )

  if(chart){

    chart.destroy()

  }

  const trends=

    results.value.trends

  const topics=

    Object.keys(

      trends

    )

  const years=

    [

      ...new Set(

        topics.flatMap(

          t=>

          Object.keys(

            trends[t]

          )

        )

      )

    ].sort()

  if(

    !topics.length

    ||

    !years.length

  ) return


  const matrixData=[]

  for(

    const topic

    of topics

  ){

    for(

      const year

      of years

    ){

      matrixData.push({

        x:year,

        y:topic,

        v:

        trends[topic][year]

        ||

        0

      })

    }

  }

  const max=Math.max(

    ...matrixData.map(

      x=>x.v

    ),

    1

  )

  chart=

    new Chart(

      ctx,

      {

        type:'matrix',

        data:{

          datasets:[{

            data:

            matrixData,

            backgroundColor:

            (ctx)=>{

              const value=

              ctx.raw?.v||0

              return `rgba(0,128,255,${
                value/max
              })`

            },

            width:

            ({chart})=>

            chart.chartArea

            ?

            chart.chartArea.width

            /

            years.length

            :

            25,

            height:

            ({chart})=>

            chart.chartArea

            ?

            chart.chartArea.height

            /

            topics.length

            :

            25

          }]

        },

        options:{

          responsive:true,

          maintainAspectRatio:false,

          plugins:{

            legend:{

              display:false

            }

          },

          scales:{

            x:{

              type:'category',

              labels:years

            },

            y:{

              type:'category',

              labels:topics

            }

          }

        }

      }

    )

}


watch(

()=>results.value.trends,

()=>{

nextTick().then(

renderHeatmap

)

}

)

</script>

<style>

@import
'tailwindcss/base';

@import
'tailwindcss/components';

@import
'tailwindcss/utilities';

</style>