<template>
  <div class="row no-wrap justify-between items-center q-mb-md">
    <q-input v-model="pagination.filter" outlined dense :debounce="500" placeholder="Buscar por nombres, documento, correo electrónico o teléfono" class="col-6" @update:model-value="load">
      <template #prepend>
        <q-icon name="search" />
      </template>
    </q-input>

    <div class="row q-gutter-x-md">
      <q-btn outline color="primary" icon="restart_alt" class="q-px-sm" :disable="loading" @click="load">
        <q-tooltip>Recargar registros</q-tooltip>
      </q-btn>
    </div>
  </div>

  <div class="row no-wrap justify-between items-center q-mb-md">
    <div class="row justify-between q-gutter-x-md">
    </div>
  </div>

  <q-table flat bordered virtual-scroll color="primary" class="" :loading="loading" :columns="columns" :rows="files" v-model:pagination="pagination" :rows-per-page-options="[10, 20, 40, 80, 100]" row-key="uuid" @request="request">
    <template #loading>
      <q-inner-loading showing>
        <q-spinner-ios size="md" color="primary"/>
      </q-inner-loading>
    </template>
  </q-table>
</template>

<script setup>
import { nextTick, onMounted, ref } from 'vue'

import { api } from 'src/boot/axios'

import moment from 'moment'

const columns = [
  { name: 'name', align: 'left', label: 'NOMBRE DEL ARCHIVO', field: 'name', sortable: true },
  { name: 'file_date', align: 'left', label: 'FECHA DEL ARCHIVO', field: fileDate => moment(fileDate), format: val => val.format('YYYY-MM-DD HH:mm:ss'), sortable: true },
  { name: 'created', align: 'left', label: 'FECHA DEL CARGUE', field: val => moment(val.created), format: val => val.format('YYYY-MM-DD HH:mm:ss'), sortable: true },
  { name: 'status', align: 'center', label: 'ESTADO', field: 'status', format: status => status.description || 'Sin documento' },
  { name: 'options', align: 'left' }
]

const loading = ref(false)

const pagination = ref({
  filter: '',
  page: 1,
  rowsPerPage: 10
})

const files = ref([])

const request = async ({ pagination: pagination_ }) => {
  loading.value = true

  const params = new URLSearchParams({
    page: pagination_.page,
    size: pagination_.rowsPerPage
  })

  if (pagination_.filter) params.set('search', pagination_.filter)
  if (pagination_.sortBy) params.set('ordering', (pagination_.descending ? '-' : '') + pagination_.sortBy)

  try {
    const { data } = await api.get(`core/files/?${params}`)
    files.value = data.results
    pagination.value = { ...pagination_, rowsNumber: data?.count }
  } catch (err) {}

  loading.value = false
}

const load = async () => await request({ pagination: { ...pagination.value, page: 1 } })

const setLoading = async (value) => {
  await nextTick()
  loading.value = value
}

onMounted(() => load())

defineExpose({ load, setLoading })
</script>
