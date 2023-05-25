import { createWebHistory, createRouter } from "vue-router";
import Home from "@/site/pages/Home.vue";
import AdminHome from "@/admin/pages/Home.vue";
import AdminBlogList from "@/admin/pages/BlogList.vue";
import AdminBlogCreate from "@/admin/pages/BlogCreate.vue";
import AdminBlogUpdate from "@/admin/pages/BlogEdit.vue";
import AdminCategoryList from "@/admin/pages/CategoryList.vue";
import AdminAuthorList from "@/admin/pages/AuthorList.vue";

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
  {
    path: "/admin/blogs/list",
    name: "AdminBlogList",
    component: AdminBlogList,
    meta: { isAdminRoute: true },
  },
  {
    path: "/admin/blogs/create",
    name: "AdminBlogCreate",
    component: AdminBlogCreate,
    meta: { isAdminRoute: true },
  },
  {
    path: "/admin/blogs/edit/:id",
    name: "AdminBlogUpdate",
    component: AdminBlogUpdate,
    meta: { isAdminRoute: true },
  },
  {
    path: "/admin/categories/list",
    name: "AdminCategoryList",
    component: AdminCategoryList,
    meta: { isAdminRoute: true },
  },
  {
    path: "/admin/authors/list",
    name: "AdminAuthorList",
    component: AdminAuthorList,
    meta: { isAdminRoute: true },
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;