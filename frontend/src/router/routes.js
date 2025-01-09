const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/third/IndexPage.vue') },
      { path: 'third', component: () => import('pages/third/IndexPage.vue') },
      { path: ':uuid/upload-file', component: () => import('pages/file/IndexPage.vue') },
      { path: 'versioning', component: () => import('pages/versioning/IndexPage.vue') },
      { path: 'report', component: () => import('pages/report/IndexPage.vue') }
    ]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
