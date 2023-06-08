<template>
  <div class="z-50 flex w-full px-8 xs:flex-col md:flex-row md:gap-8">
    <div class="px-8 mb-8 xs:w-full md:w-3/6">
      <div v-if="navigation" class="">
        <div class="mb-6 text-sm text-gray-400">{{ navigation ? navigation.created_at : '' }}</div>
        <div class="mb-6 font-semibold xs:text-2xl md:text-3xl">
          <RouterLink :to="{ name: 'Blog', params: { slug: navigation.slug }}" @click="scrollToTop">
            {{ navigation ? navigation.name : '' }}
          </RouterLink>
        </div>
            <div class="mb-6 leading-8 text-gray-600" v-html="navigation ? navigation.description : ''"></div>
        <div class="mb-6">
          <hr />
        </div>
        <div class="flex flex-row items-center mb-20">
          <div class="w-12 h-12 mr-3 bg-gray-200 rounded-full">
            <img v-if="navigation" :src="`/assets/authors/${navigation.author.avatar}`" alt="" class="h-12 rounded-full" />
          </div>
          <div>
            <h3>{{ navigation ? navigation.author.name : '' }}</h3>
            <p class="text-sm tracking-tight text-gray-500">{{ navigation ? navigation.author.designation : '' }}</p>
          </div>
        </div>
      </div>
      <div v-else>Loading ...</div>
    </div>
    <div class="flex flex-col px-8 xs:w-full md:w-3/6">
      <div v-for="item in rightBlogs" :key="item.id">
        <div class="mb-6 text-sm text-gray-300">{{ item ? item.created_at : '' }}</div>
        <RouterLink :to="{name:'Blog',params:{slug:item.slug}}" @click="scrollToTop">
          <div class="mb-4 text-lg font-bold">{{ item ? item.name : '' }}</div>
        </RouterLink>
          <div class="mb-4 leading-8 text-gray-600" v-html="item ? item.description : ''"></div>
        <div class="flex flex-row items-center mb-10">
          <div class="w-12 h-12 mr-3 bg-gray-200 rounded-full">
            <img v-if="item" :src="`/assets/authors/${item.author.avatar}`" alt="" class="h-12 rounded-full" />
          </div>
          <div>
            <h3>{{ item ? item.author.name : '' }}</h3>
            <p class="text-sm leading-7 tracking-tight text-gray-500">{{ item ? item.author.designation : '' }}</p>
          </div>
        </div>
        <div class="mb-8">
          <hr />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Blog from "@/composables/Blog"
import { onMounted, ref } from "vue"

const { getBlogHome } = Blog()
const token = localStorage.getItem('blogsAccessToken')


const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  });
};

const homeBlog = () => {
  getBlogHome(token).then((data) => {
    navigation.value = data.data[0]
    rightBlogs.value = data.data.slice(1, 3)
  })
}

const navigation = ref()
const rightBlogs = ref([])

onMounted(() => {
  homeBlog()
})
</script>