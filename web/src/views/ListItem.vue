<template>
  <!-- Header fixo no topo -->
  <div class="fixed w-full top-0" style="z-index: 1">
    <ItemHeader :title="itemStatus === 'found' ? 'Item Achado' : 'Item Perdido'" />
  </div>

  <!-- Conteúdo principal -->
  <div class="px-6 py-[120px] flex flex-col items-center gap-6" v-if="item">
    <!-- Imagem do Item -->
    <img
      :src="item.image"
      alt="Imagem do Item"
      class="w-full max-w-md h-64 md:h-80 object-cover rounded-lg"
    />

    <!-- Título, local e tags -->
    <div class="text-center">
      <h1 class="text-lg md:text-2xl font-bold">{{ item.name }}</h1>
      <p class="text-sm md:text-base text-gray-500">
        {{ itemStatus === "found" ? "Achado em:" : "Perdido em:" }}
        {{ locationName || "Não especificado" }}
      </p>

      <!-- Labels dinâmicas -->
      <div class="flex flex-wrap gap-2 justify-center mt-2">
        <span
          v-for="(label, index) in labels"
          :key="index"
          :class="
            label.type === 'category'
              ? 'bg-blue-500'
              : label.type === 'brand'
                ? 'bg-laranja'
                : 'bg-gray-500'
          "
          class="px-4 py-2 rounded-full text-sm font-medium text-white"
        >
          {{
            label.type === "category"
              ? "Categoria: "
              : label.type === "brand"
                ? "Marca: "
                : "Cor: "
          }}{{ label.name }}
        </span>
      </div>
    </div>

    <!-- Descrição -->
    <p class="text-sm md:text-base text-gray-700 text-center">
      {{ item.description }}
    </p>

    <!-- Botão para iniciar o chat -->
    <button
      class="w-full md:w-1/3 py-3 text-center text-white font-semibold rounded-lg bg-laranja hover:bg-laranja active:bg-laranja focus:ring-2 focus:ring-laranja"
      @click="startChat"
    >
      {{ itemStatus === "found" ? "É meu item" : "Este item é meu" }}
    </button>
  </div>

  <div v-else class="py-6 text-center">
    <p class="text-gray-600">Carregando informações do item...</p>
  </div>

  <div class="fixed bottom-0 w-full">
    <MainMenu :activeIcon="itemStatus === 'found' ? 'found' : 'lost'" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ItemHeader from "../components/Item-Header.vue";
import MainMenu from "../components/Main-Menu.vue";
import { useRoute, useRouter } from "vue-router";
import { fetchOneItem } from "@/services/item-api";
import { fetchOneLocation } from "@/services/location-api";
import { fetchOneCategory } from "@/services/category-api";
import { fetchOneColor } from "@/services/color-api";
import { fetchOneBrand } from "@/services/brand-api";

const item = ref(null);
const itemStatus = ref("");
const locationName = ref("");
const labels = ref([]);
const route = useRoute();
const router = useRouter();
const idItem = route.query.idItem;
const participant_2 = ref(null);
const currentUser = ref({ id: null });

async function fetchItem() {
  try {
    console.log(`🔍 Buscando detalhes do item ID ${idItem}...`);
    item.value = await fetchOneItem(idItem);

    itemStatus.value = item.value.status === "found" ? "found" : "lost";

    if (itemStatus.value === "found") {
      participant_2.value = item.value.user_id;
    } else {
      participant_2.value = currentUser.value.id;
    }

    if (!participant_2.value) {
      console.error("❌ Erro: Não foi possível obter o participant_2.");
    } else {
      console.log(`✅ participant_2 encontrado: ${participant_2.value}`);
    }

    if (itemStatus.value === "found") {
      participant_2.value = response.data.user_id;
    } else {
      participant_2.value = currentUser.value.id;
    }

    if (!participant_2.value) {
      console.error("❌ Erro: Não foi possível obter o participant_2.");
    } else {
      console.log(`✅ participant_2 encontrado: ${participant_2.value}`);
    }

    if (item.value.location) {
      const locationResponse = await fetchOneLocation(item.value.location);
      locationName.value = locationResponse.name;
    } else {
      locationName.value = "Não especificado";
    }

    labels.value = [];

    if (item.value.category) {
      const categoryIds = Array.isArray(item.value.category)
        ? item.value.category
        : [item.value.category];
      const categoryPromises = categoryIds.map((id) =>
        fetchOneCategory(id).then((res) => ({
          name: res.name,
          type: "category",
        })),
      );
      const categories = await Promise.all(categoryPromises);
      labels.value.push(...categories);
    }

    if (item.value.color) {
      const colorResponse = await fetchOneColor(item.value.color);
      labels.value.push({ name: colorResponse.data.name, type: "color" });
    }

    if (item.value.brand) {
      const brandResponse = await fetchOneBrand(item.value.brand);
      labels.value.push({ name: brandResponse.data.name, type: "brand" });
    }
  } catch (error) {
    console.error("Erro ao carregar item:", error);
  }
}

function viewMatches() {
  alert(
    itemStatus.value === "found" ? "Exibindo possíveis matches!" : "Reportando possível match!",
  );
}

function navigateToChat() {
  if (item.value && item.value.id) {
    router.push(`/chatroom=${item.value.id}`);
  } else {
    console.error("ID do item não encontrado.");
  }
}

onMounted(fetchItem);
async function fetchCurrentUser() {
  try {
    console.log("🔍 Buscando usuário logado...");
    const response = await api.get(`/auth/user/`);
    currentUser.value.id = response.data.id;
    console.log("✅ Usuário logado:", response.data);
  } catch (error) {
    console.error("Erro ao buscar usuário logado:", error);
  }
}

// 🚀 Criar o chatroom automaticamente e redirecionar
async function startChat() {
  try {
    if (!participant_2.value || !currentUser.value.id) {
      console.error("❌ Erro: participant_2 ou currentUser.id não definido.");
      return;
    }

    console.log(
      `🛠 Criando chatroom entre usuário ${currentUser.value.id} e ${participant_2.value}...`,
    );
    const chatResponse = await api.post("/chat/chatrooms/", {
      participant_1: currentUser.value.id,
      participant_2: participant_2.value,
      item_id: idItem,
    });

    console.log("✅ Chatroom criado:", chatResponse.data);

    // 🔀 Redireciona para o chat correto
    router.push(`/chat/${chatResponse.data.id}`);
  } catch (error) {
    console.error("Erro ao criar chatroom:", error);
  }
}

// ⏳ Carrega os dados quando o componente é montado
onMounted(async () => {
  await fetchCurrentUser();
  await fetchItem();
});
</script>

<style scoped></style>
