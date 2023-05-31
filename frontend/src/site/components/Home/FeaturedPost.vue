<template>
  <div class="flex w-full px-8 xs:flex-col md:flex-row md:gap-8">
    <div v-for="item in navigation" :key="item.id" class="px-8 mb-8 xs:w-full md:w-3/6">
      <div class="">
        <div class="mb-6 text-sm text-gray-400">{{ item.date }}</div>
        <div class="mb-6 font-semibold xs:text-2xl md:text-3xl">
          {{ item.title }}
        </div>
        <div class="mb-6 leading-8 text-gray-600">
          {{ item.body }}
        </div>
        <div class="mb-6 text-sm text-indigo-600">
          <RouterLink :to="{ name: 'Blog', params: {slug: 'we-are-incredible-pround-to-announce-we-have-secured-$75M-in-seriesB',},}">
            <span class="cursor-pointer">
              Continue reading &nbsp; &rarr;
            </span>
          </RouterLink>
        </div>
        <div class="mb-6">
          <hr />
        </div>

        <div class="flex flex-row items-center mb-20">
          <div class="mr-3 bg-gray-200 rounded-full">
            <img :src="item.user.image" alt="" class="rounded-full" />
          </div>

          <div class="font-bold">{{ item.user.name }}</div>
        </div>
      </div>
    </div>
    <div class="px-8 xs:w-full md:w-3/6">
      <div class="mb-6 text-sm text-gray-300">March 10, 2020</div>
      <div class="mb-4 text-lg font-bold">Boost your conversion rate</div>
      <div class="mb-4 leading-8 text-gray-600">
        Illo sint voluptas. Error voluptates culpa eligendi. Hic vel totam vitae
        illo. Non aliquid explicabo necessitatibus unde. Sed exercitationem
        placeat consectetur nulla deserunt vel iusto corrupti dicta laboris
        incididunt.
      </div>
      <div class="flex flex-row items-center mb-20">
        <div class="mr-3 bg-gray-200 rounded-full">
          <img src="src/assets/images/default_profile.png" alt="" class="rounded-full"/>
        </div>

        <div class="font-bold">Lindsay Walton</div>
      </div>
      <div class="mb-8"><hr /></div>
      <div class="mb-4 text-sm text-gray-300">Feb 12, 2020</div>
      <div class="mb-4 text-lg font-bold">
        How to use search engine optimization to drive sales
      </div>
      <div class="mb-4 leading-8 text-gray-600">
        Optio sit exercitation et ex ullamco aliquid explicabo. Dolore do ut
        officia anim non ad eu. Magna laboris incididunt commodo elit ipsum.
      </div>
      <div class="flex flex-row items-center mb-20">
        <div class="mr-3 bg-gray-200 rounded-full">
          <img
            src="src/assets/images/default_profile.png"
            alt=""
            class="rounded-full"
          />
        </div>

        <div class="font-bold">Lindsay Walton</div>
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { useRoute } from "vue-router"

const route = useRoute()
const slug = route.params.slug

const navigation = [
  {
    id: "1",
    date: "Mar 16,2020",
    title:
      "We’re incredibly proud to announce we have secured $75m in Series B",
    body: "Illo sint voluptas. Error voluptates culpa eligendi. Hic vel totam vitae  illo. Non aliquid explicabo necessitatibus unde. Sed exercitationem  placeat consectetur nulla deserunt vel iusto corrupti dicta laboris  incididunt.",

    user: {
      id: 1,
      name: "Michael Foster",
      image: "src/assets/images/default_profile.png",
    },
  },
]
</script>
  
  