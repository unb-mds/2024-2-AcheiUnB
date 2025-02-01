<template>
  <div class="flex pt-8 space-x-8 justify-center">
    <div class="flex-col space-y-1">
      <span class="font-inter font-bold text-laranja">Achados</span>
      <div class="h-[2px] bg-laranja"></div>
    </div>
    <router-link to="/user-items-lost" class="no-underline font-inter font-bold text-cinza3">
      Perdidos
    </router-link>
  </div>
</template>

<script>
export default {
  name: "SubMenu",
};
</script>

<style scoped></style>
