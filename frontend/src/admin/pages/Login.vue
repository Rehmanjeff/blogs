<!-- Login form component -->
<template>
    <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div class="w-full max-w-md overflow-hidden bg-white rounded-lg shadow-lg">
        <div class="p-8">
          <div class="flex items-center justify-center mb-8">
            <div class="text-3xl font-extrabold text-indigo-600">
              Bl<span class="text-red-400">og<span class="text-indigo-600">s</span></span>
            </div>
          </div>
          <h2 class="mb-4 text-2xl font-bold text-gray-800">Log In</h2>
          <div>
            <input id="email" type="email" v-model="email"  placeholder="Email" class="w-full px-4 py-2 border rounded border-grey-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" required />
          </div>
          <div class="mt-5">
            <input id="password" type="password" v-model="password" placeholder="Password"  class="w-full px-4 py-2 border rounded border-grey-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" required />
          </div>
          <div class="mt-10">
            <button type="button" @click="proceedLogin" class="w-full px-4 py-2 mb-4 text-sm font-semibold text-white transition-colors duration-200 bg-blue-500 border rounded-3xl hover:bg-blue-600">
              Log In
            </button>
            <RouterLink to="">
              <button type="button" class="w-full px-4 py-2 text-sm font-semibold text-blue-500 transition-colors duration-200 bg-white border border-blue-500 rounded-3xl">
                Create an account
              </button>
            </RouterLink>
            <div class="flex ml-2">
              <RouterLink to="">
                <p class="mt-2 text-xs text-blue-500 cursor-pointer hover:underline">
                  Forget password ?
                </p>
              </RouterLink>
            </div>
            <div v-if="error" class="flex ml-2">
              <div class="mt-5 text-sm font-semibold text-theme-red">{{ error }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>


<script setup>
import { ref } from 'vue'
import Auth from '../../composables/Auth';
import { useRouter } from 'vue-router';


const {login} = Auth()
const emit = defineEmits(["response"])
const email = ref('')
const error = ref(false)
const password = ref('')
const route = useRouter()

const proceedLogin = () => {
  if (email.value !== '' && password.value !== '') {
    login(email.value, password.value)
      .then((data) => {
        console.log(data)
          
      })
  }
};
</script>