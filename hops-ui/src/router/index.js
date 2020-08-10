import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',

        component: () => import('@/views/dashboard/index'),
        meta: { title: '首页', icon: 'dashboard' }
      },
      {
        path: 'user/info',
        name: 'userinfo',
        hidden: true,
        component: () => import('@/views/system/user/index'),
        meta: { title: '个人中心' }
      }
    ]
  }
  /**
  {
    path: '/cloudResources',
    component: Layout,
    redirect: '/cloudResources',
    name: '/cloudResources',
    meta: { title: '云资源管理', icon: 'cloud' },
    children: [
      {
        path: 'cloudHost',
        name: 'cloudHost',
        component: () => import('@/views/cloudResources/cloudHost'),
        meta: { title: '云服务器', icon: 'cloud' }
      },
      {
        path: 'cloudDB',
        name: 'cloudDB',
        component: () => import('@/views/system/userList/index'),
        meta: { title: '云数据库', icon: 'database' }
      },
    ]
  }


  {
    path: '/product',
    component: Layout,
    redirect: '/product',
    name: 'product',
    meta: { title: '项目管理', icon: 'product' },
    children: [
      {
        path: 'productList',
        name: 'productList',
        component: () => import('@/views/product/productList'),
        meta: { title: '项目列表', icon: 'productlist' }
      },
      {
        path: 'productAdd',
        name: 'productAdd',
        component: () => import('@/views/product/productAdd'),
        meta: { title: '申请项目', icon: 'newadd' }
      }
    ]
  }
   */
  /**
  {
    path: '/taskManager',
    component: Layout,
    redirect: '/taskManager',
    name: '/taskManager',
    meta: {
      roles: ['admin'],
      title: '作业管理',
      icon: 'task'
    },
    children: [
      {
        path: 'fastExecuteScript',
        name: 'fastExecuteScript',
        component: () => import('@/views/taskManager/fastExecuteScript'),
        meta: { title: '快速脚本执行', icon: 'script' }
      },
      {
        path: 'fastPushFile',
        name: 'fastPushFile',
        component: () => import('@/views/taskManager/fastPushFile'),
        meta: { title: '快速文件分发', icon: 'pushfile' }
      },
      {
        path: 'jobList',
        name: 'jobList',
        component: () => import('@/views/taskManager/jobList'),
        meta: { title: '常用作业执行', icon: 'job' }
      },
      {
        path: 'newTask',
        name: 'newTask',
        component: () => import('@/views/taskManager/newTask'),
        meta: { title: '新建作业', icon: 'newadd' }
      },
      {
        path: 'crontabTaskList',
        name: 'crontabTaskList',
        hidden: true,
        component: () => import('@/views/taskManager/crontabTaskList'),
        meta: { title: '定时作业', icon: 'tree' }
      },
      {
        path: 'scriptList',
        name: 'scriptList',
        component: () => import('@/views/taskManager/scriptList'),
        meta: { title: '脚本管理', icon: 'scriptlist' }
      },
      {
        path: 'taskInstanceList',
        name: 'taskInstanceList',
        component: () => import('@/views/taskManager/taskInstanceList'),
        meta: { title: '执行历史', icon: 'history' }
      },
      {
        path: 'jobdetails/jobdetail',
        name: 'jobdetails',
        hidden: true,
        component: () => import('@/views/taskManager/jobdetails/jobdetail'),
        meta: { title: '作业详情' }
      },
      {
        path: 'jobdetails/jobstart',
        name: 'jobdetails',
        hidden: true,
        component: () => import('@/views/taskManager/jobdetails/jobstart'),
        meta: { title: '执行详情' }
      }
    ]
  }*/
]

export const asyncRoutes = [
  // {
  //   path: '/userManage',
  //   component: Layout,
  //   redirect: '/userManage',
  //   name: 'userManage',
  //   meta: { title: '用户管理', icon: 'usermanage' },
  //   children: [
  //     {
  //       path: 'userList',
  //       name: 'userList',
  //       component: () => import('@/views/userManage/userList'),
  //       meta: { title: '用户管理', icon: 'user' }
  //     },
  //     {
  //       path: 'role',
  //       name: 'role',
  //       component: () => import('@/views/userManage/role'),
  //       meta: { title: '角色管理', icon: 'role' }
  //     }
  //   ]
  // },

  // 404 page must be placed at the end !!!
  // { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

// export default router
export default new Router({
  mode: 'history', // 去掉url中的#
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})
