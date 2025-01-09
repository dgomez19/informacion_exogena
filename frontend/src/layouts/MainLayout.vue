<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          CONTACTABILIDAD
        </q-toolbar-title>

        <div>ALCALDÍA DE MEDELLIN</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Menú principal
        </q-item-label>

        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

defineOptions({
  name: 'MainLayout'
})

const linksList = [
  {
    title: 'CREAR CARGUE',
    caption: 'Crear cargue',
    icon: 'people',
    link: '/#/versioning'
  },
  {
    title: 'CARGAR ARCHIVOS',
    caption: 'Cargue de archivos para ser procesados',
    icon: 'upload',
    link: `/#/${null}/upload-file`
  },
  {
    title: 'LISTAR TERCEROS',
    caption: 'Listado de terceros',
    icon: 'people',
    link: '/#/third'
  },
  {
    title: 'REPORTES',
    caption: 'Reportes generados',
    icon: 'library_books',
    link: '/#/report'
  }
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
