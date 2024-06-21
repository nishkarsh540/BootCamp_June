// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';

import HomeView from '../views/HomeView.vue';
import SignupUser from '../views/SignupUser.vue';
import LoginUser from '../views/LoginUser.vue';
import AboutView from '../views/AboutView.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import UserDashboard from '../views/UserDashboard.vue';
import StoreDashboard from '../views/StoreDashboard.vue';
import CategoryManagement from '../views/CategoryManagement.vue';
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginUser,
    meta: { requiresGuest: true } // Redirect to home if logged in
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupUser,
    meta: { requiresGuest: true } // Redirect to home if logged in
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/admin-dashboard',
    name: 'admin-dashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, roles: ['admin'] } // Requires authentication and admin role
  },
  {
    path: '/category',
    name: 'category',
    component: CategoryManagement,
    meta: { requiresAuth: true, roles: ['admin'] } // Requires authentication and admin role
  },
  {
    path: '/user-dashboard',
    name: 'user-dashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, roles: ['user'] } // Requires authentication and user role
  },
  {
    path: '/store-dashboard',
    name: 'store-dashboard',
    component: StoreDashboard,
    meta: { requiresAuth: true, roles: ['store_manager'] } // Requires authentication and store manager role
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

// Navigation guard to check authentication and role
router.beforeEach((to, from, next) => {
  // Check if the route requires authentication
  if (to.meta.requiresAuth) {
    // Check if user is authenticated
    if (!store.getters.isAuthenticated) {
      // Redirect to login if not authenticated
      next('/login');
    } else {
      // Check if user has required role
      const userRole = store.getters.userRole;
      if (to.meta.roles && !to.meta.roles.includes(userRole)) {
        // Redirect to home or unauthorized page if role does not match
        next('/');
      } else {
        // Continue to the route
        next();
      }
    }
  } else if (to.meta.requiresGuest && store.getters.isAuthenticated) {
    // Redirect to home if route requires guest (e.g., login, signup) and user is authenticated
    next('/');
  } else {
    // Continue to the route
    next();
  }
});

export default router;
