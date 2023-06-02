import { createWebHistory, createRouter } from "vue-router";
import AdminHome from "@/admin/pages/Home.vue";
import AdminBlogList from "@/admin/pages/BlogList.vue";
import AdminBlogCreate from "@/admin/pages/BlogCreate.vue";
import AdminBlogUpdate from "@/admin/pages/BlogEdit.vue";
import AdminCategoryList from "@/admin/pages/CategoryList.vue";
import AdminLogin from "@/admin/pages/Login.vue"
import AdminAuthorList from "@/admin/pages/AuthorList.vue";
import Home from "@/site/pages/Home.vue"
import Blogs from "@/site/pages/Blogs.vue"
import About from "@/site/pages/About.vue"
import Contact from "@/site/pages/Contact.vue"
import Login from "@/site/pages/Login.vue"
import Blog from "@/site/pages/Blog.vue"




const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { isUserRoute: true },
  },

  {
    path: "/about",
    name: "About",
    component: About,
    meta: { isUserRoute: true },
  },
  {
    path: "/admin/login",
    name: "AdminLogin",
    component: AdminLogin,
    
  },
  {
    path: "/blog/:slug",
    name: "Blog",
    component: Blog,
    props: true,
    meta: { isUserRoute: true },
  },
  {
    path: "/contact",
    name: "Contact",
    component: Contact,
    meta: { isUserRoute: true },
  },
  {
    path: "/blogs",
    name: "Blogs",
    component: Blogs,
    meta: { isUserRoute: true },
  },
  {
    path: "/admin",
    name: "AdminHome",
    component: AdminHome,
    meta: { isAdminRoute: true },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { isUserRoute: true },
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