import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import FishListView from '../views/FishListView.vue'
import FishDetailView from '../views/FishDetailView.vue'
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
      path: '/fish',
      name: 'fish-list',
      component: FishListView
    },
    {
      path: '/fish/:fishId',
      name: 'fish-detail',
      component: FishDetailView
    },
    {
      path: '/alerts',
      name: 'alerts',
      component: AlertsView
    }
  ]
})

export default router