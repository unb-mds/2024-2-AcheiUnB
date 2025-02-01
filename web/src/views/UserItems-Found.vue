<template>
  <div
    class="fixed w-full top-0 h-[100px] bg-verde shadow-md rounded-b-xl flex items-center justify-between px-6 text-white z-10"
  >
    <!-- Botão de voltar -->
    <router-link to="/user" class="inline-block">
      <img
        src="../assets/icons/arrow-left-white.svg"
        alt="Voltar"
        class="w-[30px] h-[30px] text-white"
      />
    </router-link>
  <div
    class="fixed w-full top-0 h-[100px] bg-verde shadow-md rounded-b-xl flex items-center justify-between px-6 text-white z-10"
  >
    <!-- Botão de voltar -->
    <router-link to="/user" class="inline-block">
      <img
        src="../assets/icons/arrow-left-white.svg"
        alt="Voltar"
        class="w-[30px] h-[30px] text-white"
      />
    </router-link>

    <!-- Título -->
    <h1 class="text-2xl font-bold text-center flex-1">Meus Itens</h1>
    <!-- Título -->
    <h1 class="text-2xl font-bold text-center flex-1">Meus Itens</h1>

    <!-- Logo (Clicável para ir para /about) -->
    <button>
    <!-- Logo (Clicável para ir para /about) -->
    <button>
      <router-link to="/about" class="no-underline text-white"
        ><Logo class="pr-4" sizeClass="text-2xl"
      /></router-link>
    </button>
  </div>

  <div class="pb-8 pt-24">
    <SubMenu />
  </div>

  <div
    class="grid grid-cols-[repeat(auto-fit,_minmax(180px,_1fr))] sm:grid-cols-[repeat(auto-fit,_minmax(200px,_1fr))] justify-items-center align-items-center lg:px-3 gap-y-3 pb-24"
  >
    <ItemCard
      v-for="item in myItemsFound"
      :key="item.id"
      :id="item.id"
      :name="item.name"
      :location="item.location_name"
      :time="formatTime(item.created_at)"
      :image="item.image_urls[0] || NotAvailableImage"
      :isMyItem="true"
      @delete="confirmDelete"
    />
  </div>

  <ButtonAdd />
  <div class="fixed bottom-0 w-full">
    <MainMenu activeIcon="search" />
  </div>

  <!-- Alertas -->
  <Alert
    v-if="submitError"
    type="error"
    :message="alertMessage"
    @closed="submitError = false"
  />
  <Alert
    v-if="formSubmitted"
    type="success"
    message="Item deletado com sucesso."
    @closed="formSubmitted = false"
  />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchMyItemsFound, deleteItem } from "@/services/item-api";
import { formatTime } from "@/utils/dateUtils";
import MainMenu from "../components/Main-Menu.vue";
import SubMenu from "../components/Sub-Menu-UserFound.vue";
import ItemCard from "@/components/Item-Card.vue";
import Alert from "@/components/Alert.vue";
import Logo from "@/components/Logo.vue";
import NotAvailableImage from "@/assets/images/not-available.png";

const myItemsFound = ref([]);
const submitError = ref(false);
const formSubmitted = ref(false);
const alertMessage = ref("");

// Função para buscar os itens encontrados
const fetchItems = async () => {
  try {
    const response = await fetchMyItemsFound();
    myItemsFound.value = response;
  } catch (error) {
    alertMessage.value = "Erro ao carregar itens encontrados.";
    submitError.value = true;
  }
};

// Função para confirmar exclusão
const confirmDelete = (itemId) => {
  if (confirm("Você tem certeza que deseja deletar este item?")) {
    handleDelete(itemId);
  }
};

// Função para excluir um item
const handleDelete = async (itemId) => {
  try {
    await deleteItem(itemId); // Chama o serviço para deletar o item no backend
    myItemsFound.value = myItemsFound.value.filter(
      (item) => item.id !== itemId
    ); // Atualiza a lista removendo o item excluído
    alertMessage.value = "Item deletado com sucesso.";
    formSubmitted.value = true;
  } catch (error) {
    alertMessage.value = "Erro ao deletar o item.";
    submitError.value = true;
  }
};

// Carrega os itens encontrados ao montar o componente
onMounted(() => fetchItems());
</script>

<style scoped></style>
