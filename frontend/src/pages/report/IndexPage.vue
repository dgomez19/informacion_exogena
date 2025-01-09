<template>
  <q-page padding>
    <div class="row no-wrap justify-between items-center q-mb-md">
      <div class="col-md-2 col-xs-2">
        <span style="font-size: large; color: #1976D2;"> REPORTES GENERADOS </span>
      </div>

      <div class="col-md-10 col-xs-10" style="text-align: right;">

        <q-btn outline color="primary" icon="refresh" class="q-px-sm" :disable="loading" @click="load">
          <q-tooltip>Refrescar registros</q-tooltip>
        </q-btn>
      </div>
    </div>

    <q-table flat bordered virtual-scroll color="primary" class="" :loading="loading" :columns="columns" :rows="buyers" v-model:pagination="pagination" :rows-per-page-options="[10, 20, 40, 80, 100]" row-key="uuid" @request="request">

      <template #loading>
        <q-inner-loading showing>
          <q-spinner-ios size="md" color="primary"/>
        </q-inner-loading>
      </template>

      <template #body-cell-download_excel="props">
        <q-td :props="props">
          <q-btn round size="xs" color="primary" icon="download" @click="download(props.row.file_excel)">
            <q-tooltip>
              Descargar archivo en EXCEL
            </q-tooltip>
          </q-btn>
        </q-td>
      </template>

      <template #body-cell-download_pdf="props">
        <q-td :props="props">
          <q-btn round size="xs" color="green" icon="download" @click="download(props.row.file_pdf)">
            <q-tooltip>
              Descargar archivo en PDF
            </q-tooltip>
          </q-btn>
        </q-td>
      </template>

      <template #body-cell-view="props">
        <q-td :props="props">
          <q-btn round size="xs" color="warning" icon="visibility" @click="view(props.row)">
            <q-tooltip>
              Ver detalles
            </q-tooltip>
          </q-btn>
        </q-td>
      </template>
    </q-table>

    <!-- INICIO -->
    <template>
      <q-dialog persistent v-model="dialog">
        <q-card flat bordered style="width: 100%; max-width: 1200px;">
          <q-card-section>
            <div class="row items-center no-wrap">
              <q-icon name="equalizer" size="md" class="q-mr-md" />
              <div class="col">
                <div class="text-h6">ESTADISTICAS</div>
              </div>

              <q-space />

              <q-btn round flat v-close-popup icon="close" size="md" color="negative" />
            </div>
          </q-card-section>

          <q-card-section>
            <q-form ref="$form" class="column q-gutter-y-sm">
              <div class="row">
                <div class="col-md-6 col-xs-6 form-group">
                  <e-chart :data="dialogData" />
                </div>

                <div class="col-md-6 col-xs-6 form-group">
                  <strong> # REGISTROS:</strong>
                  {{dataDetail.number_records.toLocaleString('es-ES')}}
                  <e-chart :data="numberRecords" />
                </div>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-dialog>
    </template>
    <!-- FIN -->

  </q-page>
</template>

<script setup>
import EChart from 'src/components/EChart.vue'

import { nextTick, onMounted, ref } from 'vue'

import { api } from 'src/boot/axios'

import moment from 'moment'

const columns = [
  { name: 'created', align: 'center', label: 'FECHA GENERACIÓN', field: data => moment(data.created), format: val => val.format('YYYY-MM-DD HH:mm:ss'), sortable: true },
  { name: 'status', align: 'center', label: 'ESTADO', field: data => data.status?.description },
  { name: 'number_records', align: 'center', label: 'NUMERO DE REGISTROS', field: 'number_records', format: val => val ? val.toLocaleString('es-ES') : 0 },
  { name: 'download_excel', align: 'center', label: 'DESCARGAR EXCEL' },
  { name: 'download_pdf', align: 'center', label: 'DESCARGAR PDF' },
  { name: 'view', align: 'center', label: 'VER DETALLES' }
]

const loading = ref(false)

const dialog = ref(false)

const dialogData = ref({})

const dataDetail = ref({})

const numberRecords = ref({})

const pagination = ref({
  filter: '',
  page: 1,
  rowsPerPage: 10
})

const buyers = ref([])

const request = async ({ pagination: pagination_ }) => {
  loading.value = true

  const params = new URLSearchParams({
    page: pagination_.page,
    size: pagination_.rowsPerPage
  })

  if (pagination_.filter) params.set('search', pagination_.filter)
  if (pagination_.sortBy) params.set('ordering', (pagination_.descending ? '-' : '') + pagination_.sortBy)

  try {
    const { data } = await api.get('core/report/')
    buyers.value = data.results
    pagination.value = { ...pagination_, rowsNumber: data?.count }
  } catch (err) {}

  loading.value = false
}

const load = async () => await request({ pagination: { ...pagination.value, page: 1 } })

const setLoading = async (value) => {
  await nextTick()
  loading.value = value
}

const download = (file) => {
  window.open(file, '_blank')
}

const view = (row) => {
  dialog.value = true
  dataDetail.value = row

  numberRecords.value = [
    {
      name: '# Registros',
      value: row.number_records
    }
  ]

  dialogData.value = [
    {
      name: '# Direcciones',
      value: row.address
    },
    {
      name: '# Celulares',
      value: row.cell_phone
    },
    {
      name: '# Teléfonos',
      value: row.phone
    },
    {
      name: '# Correos',
      value: row.email
    }
  ]
}

onMounted(() => load())

defineExpose({ load, setLoading })
</script>
