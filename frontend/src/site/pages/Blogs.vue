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
        <div v-for="item in navigation" :key="item.id">
          <div class="flex flex-row items-center gap-4 mb-4">
            <div class="text-sm leading-8 text-gray-600">{{ item.date }}</div>
            <div class="p-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-full">
              {{ item.catagery.name }}
            </div>
          </div>
          <div>
            <div class="mb-6 text-xl font-medium">
              {{ item.title }}
            </div>
            <div class="mb-6 text-sm leading-6 text-gray-600">
              {{ item.body }}
            </div>
            <div class="flex flex-row items-center mb-20">
              <div class="mr-3 bg-gray-200 rounded-full">
                <img :src="item.user.image" alt="" class="rounded-full" />
              </div>
              <div class="flex flex-col pt-10">
                <div class="font-bold">{{ item.user.name }}</div>
                <div class="mb-10 text-sm leading-8 text-gray-600">
                  {{ item.user.post }}
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
import { ref } from "vue"
const navigation = ref([
  {
    id: "1",
    date: "Mar 16,2020",
    catagery: { id: "1", name: "Marketing" },
    title: "Boost your conversion rate",
    body: "lllo sint voluptos. Error voluption culpa eligendi. Hic vel totamvitae illo. Non aliquid explicabo necessitatibus unde. Sed excercitationem placeta consectetur nulla deserunt vel iusto corrupti dicta laboris incididunt",
    user: {
      id: 1,
      name: "Johndoe",
      image: "src/assets/images/default_profile.png",
      post: "Co-Founder / CTO",
    },
  },

  {
    id: "2",
    date: "Mar 16,2020",
    catagery: { id: "1", name: "Sales" },
    title: "How to use search engine optamization to drives saales",
    body: "lllo sint voluptos. Error voluption culpa eligendi. Hic vel totamvitae illo.",
    user: {
      id: 1,
      name: "Linsay Walton",
      image: "src/assets/images/default_profile.png",
      post: "Front-end Developer ",
    },
  },
  {
    id: "3",
    date: "Mar 16,2020",
    catagery: { id: "1", name: "Development" },
    title: "Boost your conversion rate",
    body: "Illo sint voluptas. Error voluptates culpa eligendi. Hic vel totam vitae   illo. Non aliquid explicabo necessitatibus unde. Sed exercitationem  placeat consectetur nulla deserunt vel iusto corrupti dicta laboris  incididunt.",
    user: {
      id: 1,
      name: "James Alon",
      image: "src/assets/images/default_profile.png",
      post: "Manager ",
    },
  },
])
</script>
