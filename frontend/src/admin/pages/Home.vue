<template>
    <h1>Admin Home</h1>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Admin from '@/composables/Admin.js'

const { dashboard } = Admin()
const token = localStorage.getItem('blogsAccessToken')

const getAdminDashboard = (token) => {

    dashboard(token).then((response) => {
        
        if(response.status == 200){
            
            console.log(response.data)
        } else {
            
            console.log(response)
        }
    })
}

onMounted(() => {

    getAdminDashboard(token)    
})
</script>