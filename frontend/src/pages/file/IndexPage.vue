<template>
  <q-page padding>
    <file-upload @submit="loadTable" /> <br><br>
    <file-table ref="$table" />
  </q-page>
</template>

<script setup>
import { ref } from 'vue'

import FileUpload from 'src/components/file/FileUpload.vue'

import FileTable from 'src/components/file/FileTable.vue'

const $table = ref(null)

const loadTable = () => $table.value.load()

</script>
