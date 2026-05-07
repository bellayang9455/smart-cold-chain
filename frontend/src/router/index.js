import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import BoxListView from '../views/BoxListView.vue'
import BoxDetailView from '../views/BoxDetailView.vue'
import AlertsView from '../views/AlertsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/boxes',
      name: 'box-list',
      component: BoxListView
    },
    {
      path: '/boxes/:boxId',
      name: 'box-detail',
      component: BoxDetailView
    },
    {
      path: '/alerts',
      name: 'alerts',
      component: AlertsView
    }
  ]
})

export default router