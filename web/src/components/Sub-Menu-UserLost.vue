<template>
  <div class="flex pt-8 space-x-8 justify-center">
    <router-link to="/user-items-found" class="no-underline font-inter font-bold text-cinza3">
      Achados
    </router-link>
    <div class="flex-col space-y-1">
      <span class="font-inter font-bold text-laranja">Perdidos</span>
      <div class="h-[2px] bg-laranja"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SubMenu",
};
</script>

<style scoped></style>
