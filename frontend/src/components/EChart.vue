<template>
  <div ref="chartRef" style="width: 100%; height: 400px;"></div>
</template>

<script setup>
import * as echarts from 'echarts'

import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const chartRef = ref(null)

let chartInstance = null

const dataTop10 = []

const setChartOptions = () => {
  chartInstance.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      top: '1%',
      left: 'left'
    },
    series: [
      {
        name: '',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        padAngle: 5,
        itemStyle: {
          borderRadius: 15
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 10,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: true
        },
        data: dataTop10.value
      }
    ]
  })
}

const getTop10 = async () => {
  dataTop10.value = props.data
}

onMounted(async () => {
  await getTop10()

  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value)
    await setChartOptions()
  }
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
})
</script>
