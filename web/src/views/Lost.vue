<template>
  <div class="h-screen">
    <div class="sticky top-0">
      <Header />
    </div>
    <div
      class="grid grid-cols-[repeat(auto-fit,_minmax(200px,_1fr))] p-8 gap-y-6"
    >
      <ItemCard />
      <ItemCard />
      <ItemCard />
      <ItemCard />
      <ItemCard />
      <ItemCard />
    </div>
    <ButtonAdd />
    <div class="fixed bottom-0 w-full">
      <MainMenu activeIcon="search" />
    </div>
  </div>
</template>

<script setup>
import MainMenu from "../components/Main-Menu.vue";
import ItemCard from "../components/Item-Card.vue";
import ButtonAdd from "../components/Button-Add.vue";
import Header from "../components/Header.vue";
import SearchBar from "@/components/SearchBar.vue";
</script>

<style scoped></style>
