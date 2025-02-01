<template>
  <div
    class="h-[100px] bg-verde shadow-md rounded-b-xl flex items-center justify-center text-white p-6"
  >
    <div>
      <span class="font-inter font-semibold text-2xl">
        {{ text ? text : "Sobre o projeto" }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "AboutHeader",
  props: {
    text: String,
  },
};
</script>

<style scoped></style>
