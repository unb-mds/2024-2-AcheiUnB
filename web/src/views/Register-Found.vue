<template>
  <div class="fixed w-full top-0" style="z-index: 10000">
    <FoundHeader />
  </div>

  <div class="px-6 py-[120px]" style="z-index: 2">
    <Form />
  </div>

  <div class="fixed bottom-0 w-full">
    <MainMenu activeIcon="search" />
  </div>
</template>

<script setup>
import Form from "../components/Form-Found.vue";
import FoundHeader from "../components/Header-Found.vue";
import MainMenu from "../components/Main-Menu.vue";
</script>

<style scoped></style>
