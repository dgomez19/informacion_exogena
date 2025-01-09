<template>
  <q-menu context-menu ref="$menu" :target="target">
    <q-list>

      <template v-for="item, i of items" :key="i + 1">
        <q-item clickable @click="item.children ? null : (item.click(row) || $menu.hide())" :disable="item.disable?.(row)" v-if="!item.hide?.(row)">
          <q-item-section avatar>
            <q-icon :name="item.icon" />
          </q-item-section>

          <q-item-section>
            <q-item-label>
              {{ item.label }}
            </q-item-label>
          </q-item-section>

          <template v-if="item.children">
            <q-item-section side>
              <q-icon name="keyboard_arrow_right" color="dark" />
            </q-item-section>

            <q-menu anchor="top end" self="top start">
              <q-list>

                <q-item v-for="child, i of item.children" :key="i + 1" clickable @click="child.click(row) || $menu.hide()" :disable="child.disable?.(row)">
                  <q-item-section avatar>
                    <q-icon :name="child.icon" />
                  </q-item-section>

                  <q-item-section>
                    <q-item-label>
                      {{ child.label }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

              </q-list>
            </q-menu>

          </template>
        </q-item>
      </template>

    </q-list>
  </q-menu>
</template>

<script setup>
import { ref, nextTick } from 'vue'

defineProps({
  items: { type: Array, default: null }
})

const $menu = ref(null)

const target = ref(false)
const row = ref(null)

const show = async (event, row_) => {
  target.value = event?.target || false
  row.value = row_

  event?.preventDefault()

  await nextTick()
  $menu.value.show()
}

defineExpose({ show })
</script>
