<template>
  <div class="flex flex-col items-center px-6 pt-10 lg:pt-16">
    <!-- Foto do Usuário -->
    <div
      class="w-24 h-24 lg:w-32 lg:h-32 rounded-full flex items-center justify-center border-4 border-laranja overflow-hidden"
    >
      <img
        v-if="user.foto"
        :src="user.foto"
        alt="Foto do Usuário"
        class="w-full h-full object-cover"
      />
      <div
        v-else
        class="w-full h-full bg-cinza2 flex items-center justify-center text-cinza3 text-sm lg:text-lg"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="white"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="#FFFFFF"
          class="w-10 h-10"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"
          />
        </svg>
      </div>
    </div>

    <!-- Nome e Email do Usuário -->
    <h1 class="text-xl lg:text-3xl font-bold text-azul mt-4 lg:mt-6">
      {{
        user.first_name || user.last_name ? user.first_name + " " + user.last_name : user.username
      }}
    </h1>
    <p class="text-sm lg:text-lg text-cinza3">
      {{ user.email || "Email não disponível" }}
    </p>

    <!-- Matrícula (se existir) -->
    <p v-if="user.matricula" class="text-sm lg:text-lg text-cinza3">
      Matrícula: {{ user.matricula }}
    </p>

    <!-- Botões de Ação (Centralizados e Melhor Distribuídos) -->
    <div
      class="pt-[30px] lg:pt-[50px] flex flex-col items-center w-full mt-6 space-y-4 lg:space-y-6"
    >
      <router-link to="/user-items-lost" class="w-full flex justify-center">
        <button
          class="bg-verde text-white w-full md:w-[70%] lg:w-[40%] font-medium py-4 rounded-full hover:scale-110 transition-transform duration-300 text-center text-lg lg:text-xl"
        >
          Meus itens ativos
        </button>
      </router-link>
      <a href="mailto:acheiunb2024@gmail.com" class="w-full flex justify-center">
        <button
          class="bg-verde text-white w-full md:w-[70%] lg:w-[40%] font-medium py-4 rounded-full hover:scale-110 transition-transform duration-300 text-center text-lg lg:text-xl"
        >
          Reportar um problema
        </button>
      </a>
      <router-link to="/" class="w-full flex justify-center">
        <button
          class="bg-verde text-white w-full md:w-[70%] lg:w-[40%] font-medium py-4 rounded-full hover:scale-110 transition-transform duration-300 text-center text-lg lg:text-xl"
        >
          Sair da Conta
        </button>
      </router-link>
    </div>

    <!-- Espaçamento extra para telas grandes -->
    <div class="h-16 lg:h-24"></div>

    <!-- Menu Fixo -->
    <div class="fixed bottom-0 w-full">
      <MainMenu activeIcon="user" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import MainMenu from "../components/Main-Menu.vue";

// Dados do Usuário
const user = ref({
  foto: "",
  first_name: "",
  last_name: "",
  email: "",
  username: "",
  matricula: null,
});

// Função para buscar os dados do usuário logado
async function fetchUserData() {
  try {
    console.log("Buscando dados do usuário logado...");
    const response = await api.get("/auth/user/");
    console.log("Dados do usuário recebidos:", response.data);

    // Atualizar os dados do usuário com base na resposta da API
    user.value = {
      foto: response.data.foto || null,
      first_name: response.data.first_name,
      last_name: response.data.last_name,
      email: response.data.email,
      username: response.data.username,
      matricula: response.data.matricula,
    };
  } catch (error) {
    console.error("Erro ao carregar dados do usuário:", error);
  }
}

// Buscar os dados ao montar o componente
onMounted(fetchUserData);
</script>

<style scoped></style>
