<template>

  <div>
    <Header></Header>
    <div class="mt-16">
      <slot></slot>
    </div>
    <FooterVue/>
  </div>

</template>

<script setup>
import Header from "@/site/components/Header.vue"
import FooterVue from "@/site/components/Footer.vue";

</script>
