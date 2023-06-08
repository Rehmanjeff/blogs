<template>
  <div>
    <div class="relative px-6 isolate lg:px-8">
      <div class="absolute inset-x-0 overflow-hidden -top-40 -z-10 transform-gpu blur-3xl sm:-top-80" aria-hidden="true">
        <div class="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]" style="clip-path: polygon(74.1% 44.1%,100% 61.6%,97.5% 26.9%,85.5% 0.1%,80.7% 2%,72.5% 32.5%,60.2% 62.4%,52.4% 68.1%,47.5% 58.3%,45.2% 34.5%,27.5% 76.7%,0.1% 64.9%,17.9% 100%,27.6% 76.8%,76.1% 97.7%,74.1% 44.1%);"/>
      </div>
      <div class="max-w-2xl py-32 mx-auto sm:py-48 lg:py-56">
        <div class="hidden sm:mb-8 sm:flex sm:justify-center">
          <div class="relative px-3 py-1 text-sm leading-6 text-gray-600 rounded-full ring-1 ring-gray-900/10 hover:ring-gray-900/20">
            Announcing our next round of funding.
            <a href="#" class="font-semibold text-indigo-600">
              <span class="absolute inset-0" aria-hidden="true" />
              Read more
              <span aria-hidden="true">&rarr;</span>
              </a>
          </div>
        </div>
        <div class="text-center">
          <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Data to enrich your online business
          </h1>
          <p class="mt-6 text-lg leading-8 text-gray-600">
            Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui lorem
            cupidatat commodo. Elit sunt amet fugiat veniam occaecat fugiat
            aliqua.
          </p>
          <div class="flex items-center justify-center mt-10 gap-x-6">
            <a href="#" class="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
              Get started
            </a>
            <a href="#" class="text-sm font-semibold leading-6 text-gray-900">
              Learn more 
              <span aria-hidden="true">→</span>
            </a>
          </div>
        </div>
      </div>
      
    </div>
    <FeaturedPostVue />
    <Team />
    <Testimonial />
    <div v-if="!accepted" class="fixed bottom-0 left-0 w-full px-4 py-2 text-white bg-gray-800">
      <p class="p-2 text-sm">
        We use cookies to improve your experience on our website. By continuing to browse, you accept our use of cookies.
        <button @click="accept" class="px-2 py-1 ml-4 text-gray-800 bg-white rounded hover:bg-gray-200">Accept</button>
      </p>
    </div>
  </div>
</template>
  
<script setup>
import FeaturedPostVue from "@/site/components/Home/FeaturedPost.vue"
import Team from "@/site/components/Home/Team.vue"
import Testimonial from "@/site/components/Home/Testimonial.vue"
import { ref, onMounted } from 'vue';
import Cookies from 'js-cookie';

const accepted = ref(false);

onMounted(() => {
  if (Cookies.get('cookieAccepted')) {
    accepted.value = true;
  }
});

const accept = () => {
  Cookies.set('cookieAccepted', true, { expires: 365 });
  accepted.value = true;
};
</script>