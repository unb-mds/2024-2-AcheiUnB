<template>
  <h1 :class="[customClass || 'text-light']">
    <span class="italic" :class="sizeClass">Achei</span>
    <span class="font-bold" :class="sizeClass">UnB</span>
  </h1>
</template>

<script>
export default {
  props: {
    customClass: {
      type: String,
    },
    sizeClass: {
      type: String,
      default: "text-5xl",
    },
  },
};
</script>

<style scoped></style>
