<template>
  <div class="row no-wrap justify-between items-center q-mb-md">
    <div class="col-md-4 col-xs-4">
      <q-input v-model="pagination.filter" outlined dense :debounce="500" placeholder="Buscar por nombres, documento, correo electrónico o teléfono" class="col-4" @update:model-value="load">
        <template #prepend>
          <q-icon name="search" />
        </template>
      </q-input>
    </div>

    <div class="col-md-4 col-xs-4">
      <q-input outlined dense v-model="dateBuild" readonly label="Fecha">
        <template #after>
          <q-btn icon="event" round color="primary">
            <q-tooltip>Seleccione las fechas</q-tooltip>
            <q-popup-proxy @before-show="updateProxy" transition-show="scale" transition-hide="scale">
              <q-date v-model="dateSearch" range>
                <div class="row items-center justify-end q-gutter-sm">
                  <q-btn label="Cancel" color="primary" flat v-close-popup />
                  <q-btn label="OK" color="primary" flat @click="save" v-close-popup />
                </div>
              </q-date>
            </q-popup-proxy>
          </q-btn>
        </template>
      </q-input>
    </div>

    <div class="row q-gutter-x-md">
      <q-btn color="green" icon="download" class="primary" :disable="loading" @click="downloadExcel">
        <q-tooltip>Descargar datos en excel</q-tooltip>
      </q-btn>

      <q-btn outline color="primary" icon="restart_alt" class="q-px-sm" :disable="loading" @click="load">
        <q-tooltip>Recargar registros</q-tooltip>
      </q-btn>
    </div>
  </div>

  <div class="row no-wrap justify-between items-center q-mb-md">
    <div class="row justify-between q-gutter-x-md">
    </div>
  </div>

  <q-table flat bordered virtual-scroll color="primary" class="" :loading="loading" :columns="columns" :rows="buyers" v-model:pagination="pagination" :rows-per-page-options="[10, 20, 40, 80, 100]" row-key="uuid" @request="request">

    <template #loading>
      <q-inner-loading showing>
        <q-spinner-ios size="md" color="primary"/>
      </q-inner-loading>
    </template>

    <template #body-cell-file="props">
      <q-td :props="props">
        <i class="text-grey-8">
          {{props.row.file.name}}
        </i> <br>
        {{ moment(props.row.file.file_date).format('YYYY-MM-DD HH:mm:ss') }}
      </q-td>
    </template>

    <template #body-cell-number_document="props">
      <q-td :props="props">
        <i class="text-grey-8">
          {{ props.row.type_document.description }}
        </i> <br>
        {{ props.row.number_document }}
      </q-td>
    </template>

    <template #body-cell-names="props">
      <q-td :props="props">
        {{ props.row.social_reason }}
        {{ props.row.surnames }}
      </q-td>
    </template>

    <template #body-cell-is_active="props">
      <q-td :props="props">
        <q-toggle color="primary" v-model="props.row.is_active" size="xs" checked-icon="check" unchecked-icon="clear" @update:model-value="() => $emit('toggle-active', props.row)" :disable="loading" />
      </q-td>
    </template>

    <template #body-cell-options="props">
      <q-td :props="props">
        <q-btn flat round color="dark" size="sm" icon="more_vert" @click="event => showMenu(event, props.row)" :disable="loading" />
      </q-td>
    </template>
  </q-table>
</template>

<script setup>
import { nextTick, onMounted, ref } from 'vue'

import { api } from 'src/boot/axios'

import { download } from 'src/lib/documents'

import moment from 'moment'

const dateBuild = ref(null)

const dateSend = ref(null)

const dateSearch = ref(null)

const date = ref(moment().format('YYYY/MM/DD'))

const $emit = defineEmits(['create', 'toggle-active', 'reset-password', 'update', 'delete'])

const columns = [
  { name: 'file', align: 'center', label: 'Información del archivo', field: file => moment(file.file_date), format: val => val.format('YYYY-MM-DD HH:mm:ss'), sortable: true },
  { name: 'number_document', align: 'center', label: 'Documento', field: 'number_document', format: numberDocument => numberDocument || 'Sin documento' },
  { name: 'names', align: 'center', label: 'Nombres completos', field: 'names' },
  { name: 'phone', align: 'center', label: 'Teléfono', field: 'phone' },
  { name: 'cell_phone', align: 'center', label: 'Celular', field: 'cell_phone' },
  { name: 'email', align: 'center', label: 'Correo electrónico', field: 'email', format: email => email || 'Sin correo electrónico' },
  { name: 'address', align: 'center', label: 'Dirección', field: 'address' },
  { name: 'compound_address', align: 'center', label: 'Dirección compuesta', field: 'compound_address' },
  { name: 'department', align: 'center', label: 'Departamento', field: 'department' },
  { name: 'municipality', align: 'center', label: 'Municipio', field: 'municipality' },
  { name: 'country', align: 'center', label: 'País', field: 'country' },
  { name: 'notification_address', align: 'center', label: 'Dirección de notificación', field: 'notification_address' },
  { name: 'options', align: 'center' }
]

const $menu = ref(null)

const loading = ref(false)

const pagination = ref({
  filter: '',
  page: 1,
  rowsPerPage: 10
})

const buyers = ref([])

const showMenu = async (event, row) => $menu.value.show(event, row)

const request = async ({ pagination: pagination_ }) => {
  loading.value = true

  const filterDate = dateSend.value !== null ? '&created=' + dateSend.value : ''

  console.log('filterDate', filterDate)

  const params = new URLSearchParams({
    page: pagination_.page,
    size: pagination_.rowsPerPage
  })

  if (pagination_.filter) params.set('search', pagination_.filter)
  if (pagination_.sortBy) params.set('ordering', (pagination_.descending ? '-' : '') + pagination_.sortBy)

  try {
    const { data } = await api.get(`core/file-detail/?${params}${filterDate}`)
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

const downloadExcel = async () => {
  loading.value = true
  await download('core/report-file-detail/')
  loading.value = false
}

const updateProxy = () => {
  dateSearch.value = date.value
}

const save = () => {
  if (dateSearch.value.from !== undefined && dateSearch.value.to !== undefined) {
    dateBuild.value = 'Del ' + fechaFormated(dateSearch.value.from) + ' al ' + fechaFormated(dateSearch.value.to)
    dateSend.value = fechaFormated(dateSearch.value.from) + ':' + fechaFormated(dateSearch.value.to)
    load()
  }
}

const fechaFormated = (fecha) => {
  if (fecha) return moment(fecha).format('YYYY-MM-DD')
  return ''
}

onMounted(() => load())

defineExpose({ load, setLoading })
</script>
