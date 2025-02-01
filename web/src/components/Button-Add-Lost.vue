<template>
  <router-link to="/register-lost">
    <button
      class="fixed right-0 bottom-28 rounded-l-lg w-60 h-12 cursor-pointer flex items-center border border-laranja bg-laranja group hover:bg-laranja active:bg-laranja active:border-laranja"
    >
      <span class="text-azul font-inter font-medium ml-6 transform group-hover:translate-x-0"
        >Adicionar item perdido</span
      >
      <span
        class="absolute right-0 h-full w-10 rounded-lg bg-laranja flex items-center justify-center transform group-hover:translate-x-0 group-hover:w-full transition-all duration-300"
      >
        <img src="../assets/icons/add-item.svg" alt="" />
      </span>
    </button>
  </router-link>
</template>

<script>
export default {
  props: {
    customClass: {
      name: "ButtonAdd",
      type: String,
    },
  },
};
</script>

<style scoped></style>
