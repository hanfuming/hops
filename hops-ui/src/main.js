import Vue from 'vue'
import './assets/icons/iconfont.css'
import VueClipboard from 'vue-clipboard2'
import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import VueCodemirror from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import locale from 'element-ui/lib/locale/lang/en' // lang i18n
import locale from 'element-ui/lib/locale/lang/zh-CN' // lang i18n

import moment from 'moment'

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'
import permission from './directive/permission'

import '@/icons' // icon
import '@/permission' // permission control

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */
if (process.env.NODE_ENV === 'production') {
  const { mockXHR } = require('../mock')
  mockXHR()
}

Vue.use(permission)

// set ElementUI lang to EN
Vue.use(ElementUI, { locale })
Vue.use(VueClipboard)
// Vue.use(VueCodemirror)
Vue.use(VueCodemirror,)
// 如果想要中文版 element-ui，按如下方式声明
// Vue.use(ElementUI)

Vue.prototype.$moment = moment

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
