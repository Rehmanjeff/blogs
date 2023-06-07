<template>
  <div>
    <div class="flex flex-row w-full pt-16 mb-16">
      <div class="w-2/8"></div>
      <div class="w-4/8">
        <div class="flex flex-row items-center gap-4 mb-2">
          <div class="text-sm leading-8 text-gray-600">{{ blogDetails ? blogDetails.created_at : '' }}</div>
          <div class="px-6 py-1 text-xs text-gray-600 bg-gray-100 rounded-full">
            {{ blogDetails ? blogDetails.category.name : '' }}
          </div>
        </div>
        <div class="mb-4 text-xl font-medium">
          {{ blogDetails ? blogDetails.name : '' }}
        </div>

        <div class="mb-6 text-sm leading-6 text-gray-600" v-html="blogDetails ? blogDetails.description : ''">
          
        </div>
        
        <div class="flex flex-row items-center">
          <div class="flex items-center justify-center w-12 h-12 mr-3 overflow-hidden bg-gray-200 rounded-full">
            <img v-if="blogDetails" :src="`/assets/authors/${blogDetails.author.avatar}`" alt="" class="h-12 rounded-full" />
          </div>
          <div class="flex flex-col">
            <div>
              <h3>{{ blogDetails ? blogDetails.author.name : '' }}</h3>
              <p class="text-sm leading-7 tracking-tight text-gray-500">{{ blogDetails ? blogDetails.author.designation : '' }}</p>
            </div>
            
          </div>
        </div>
      </div>
      <div class="w-2/8"></div>
    </div>

    <div class="flex flex-col mt-32 xs:px-10 md:px-24">
      <div class="text-2xl font-bold">From the Blog</div>
      <div class="mb-10 text-sm leading-6 text-gray-600">
        Learn how to grow your business with our expert advice
      </div>
      <hr class="mb-10" />

      <div class="flex gap-12 xs:flex-col md:flex-row">
        <div v-for="item in navigation" :key="item.id" class="md:w-2/6 xs:w-full">
          <div class="flex flex-row items-center gap-4 mb-4">
            <div class="text-sm leading-8 text-gray-600">{{ item.date }}</div>
            <div class="p-1 px-6 text-xs text-gray-600 bg-gray-100 rounded-full">
              {{ item.catagery.name }}
            </div>
          </div>
          <div class="mb-6 text-xl">{{ item.title }}</div>
          <div class="mb-6 text-sm leading-6 text-gray-600">
            {{ item.body }}
          </div>
          <div class="flex flex-row items-center">
            <div class="w-12 h-12 mr-3 bg-gray-200 rounded-full">
              <img :src="item.user.image" alt="" class="h-12 rounded-full" />
            </div>
            <div class="flex flex-col pt-10">
              <div>{{ item.user.name }}</div>
              <div class="mb-10 text-sm leading-6 text-gray-600">
                {{ item.user.post }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import Blog from "@/composables/Blog"
import { useRoute } from "vue-router"

const route = useRoute()
const slug = route.params.slug
const token = localStorage.getItem('blogsAccessToken')
const { getBlogSlug } = Blog()
const blogDetails = ref(null)

const getBlog = ()=>{
  getBlogSlug(token, slug).then((data)=>{
    blogDetails.value = data.data.blog
  })
}

onMounted(()=>{
  getBlog()
})

const navigation = ref([
  {
    id: "1",
    date: "Mar 16,2020",
    catagery: { id: "1", name: "Marketing" },
    title: "Boost your conversion rate",
    body: "lllo sint voluptos. Error voluption culpa eligendi. Hic vel totamvitae illo. Non aliquid explicabo necessitatibus unde. Sed excercitationem placeta consectetur nulla deserunt vel iusto corrupti dicta laboris incidid...",
    user: {
      id: 1,
      name: "Johndoe",
      image: "/src/assets/images/default_profile.png",
      post: "Co-Founder / CTO",
    },
  },

  {
    id: "2",
    date: "Apr 26,2020",
    catagery: { id: "1", name: "Develop" },
    title: "If you want to achieve the desired ",
    body: "You can also provide a default slot content by placing content inside the  element in the child component. If the parent component doesn't provide any content for the slot, the default content will be used instead.",
    user: {
      id: 1,
      name: "Linsay Walton",
      image: "/src/assets/images/default_profile.png",
      post: "Front-end Developer ",
    },
  },
  {
    id: "2",
    date: "Dec 7,2020",
    catagery: { id: "1", name: "Sales" },
    title: "How to use search engine",
    body: "You can also provide a default slot content by placing content inside the  element in the child component. If the parent component doesn't provide any content for the slot, the default content will be used instead.",
    user: {
      id: 1,
      name: "Linsay Walton",
      image: "/src/assets/images/default_profile.png",
      post: "Front-end Developer ",
    },
  },
])
</script>
