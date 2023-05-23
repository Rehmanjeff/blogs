import { createWebHistory, createRouter } from "vue-router";
import Home from "@/site/pages/Home.vue";
import AdminHome from "@/admin/pages/Home.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { isUserRoute: true },
  },
  {
    path: "/admin",
    name: "AdminHome",
    component: AdminHome,
    meta: { isAdminRoute: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;