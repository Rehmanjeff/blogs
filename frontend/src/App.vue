<template>

  <AdminLayout v-if="route.meta.isAdminRoute == true && isLoggedIn">
    <router-view />
  </AdminLayout>

  <AdminLogin @response="checkLogin" v-else-if="route.meta.isAdminRoute == true && !isLoggedIn" />

  <SiteLayout v-else-if="route.meta.isUserRoute == true">
    <router-view />
  </SiteLayout>

  <NotFound v-else />

</template>

<script setup>
import AdminLayout from '@/layouts/Admin.vue'
import NotFound from '@/404.vue'
import SiteLayout from '@/layouts/Site.vue'
import { useRoute } from "vue-router"
import AdminLogin from "@/admin/pages/Login.vue"
import { ref } from 'vue'

const route = useRoute()
const token = ref(localStorage.getItem('blogsAccessToken'))
const isLoggedIn = ref(token.value !== null && token.value != '' ? true : false)

console.log(token.value)
const checkLogin = () => {

isLoggedIn.value = true
}

</script>