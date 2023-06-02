<template>

    <AdminLayout v-if="route.meta.isAdminRoute == true  &&  isLoggedIn">
      <router-view />
    </AdminLayout>

    <SiteLayout v-else-if="route.meta.isUserRoute == true ">
      <router-view />
    </SiteLayout>

    <AdminLogin @response="checkLogin" v-else/>

</template>

<script setup>
import AdminLayout from '@/layouts/Admin.vue'
import BasicLayout from '@/layouts/Basic.vue'
import SiteLayout from '@/layouts/Site.vue'
import { useRoute } from "vue-router"
import AdminLogin from "@/admin/pages/Login.vue"
import { ref } from 'vue'

const route = useRoute()
const token = ref(localStorage.getItem('dynoAuthToken'))
const isLoggedIn = ref(token.value !== null && token.value != '' ? true : false)

const checkLogin = () => {
  
  isLoggedIn.value = true
}

</script>