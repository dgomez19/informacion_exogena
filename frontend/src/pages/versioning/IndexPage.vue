<template>
  <q-page padding>
    <versioning-table
      @create="showForm"
      @update="showForm"
      @delete="delete_"
      ref="$table"
    />
  </q-page>

  <versioning-form ref="$form" @submit="loadTable" />
</template>

<script setup>
import VersioningTable from 'src/components/versioning/VersioningTable.vue'

import VersioningForm from 'src/components/versioning/VersioningForm.vue'

import { ref } from 'vue'

import { Dialog, Notify } from 'quasar'

import { api } from 'src/boot/axios'

const $form = ref(null)

const $table = ref(null)

const showForm = (row = null) => $form.value?.show(row)

const loadTable = () => $table.value.load()

const delete_ = async (row) => {
  const callback = async () => {
    try {
      await api.delete(`core/versioning/${row.uuid}/`, { useSpinner: true })

      Notify.create({
        type: 'success',
        message: 'Se ha eliminado el registro con éxito.'
      })

      console.log('xd')

      $table.value.load()

      console.log('01')
    } catch (err) {
      console.log('02', err)
    }
  }

  Dialog.create({
    title: '¿Está segura/ro que desea eliminar este registro?',
    message: 'Toda la información de este registro se borrará del sistema.',
    componentProps: { flat: true, bordered: true },
    ok: { unelevated: true, noCaps: true, color: 'primary', label: 'Sí, eliminar el registro' },
    cancel: { outline: true, noCaps: true, color: 'primary', label: 'Cancelar' }
  }).onOk(() => { callback() })
}
</script>
