<template>
<button
  class="rounded-lg relative w-60 h-12 cursor-pointer flex items-center border border-laranja bg-laranja group hover:bg-laranja active:bg-laranja active:border-laranja"
>
  <span
    class="text-azul font-inter ml-6 transform group-hover:translate-x-0"
    >Adicionar item achado</span
  >
  <span
    class="absolute right-0 h-full w-10 rounded-lg bg-laranja flex items-center justify-center transform group-hover:translate-x-0 group-hover:w-full transition-all duration-300"
  >
    <svg
      class="svg w-8 text-azul"
      fill="none"
      height="24"
      stroke="currentColor"
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      viewBox="0 0 24 24"
      width="24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <line x1="12" x2="12" y1="5" y2="19"></line>
      <line x1="5" x2="19" y1="12" y2="12"></line>
    </svg>
  </span>
</button>
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
