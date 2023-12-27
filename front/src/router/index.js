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
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
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
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '测试管理平台', icon: 'guanlixitong' }
    }]
  },
  {
    path: '/project',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Projects',
        component: () => import('@/views/project/index'),
        meta: { title: '项目管理', icon: 'project' }
      }
    ]
  },
  {
    path: '/apis',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Apis',
        component: () => import('@/views/apis/index'),
        meta: { title: '接口管理', icon: 'api' }
      }
    ]
  },
  {
    path: '/case',
    component: Layout,
    redirect: '/case/manage',
    name: 'Case',
    meta: { title: '用例管理', icon: 'case' },
    children: [
      {
        path: 'demand',
        name: 'Demand',
        component: () => import('@/views/cases/demand/index'),
        meta: { title: '测试需求', icon: 'demand' }
      },
      {
        path: 'manage',
        name: 'Mange',
        component: () => import('@/views/cases/manage/index'),
        meta: { title: '测试用例', icon: 'testcase' }
      },
      {
        path: 'suite',
        name: 'Suite',
        component: () => import('@/views/cases/suite/index'),
        meta: { title: '测试用例集', icon: 'suite' }
      }
    ]
  },
  {
    path: '/infos',
    component: Layout,
    redirect: '/infos/har',
    name: 'Info',
    meta: { title: '接口信息', icon: 'information' },
    children: [
      {
        path: 'har',
        name: 'Har',
        component: () => import('@/views/infos/har/index'),
        meta: { title: 'Har接口信息', icon: 'har' }
      },
      {
        path: 'swagger',
        name: 'Swagger',
        component: () => import('@/views/infos/swagger/index'),
        meta: { title: 'Swagger接口信息', icon: 'swagger' }
      },
      {
        path: 'yapi',
        name: 'Yapi',
        component: () => import('@/views/infos/yapi/index'),
        meta: { title: 'Yapi接口信息', icon: 'yapi' }
      }
    ]
  },
  {
    path: '/test',
    component: Layout,
    redirect: '/test/data',
    name: 'Tests',
    meta: { title: '测试数据', icon: 'data' },
    children: [
      {
        path: 'data',
        name: 'Data',
        component: () => import('@/views/tests/data/index'),
        meta: { title: '基础测试数据', icon: 'database' }
      },
      {
        path: 'search',
        name: 'Search',
        component: () => import('@/views/tests/search/index'),
        meta: { title: '查询条件数据', icon: 'search' }
      }
    ]
  },
  {
    path: '/httprunner',
    component: Layout,
    redirect: '/httprunner/project',
    name: 'Httprunner',
    meta: { title: 'HttpRunner', icon: 'run' },
    children: [
      {
        path: 'project',
        name: 'Project',
        component: () => import('@/views/httprunner/project/index'),
        meta: { title: '项目管理', icon: 'xinicon' }
      },
      {
        path: 'api',
        name: 'Api',
        component: () => import('@/views/httprunner/apis/index'),
        meta: { title: 'API管理', icon: 'apis' }
      },
      {
        path: 'cases',
        name: 'Cases',
        component: () => import('@/views/httprunner/cases/index'),
        meta: { title: '用例管理', icon: 'cases' }
      },
      {
        path: 'suites',
        name: 'Suites',
        component: () => import('@/views/httprunner/suite/index'),
        meta: { title: '用例集管理', icon: 'test-suite' }
      }
    ]
  },
  {
    path: '/envs',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Envs',
        component: () => import('@/views/envs/index'),
        meta: { title: '环境管理', icon: 'envs' }
      }
    ]
  },
  {
    path: '/chat',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Chat',
        component: () => import('@/views/chat/index'),
        meta: { title: 'AI小助手', icon: 'chat' }
      }
    ]
  },
  // {
  //   path: '/example',
  //   component: Layout,
  //   redirect: '/example/table',
  //   name: 'Example',
  //   meta: { title: 'Example', icon: 'el-icon-s-help' },
  //   children: [
  //     {
  //       path: 'table',
  //       name: 'Table',
  //       component: () => import('@/views/table/index'),
  //       meta: { title: 'Table', icon: 'table' }
  //     },
  //     {
  //       path: 'tree',
  //       name: 'Tree',
  //       component: () => import('@/views/tree/index'),
  //       meta: { title: 'Tree', icon: 'tree' }
  //     }
  //   ]
  // },

  // {
  //   path: '/form',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'index',
  //       name: 'Form',
  //       component: () => import('@/views/form/index'),
  //       meta: { title: 'Form', icon: 'form' }
  //     }
  //   ]
  // },

  // {
  //   path: '/nested',
  //   component: Layout,
  //   redirect: '/nested/menu1',
  //   name: 'Nested',
  //   meta: {
  //     title: 'Nested',
  //     icon: 'nested'
  //   },
  //   children: [
  //     {
  //       path: 'menu1',
  //       component: () => import('@/views/nested/menu1/index'), // Parent router-view
  //       name: 'Menu1',
  //       meta: { title: 'Menu1' },
  //       children: [
  //         {
  //           path: 'menu1-1',
  //           component: () => import('@/views/nested/menu1/menu1-1'),
  //           name: 'Menu1-1',
  //           meta: { title: 'Menu1-1' }
  //         },
  //         {
  //           path: 'menu1-2',
  //           component: () => import('@/views/nested/menu1/menu1-2'),
  //           name: 'Menu1-2',
  //           meta: { title: 'Menu1-2' },
  //           children: [
  //             {
  //               path: 'menu1-2-1',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-1'),
  //               name: 'Menu1-2-1',
  //               meta: { title: 'Menu1-2-1' }
  //             },
  //             {
  //               path: 'menu1-2-2',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-2'),
  //               name: 'Menu1-2-2',
  //               meta: { title: 'Menu1-2-2' }
  //             }
  //           ]
  //         },
  //         {
  //           path: 'menu1-3',
  //           component: () => import('@/views/nested/menu1/menu1-3'),
  //           name: 'Menu1-3',
  //           meta: { title: 'Menu1-3' }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'menu2',
  //       component: () => import('@/views/nested/menu2/index'),
  //       name: 'Menu2',
  //       meta: { title: 'menu2' }
  //     }
  //   ]
  // },

  // {
  //   path: 'external-link',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
  //       meta: { title: 'External Link', icon: 'link' }
  //     }
  //   ]
  // },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
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

export default router
