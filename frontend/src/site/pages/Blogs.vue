<template>
  <div class="flex flex-row w-full xs:px-8 md:px-0">
    <div class="md:w-2/7"></div>
    <div class="pt-16 sm:w-full md:w-3/7">
      <div class="flex flex-col items-start">
        <div class="text-3xl font-bold">From The Blog</div>
        <div class="text-sm leading-8 text-gray-600">
          Learn how to grow your business with our expert advice
        </div>
        <hr class="w-full mt-10 mb-10" />
        <div v-for="item in navigation.blogs" :key="item.id">
          <div v-if="item.status == 'live'">
            <div class="flex flex-row items-center gap-4 mb-4">
              <div class="text-sm leading-8 text-gray-600">{{ item.created_at }}</div>
              <div class="p-1 px-6 text-xs text-gray-600 bg-gray-100 rounded-full">
                {{ item.category }}
              </div>
            </div>
            <div>
              <div class="mb-6 text-xl font-medium">
                  <RouterLink :to="{name: 'Blog', params: {slug: item.slug}}" @click="scrollToTop">
                  {{ item.name }}
                </RouterLink>
                </div>
              <!-- truncateDescription is the function which allow to display first 200 letter of the description coming from the endpoint -->
              <div class="mb-6 text-sm leading-6 text-gray-600" v-html="truncateDescription(item.description)"></div>
              <!-- Adjust the img size according to your needs -->
              <div class="flex flex-row items-center mb-20">
                <div class="w-12 h-12 mr-3 bg-gray-200 rounded-full">
                  <img :src="'/assets/authors/' + item.author.avatar" alt="" class="h-12 rounded-full " />
                </div>
                <div class="flex flex-col pt-10">
                  <div>
                    <h3>{{ item.author.name }}</h3>
                    <p class="text-sm leading-7 tracking-tight text-gray-500" v-if="item.author.designation">{{ item.author.designation }}</p>
                  </div>
                  <div class="mb-10 text-sm leading-8 text-gray-600">
            
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div> 
        <div class="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]" aria-hidden="true">
          <div class="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]" style="clip-path: polygon(74.1% 44.1%,100% 61.6%,97.5% 26.9%,85.5% 0.1%,80.7% 2%,72.5% 32.5%,60.2% 62.4%,52.4% 68.1%,47.5% 58.3%,45.2% 34.5%,27.5% 76.7%,0.1% 64.9%,17.9% 100%,27.6% 76.8%,76.1% 97.7%,74.1% 44.1%)"/>
        </div>
    </div>

    <div class="md:w-2/7"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import Blog from "@/composables/Blog"
const token = localStorage.getItem('blogsAccessToken')

const {listBlogs} = Blog()
const navigation = ref([])

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  });
};

const getBlog = ()=>{
  listBlogs(token).then((data)=>{
    navigation.value = data.data
  })
}

function truncateDescription(description) {
  const maxCharacters = 200;
  if (description && description.length > maxCharacters) {
    return description.slice(0, maxCharacters) + '...'
  } else {
    return description
  }
} 

onMounted(()=>{
  getBlog()
})
</script>
