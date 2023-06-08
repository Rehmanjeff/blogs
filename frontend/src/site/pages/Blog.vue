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

    <div  class="flex flex-col mt-32 xs:px-10 md:px-24">
      <div class="text-2xl font-bold">From the Blog</div>
      <div class="mb-10 text-sm leading-6 text-gray-600">
        Learn how to grow your business with our expert advice
      </div>
      <hr class="mb-10" />

      <div class="flex gap-12 xs:flex-col md:flex-row">
        <div v-for="item in navigation" :key="item.id" class="flex flex-col md:w-2/6 xs:w-full">
          <div class="flex flex-row items-center gap-4 mb-4">
            <div class="text-sm leading-8 text-gray-600">{{  item ? item.created_at :'' }}</div>
            <div class="p-1 px-6 text-xs text-gray-600 bg-gray-100 rounded-full">
              {{ item ? item.category : '' }}
            </div>
          </div>
          <div class="mb-6 text-lg">
            <a :href="`/blog/${item.slug}`">{{ item ? item.name : '' }}</a>
          </div>
          <div class="mb-6 text-xs leading-6 text-gray-600" v-html="item ? truncateDescription(item.description) : ''">
            
          </div>
          <div class="flex flex-row items-center mt-auto">
            <div class="w-12 h-12 mr-3 bg-gray-200 rounded-full">
              <img :src="'/assets/authors/'+  item.author.avatar " alt="" class="h-12 rounded-full" />
            </div>
            <div class="flex flex-col pt-10">
              <div class="text-sm">{{ item ? item.author.name :'' }}</div>
              <div class="mb-10 text-xs leading-6 text-gray-600">
                {{item ? item.author.designation :'' }}
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
const { getBlogSlug, getBlogCategory } = Blog()
const blogDetails = ref(null)
const category = ref()
const navigation = ref(null)


const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  });
};


function truncateDescription(description) {
  const maxCharacters = 200;
  if (description && description.length > maxCharacters) {
    return description.slice(0, maxCharacters) + '...'
  } else {
    return description
  }
} 

const getBlog = async () => {
  try {
    const response = await getBlogSlug(token, slug);
    blogDetails.value = response.data.blog;
    category.value = response.data.blog.category.name;
  } catch (error) {
    // Handle error
  }
};

const getBlogbyCategory = async () => {
  try {
    const response = await getBlogCategory(token, category.value);
    console.log(response.data);
    navigation.value = response.data
    console.log(response.data[0].author.name)
  } catch (error) {
    // Handle error
  }
};

onMounted(async () => {
  await getBlog();
  await getBlogbyCategory()
});
// const navigation = ref([
//   {
//     id: "1",
//     date: "Mar 16,2020",
//     catagery: { id: "1", name: "Marketing" },
//     title: "Boost your conversion rate",
//     body: "lllo sint voluptos. Error voluption culpa eligendi. Hic vel totamvitae illo. Non aliquid explicabo necessitatibus unde. Sed excercitationem placeta consectetur nulla deserunt vel iusto corrupti dicta laboris incidid...",
//     user: {
//       id: 1,
//       name: "Johndoe",
//       image: "/src/assets/images/default_profile.png",
//       post: "Co-Founder / CTO",
//     },
//   },

//   {
//     id: "2",
//     date: "Apr 26,2020",
//     catagery: { id: "1", name: "Develop" },
//     title: "If you want to achieve the desired ",
//     body: "You can also provide a default slot content by placing content inside the  element in the child component. If the parent component doesn't provide any content for the slot, the default content will be used instead.",
//     user: {
//       id: 1,
//       name: "Linsay Walton",
//       image: "/src/assets/images/default_profile.png",
//       post: "Front-end Developer ",
//     },
//   },
//   {
//     id: "2",
//     date: "Dec 7,2020",
//     catagery: { id: "1", name: "Sales" },
//     title: "How to use search engine",
//     body: "You can also provide a default slot content by placing content inside the  element in the child component. If the parent component doesn't provide any content for the slot, the default content will be used instead.",
//     user: {
//       id: 1,
//       name: "Linsay Walton",
//       image: "/src/assets/images/default_profile.png",
//       post: "Front-end Developer ",
//     },
//   },
// ])
</script>
