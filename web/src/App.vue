<script setup>
import { RouterLink, RouterView } from "vue-router";
import InstallPrompt from "./components/InstallPrompt.vue";
</script>

<template>
  <router-view />
  <InstallPrompt />
</template>

<style scoped></style>
