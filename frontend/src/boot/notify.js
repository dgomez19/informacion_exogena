import { Notify } from 'quasar'
import { boot } from 'quasar/wrappers'

export default boot(({ app }) => {
  Notify.registerType('success', {
    color: 'primary',
    icon: 'check_circle',
    position: 'bottom-right'
  })

  Notify.registerType('warning', {
    color: 'warning',
    icon: 'warning',
    position: 'bottom-right'
  })

  Notify.registerType('error', {
    color: 'negative',
    icon: 'error',
    position: 'bottom-right'
  })
})
