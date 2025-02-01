<template>
  <div class="h-[100px] bg-verde shadow-md rounded-b-xl flex items-center text-white p-4 md:p-6">
    <!-- Botão de Voltar -->
    <div class="flex items-center w-1/4">
      <img
        @click="goBack"
        src="../assets/icons/arrow-left-white.svg"
        alt="Voltar"
        class="w-[30px] h-[30px] text-white cursor-pointer"
      />
    </div>

    <!-- Título Centralizado -->
    <div class="flex-grow flex justify-center">
      <span class="font-inter font-semibold text-lg md:text-2xl text-center break-words">
        {{ title }}
      </span>
    </div>

    <!-- Logo à Direita -->
    <div class="flex items-center w-1/4 justify-end">
      <router-link to="/about" class="no-underline text-white">
        <Logo class="pr-2 md:pr-4" sizeClass="text-xl md:text-2xl" />
      </router-link>
    </div>
  </div>
</template>

<script>
import Logo from "./Logo.vue";

export default {
  name: "ItemHeader",
  components: {
    Logo,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
  },
  methods: {
    goBack() {
      this.$router.back(); // Retorna para a página anterior
    },
  },
};
</script>

<style scoped></style>
