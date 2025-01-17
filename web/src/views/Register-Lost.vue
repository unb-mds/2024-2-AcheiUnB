<template>
  <div class="fixed w-full top-0" style="z-index: 1">
    <LostHeader />
  </div>

  <div class="px-6 py-[120px]" style="z-index: 2">
    <Form />
  </div>

  <div class="fixed bottom-0 w-full">
    <MainMenu activeIcon="search" />
  </div>
</template>

<script setup>
import Form from "../components/Form.vue";
import LostHeader from "../components/Header-Lost.vue";
import MainMenu from "../components/Main-Menu.vue";
</script>

<style scoped></style>
