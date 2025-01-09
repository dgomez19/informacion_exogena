<template>
  <q-dialog persistent ref="$dialog">
    <q-card flat bordered style="width: 100%; max-width: 800px;">
      <q-card-section>
        <div class="row items-center no-wrap">
          <q-icon name="style" size="md" class="q-mr-md" />
          <div class="col">
            <div class="text-h6">{{ editing ? 'Editar cargue' : 'Agregar cargue'}}</div>
          </div>

          <q-space />

          <q-btn round flat v-close-popup icon="close" size="md" color="negative" :disable="loading" />
        </div>
      </q-card-section>

      <q-card-section>
        <q-form ref="$form" class="column q-col-gutter-y-sm" @submit="submit" @reset="reset">
          <q-input outlined dense v-model="versioning.name" label="Nombre *" lazy-rules :rules="[vals.required, vals.minMaxLen(3, 200)]">
            <template #prepend>
              <q-icon name="title" />
            </template>
          </q-input>

          <div class="row no-wrap q-gutter-x-sm">
            <q-btn v-if="editing" unelevated no-caps size="12px" type="submit" icon="save" label="Editar cargue" color="primary" :loading="loading"/>
            <q-btn v-else unelevated no-caps size="12px" type="submit" icon="save" label="Agregar cargue" color="primary" :loading="loading"/>
            <q-btn v-if="editing" outline no-caps size="12px" type="reset" icon="restart_alt" label="Restaurar cambios" color="primary" :disable="loading"/>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { nextTick, reactive, ref } from 'vue'

import { api } from 'src/boot/axios'

import { Notify } from 'quasar'

import * as vals from 'src/lib/validators'

const $emit = defineEmits(['submit', 'close'])

const $dialog = ref(null)
const $form = ref(null)

const fields = {
  uuid: '',
  name: '',
  description: '',
  status: null
}

const initial = ref({ ...fields })

const versioning = reactive({ ...fields })

const loading = ref(false)

const editing = ref(false)

const create = async () => {
  loading.value = true

  try {
    const { data } = await api.post('core/versioning/', { ...versioning })

    $emit('submit', data)

    Notify.create({
      type: 'success',
      message: 'Se ha creado la cargue con éxito.'
    })

    $dialog.value?.hide()
  } catch (err) {}

  loading.value = false
}

const update = async () => {
  loading.value = true

  try {
    const { data } = await api.put(`core/versioning/${versioning.uuid}/`, { ...versioning, status: versioning.status?.code })

    $emit('submit', data)

    Notify.create({
      type: 'success',
      message: 'Se ha actualizado la cargue con éxito.'
    })

    $dialog.value?.hide()
  } catch (err) {}

  loading.value = false
}

const submit = async () => {
  const success = await $form?.value.validate()

  if (!success) return

  if (editing.value) {
    await update()
    return
  }

  await create()
}

const reset = () => Object.assign(versioning, { ...initial.value })

const show = async (row) => {
  editing.value = !!row

  initial.value = { ...fields }

  if (row) Object.assign(initial.value, { ...row })

  Object.assign(versioning, { ...initial.value })

  $dialog.value?.show()

  await nextTick()

  reset()

  $form.value?.resetValidation()
}

defineExpose({ show })
</script>
