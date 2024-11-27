<template>
  <div>
    <q-form ref="form">
      <div class="row form-group">
        <div class="col-4 col-md-12">
          <q-uploader
            :hide-upload-btn="true"
            accept=".csv"
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
import { ref } from 'vue'

import { api } from 'src/boot/axios'

const $emit = defineEmits(['submit'])

const files = ref([])

const addFiles = (file) => {
  files.value.push(file)
}

const onSubmit = async () => {
  const datos = new FormData()

  datos.append('number_records', 0)
  datos.append('name', 'uno')

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
</script>
