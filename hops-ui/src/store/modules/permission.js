import { constantRoutes } from '@/router'
import { getRouters } from '@/api/login'
import Layout from '@/layout/index'
/**
 * Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */
const _import = require('@/router/_import_' + process.env.NODE_ENV)

function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role))
  } else {
    return true
  }
}

/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 * @param roles
 */
export function filterAsyncRoutes(routes, roles) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(roles, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, roles)
      }
      res.push(tmp)
    }
  })

  return res
}

const state = {
  routes: constantRoutes,
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  GenerateRoutes({ commit }, roles) {
    return new Promise(resolve => {
      getRouters(roles).then(res => {
        const accessedRoutes = filterAsyncRouter(res.datail)
        accessedRoutes.push({ path: '*', redirect: '/404', hidden: true })
        //   let accessedRoutes
        //   if (roles.includes('admin')) {
        //     accessedRoutes = asyncRoutes || []
        //   } else {
        //     accessedRoutes = filterAsyncRoutes(asyncRoutes, roles)
        //   }
        commit('SET_ROUTES', accessedRoutes)
        resolve(accessedRoutes)
      })
    })
  }
}

// 遍历后台传来的路由字符串，转换为组件对象
function filterAsyncRouter(asyncRouterMap) {
  return asyncRouterMap.filter(route => {
    if (route.component) {
      // Layout组件特殊处理
      if (route.component === 'Layout') {
        route.component = Layout
      } else {
        // route.component = loadView(route.component)
        route.component = _import(route.component)
      }
    }
    if (route.hidden === '0') {
      route.hidden = false
    } else {
      route.hidden = true
    }
    if (route.children != null && route.children && route.children.length) {
      route.children = filterAsyncRouter(route.children)
    }
    return true
  })
}
// export const loadView = (view) => { // 路由懒加载
// return () => import(`@/views/${view}`)
// }

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
