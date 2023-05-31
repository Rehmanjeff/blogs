<template>
  <div class="bg-white">
    <header class="fixed inset-x-0 top-0 z-50 bg-white">
      <nav class="flex items-center justify-between p-4 shadow-lg lg:px-8" aria-label="Global">
        <div class="flex lg:flex-1">
          <RouterLink :to="{ name: 'Home' }" class="-m-1.5 p-1.5">
            <div class="text-3xl font-extrabold text-indigo-600">
              Bl<span class="text-red-400">og<span class="text-indigo-600">s</span></span>
            </div>
          </RouterLink>
        </div>
        <div v-if="MenuOpen" class="hidden lg:flex lg:gap-x-12">
          <RouterLink v-for="item in navigation" :key="item.name" :to="{ name: item.href }" class="text-sm font-semibold leading-6 text-gray-900">
            {{ item.name }}
          </RouterLink>
        </div>
        <div class="flex lg:hidden">
          <button type="button" class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700" @click="mobileMenuOpen">
            <span class="sr-only">Open main menu</span>
            <Bars3Icon class="w-6 h-6" aria-hidden="true" />
          </button>
        </div>
        <div class="hidden lg:flex lg:gap-x-12">
          <RouterLink v-for="item in navigation" :key="item.name" :to="{ name: item.href }" class="text-sm font-semibold leading-6 text-gray-900">
            {{ item.name }}
          </RouterLink>
        </div>
        <div class="hidden lg:flex lg:flex-1 lg:justify-end">
          <RouterLink :to="{ name: 'Login',}" class="text-sm font-semibold leading-6 text-gray-900">
            Log in &rarr;
          </RouterLink>
        </div>
      </nav>
    </header>
  </div>
</template>
  
<script setup>
import { ref } from "vue"
import { Dialog, DialogPanel } from "@headlessui/vue"
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline"
import { useRoute } from "vue-router"

const navigation = [
  { name: "Browse", href: "Blogs" },
  { name: "About", href: "About" },
  { name: "Contact", href: "Contact" },
]

const MenuOpen = ref(false)

const mobileMenuOpen = () => {
  MenuOpen.value = !MenuOpen.value
}
</script>