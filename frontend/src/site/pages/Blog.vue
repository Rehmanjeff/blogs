<template>
  <div>
    <div class="flex flex-row w-full pt-16 mb-16">
      <div class="w-2/8"></div>
      <div v-for="blog in blogDetails" :key="blog.id" class="w-4/8">
        <div class="flex flex-row gap-4 mb-2">
          <div class="text-sm leading-8 text-gray-600">{{ blog.data }}</div>
          <div class="p-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-full">
            {{ blog.catagery.name }}
          </div>
        </div>
        <div class="mb-4 text-xl font-medium">
          {{ blog.title }}
        </div>

        <div class="mb-6 text-sm leading-6 text-gray-600">
          {{ blog.body.paraOne }}
        </div>
        <div class="mb-10 text-sm leading-6 text-gray-600">
          {{ blog.body.paraTwo }}
        </div>
        <div class="flex flex-row items-center">
          <div class="mr-3 bg-gray-200 rounded-full">
            <img :src="blog.user.image" alt="" class="rounded-full" />
          </div>
          <div class="flex flex-col pt-10">
            <div>{{ blog.user.name }}</div>
            <div class="mb-10 text-sm leading-6 text-gray-600">
              {{ blog.user.post }}
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
            <div class="p-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-full">
              {{ item.catagery.name }}
            </div>
          </div>
          <div class="mb-6 text-xl">{{ item.title }}</div>
          <div class="mb-6 text-sm leading-6 text-gray-600">
            {{ item.body }}
          </div>
          <div class="flex flex-row items-center">
            <div class="mr-3 bg-gray-200 rounded-full">
              <img :src="item.user.image" alt="" class="rounded-full" />
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
import { ref } from "vue"

const blogDetails = ref([
  {
    id: "1",
    data: "Sep 16, 2021",
    catagery: { id: "1", name: "Marketing" },
    title:
      " We’re incredibly proud to announce we have secured $75m in Series B",
    body: {
      paraOne:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed consectetur viverra purus, ut interdum velit ultrices sed. Nulla sit amet tristique ipsum. Quisque rutrum sollicitudin purus, sed aliquam sapien fringilla in. Phasellus et sem non felis faucibus hendrerit. Vivamus at sem sit amet elit auctor eleifend a id justo. Fusce quis felis ut odio condimentum eleifend. Proin at condimentum mauris, at auctor mauris. Mauris hendrerit metus a leo pulvinar rutrum. Nullam dignissim purus in malesuada auctor. Fusce ac metus nec leo commodo consectetur.",
      paraTwo:
        " Suspendisse potenti. Vestibulum pharetra dignissim faucibus. Maecenas  gravida arcu quis urna bibendum, ac pellentesque metus vulputate. Sed hendrerit lectus non libero tristique semper.",
    },
    user: {
      id: 1,
      name: "Johndoe",
      image: "/src/assets/images/default_profile.png",
      post: "Co-Founder / CTO",
    },
  },
])

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
