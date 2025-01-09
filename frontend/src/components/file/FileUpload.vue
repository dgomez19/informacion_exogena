<template>
  <div>
    <q-form ref="$form">
      <div class="row form-group">
        <div class="col-4 col-md-12">
          <q-select outlined dense v-model="versioning" label="Tipo de cargue *" option-value="uuid" option-label="name" :options="listVersioning" lazy-rules :rules="[vals.required]" />
        </div>
      </div>

      <div class="row form-group">
        <div class="col-4 col-md-12">
          <q-uploader
            :hide-upload-btn="true"
            style="width:100%"
            multiple
            label="CARGUE AQUÍ SUS ARCHIVOS EN FORMATO CSV"
            @added="addFiles"
          />
        </div>
      </div> <br>

      <div class="row no-wrap q-gutter-x-sm">
        <div class="col-4 col-md-12">
          <q-btn unelevated no-caps size="13px" type="submit" icon="upload" label="CARGAR ARCHIVOS" color="primary" style="width:100%;" @click="onSubmit" />
        </div>
      </div>
    </q-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import { api } from 'src/boot/axios'

import * as vals from 'src/lib/validators'

import { useRoute } from 'vue-router'

const $emit = defineEmits(['submit'])

const $route = useRoute()

const files = ref([])

const listVersioning = ref([])

const versioning = ref(null)

const $form = ref(null)

const addFiles = (file) => {
  files.value.push(file)
}

const onSubmit = async () => {
  const success = await $form?.value.validate()

  if (!success) return

  const datos = new FormData()

  datos.append('number_records', 0)
  datos.append('name', 'uno')
  datos.append('versioning', versioning.value.uuid)

  files.value[0].forEach((file) => {
    datos.append('file_route', file)
  })

  try {
    const { data } = await api.post('core/files/', datos, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    $emit('submit', data)
  } catch (error) {}
}

const getVersioning = async () => {
  if ($route.params.uuid !== 'null') {
    const { data } = await api.get(`core/versioning/${$route.params.uuid}/`)
    versioning.value = {
      uuid: data.uuid,
      name: data.name
    }
  }

  const { data } = await api.get('core/versioning/')
  listVersioning.value = data.results
}

onMounted(() => getVersioning())

</script>
