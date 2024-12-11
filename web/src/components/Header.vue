<template>
    <div
    class="h-full bg-verde shadow-md rounded-b-xl flex items-center justify-between text-white gap-x-9 p-4"
    >
      <div class="flex-1">
        <SearchBar />
      </div>
      <div>
        <Logo sizeClass="text-2xl" />
      </div>
    </div>
  </template>

<script>
import SearchBar from './SearchBar.vue';
import Logo from './Logo.vue';

export default {
  name: "Header",
    components: {
        SearchBar,
        Logo,
  },
};
</script>

<style scoped>

</style>