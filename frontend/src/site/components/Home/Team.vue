
<template>
  <div class="py-24 bg-white sm:py-32">
    <div class="grid px-6 mx-auto max-w-7xl gap-x-8 gap-y-20 lg:px-8 xl:grid-cols-3">
      <div class="max-w-2xl">
        <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Meet our leadership
        </h2>
        <p class="mt-6 leading-8 text-gray-600">
          A team of visionary authors who lead by example, inspire creativity, and guide our journey towards knowledge and inspiration.
        </p>
      </div>
      <ul role="list" class="grid gap-x-8 gap-y-12 sm:grid-cols-2 sm:gap-y-16 xl:col-span-2">
        <li v-for="person in people" :key="person.name">
          <div class="flex items-center gap-x-6">
            <div class="w-12 h-12">
              <img class="h-12 rounded-full " v-if="person" :src="`/assets/authors/${person.avatar}`" alt="" />
            </div>
            <div>
              <h3 class="text-base tracking-tight text-gray-900">
                {{ person ? person.name : '' }}
              </h3>
              <p class="text-sm leading-7 tracking-tight text-gray-500" v-if="person.designation">{{ person ? person.designation : '' }}</p>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
  
<script setup>
import Author from '@/composables/Author';
import { onMounted, ref } from 'vue';

const { listAuthors } = Author()
const people = ref([])
const token = localStorage.getItem('blogsAccessToken')

const authorList = ()=>{
  listAuthors(token).then((data)=>{
    people.value = data.data.authors
  })
}

onMounted(()=>{
  authorList()
})

</script>