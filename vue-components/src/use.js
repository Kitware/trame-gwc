// Import Vue
import Vuetify from 'vuetify/lib'
import * as GirderComponents from '@girder/components'
import RestProvider from './components/RestProvider.vue'
import '@girder/components/dist/girder.css'


// Create a Vue instance if needed for development or export for Trame integration
export default function install(Vue) {
  Object.keys(GirderComponents).forEach((componentName) => {
    Vue.component(componentName, GirderComponents[componentName])
  })
  Vue.component('girder-rest-provider', RestProvider)
}