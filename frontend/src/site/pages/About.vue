<template>
  <div class="flex flex-col justify-center text-center">
    <div class="flex flex-row justify-center p-2 bg-red-400" id="message">
      <div class="mt-1 text-white">Page Under Construction !</div>
    </div>
    <div class="justify-center mt-32 text-4xl font-bold text-center">
      Page Under Construction !
    </div>
    <div class="mt-2 font-bold text-indigo-500">
      <RouterLink :to="{ name: 'Home' }">Go to home &rarr;</RouterLink>
    </div>
  </div>
</template>

<script setup>
setTimeout(() => {
  const messageDiv = document.getElementById("message")
  messageDiv.classList.add("hidden")
}, 4000)

setTimeout(() => {
  const messageDiv = document.getElementById("message")
  messageDiv.remove()
}, 4000)
</script>
