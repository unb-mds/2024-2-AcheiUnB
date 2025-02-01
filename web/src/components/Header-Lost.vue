<template>
  <div
    class="h-[100px] bg-verde shadow-md rounded-b-xl flex items-center justify-start text-white gap-x-9 p-6"
  >
    <router-link to="/lost" class="inline-block">
      <img
        src="../assets/icons/arrow-left-white.svg"
        alt="Voltar"
        class="w-[30px] h-[30px] text-white"
      />
    </router-link>
    <div>
      <span class="font-inter font-semibold text-2xl">{{
        text ?? "Cadastro de item perdido"
      }}</span>
    </div>
    <button class="ml-auto">
      <router-link to="/about" class="no-underline text-white">
        <Logo class="pr-4" sizeClass="text-2xl" />
      </router-link>
    </button>
  </div>
</template>

<script>
import Logo from "./Logo.vue";

export default {
  name: "LostHeader",
  components: {
    Logo,
  },
  props: {
    text: String,
  },
};
</script>

<style scoped></style>
