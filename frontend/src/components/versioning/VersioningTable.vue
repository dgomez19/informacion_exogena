<template>
  <div class="row no-wrap justify-between items-center q-mb-md">
    <div class="row q-gutter-x-md">
      <q-btn outline color="primary" icon="restart_alt" class="q-px-sm" :disable="loading" @click="load">
        <q-tooltip>Recargar registros</q-tooltip>
      </q-btn>

      <q-btn unelevated no-caps color="primary" icon="add" label="Agregar cargue" @click="$emit('create')"/>
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

    <template #body-cell-close="props">
      <q-td :props="props">
        <q-toggle v-if="!props.row.close" color="primary" v-model="props.row.close" size="xs" checked-icon="check" unchecked-icon="clear" @update:model-value="() => close(props.row)" />
        <q-badge v-else outline color="red" label="Cerrado" />
      </q-td>
    </template>
  </q-table>

  <context-menu ref="$menu" :items="MENU_ITEMS" />
</template>

<script setup>
import { nextTick, onMounted, ref } from 'vue'

import { api } from 'src/boot/axios'

import moment from 'moment'

import ContextMenu from 'src/components/ContextMenu.vue'

import { useRouter } from 'vue-router'

import { Notify, Dialog } from 'quasar'

const $router = useRouter()

const $emit = defineEmits(['create', 'toggle-active', 'reset-password', 'update', 'delete'])

const columns = [
  { name: 'created', align: 'center', label: 'FECHA DEL CARGUE', field: 'created' },
  { name: 'name', align: 'center', label: 'NOMBRE', field: 'name' },
  { name: 'get_files', align: 'center', label: 'CANTIDAD DE ARCHIVOS', field: 'get_files' },
  { name: 'close', align: 'center', label: '¿CERRAR?' },
  { name: 'options', align: 'center' }
]

const MENU_ITEMS = [
  { icon: 'edit', label: 'Editar', click: row => $emit('update', row) },
  { icon: 'delete_forever', label: 'Eliminar', click: row => $emit('delete', row) },
  { icon: 'upload', label: 'Cargar archivos', click: row => upload(row.uuid) }
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

  const params = new URLSearchParams({
    page: pagination_.page,
    size: pagination_.rowsPerPage
  })

  if (pagination_.filter) params.set('search', pagination_.filter)
  if (pagination_.sortBy) params.set('ordering', (pagination_.descending ? '-' : '') + pagination_.sortBy)

  try {
    const { data } = await api.get(`core/versioning/?${params}`)
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

const upload = (uuid) => {
  $router.push(`${uuid}/upload-file`)
}

const close = async (row) => {
  if (!row.close) {
    return false
  }

  loading.value = true

  const callback = async () => {
    try {
      await api.put(`core/versioning/${row.uuid}/`, { ...row, close: row.close })

      Notify.create({
        type: 'success',
        message: 'Se ha cerrado el cargue exitosamente.'
      })
    } catch (err) {}
  }

  loading.value = false

  Dialog.create({
    title: '¿Está segura/ro que desea cerrar este ciclo?',
    message: 'No podrá cargar mas archivos.',
    componentProps: { flat: true, bordered: true },
    ok: { unelevated: true, noCaps: true, color: 'primary', label: 'Sí, cerrar cargue' },
    cancel: { outline: true, noCaps: true, color: 'primary', label: 'Cancelar' }
  }).onOk(() => {
    callback()
  }).onCancel(() => {
    row.close = false
  })
}

onMounted(() => load())

defineExpose({ load, setLoading })
</script>
