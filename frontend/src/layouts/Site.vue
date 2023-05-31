<template>

  <div>
    <Header></Header>
    <div class="mt-16">
      <slot></slot>
    </div>
  </div>

</template>

<script setup>
import Header from "@/site/components/Header.vue"

</script>
