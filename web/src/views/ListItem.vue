<template>
  <div class="fixed w-full top-0 z-[20]" v-if="isLoaded && item">
    <ItemHeader
      :title="itemStatus === 'found' ? 'Item Achado' : 'Item Perdido'"
      :userId="currentUser.id"
      :itemUserId="item.user_id"
      :itemId="item.id"
    />
  </div>

  <div
    class="px-6 py-[120px] min-h-screen flex flex-col justify-center items-center gap-6 mt-3"
    v-if="isLoaded && item"
  >
    <div class="w-full md:grid md:grid-cols-2 md:gap-8 md:max-w-4xl lg:max-w-6xl xl:max-w-7xl lg:grid-cols-2">
      <div class="w-full max-w-md md:max-w-full md:col-span-1 relative flex flex-col">
        <button
          v-if="currentUser?.id !== item.user_id"
          @click="openReportModal"
          class="absolute -top-6 right-0 z-[10] flex items-center gap-2 text-red-600 font-semibold text-base md:text-lg hover:underline hover:text-red-700 bg-white/95 px-3 py-1 rounded-full shadow-lg border border-red-200 transition-colors duration-200"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="w-6 h-6">
            <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6A8.38 8.38 0 0112.5 3a8.5 8.5 0 018.5 8.5z"/>
            <circle cx="12" cy="15.5" r="1" fill="currentColor"/>
            <path d="M12 8.5v2.5a1 1 0 001 1h0a1 1 0 001-1v-1a1 1 0 00-1-1h-1"/>
            <line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" stroke-width="1.5"/>
            <circle cx="12" cy="16" r="0.5" fill="currentColor"/>
          </svg>
          Denunciar item
        </button>

        <div v-if="!item.image_urls || item.image_urls.length === 0" class="w-full h-64">
          <img
            :src="notAvailableImage"
            alt="Imagem não disponível"
            class="w-full h-full object-contain"
          />
        </div>

        <div
          v-else
          class="hidden md:grid"
          :class="item.image_urls.length === 1 ? 'grid-cols-1' : 'grid-cols-2 gap-4'"
        >
          <img
            v-for="(url, index) in item.image_urls.slice(0, 2)"
            :key="index"
            :src="url"
            :alt="`Imagem ${index + 1} do item`"
            class="h-64 md:h-80 lg:h-96 w-full object-cover rounded-lg"
          />
        </div>

        <div
          v-if="item.image_urls && item.image_urls.length > 0"
          class="md:hidden overflow-hidden relative"
        >
          <div
            class="flex transition-transform duration-300 ease-out snap-x snap-mandatory"
            :style="{ transform: `translateX(-${activeIndex * 100}%)` }"
          >
            <div
              v-for="(url, index) in item.image_urls"
              :key="index"
              class="w-full flex-shrink-0 relative snap-start"
            >
              <img
                :src="url"
                :alt="`Imagem ${index + 1} do item`"
                class="w-full h-64 object-cover rounded-lg"
              />
            </div>
          </div>

          <div
            v-if="item.image_urls.length > 1"
            class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2"
          >
            <div
              v-for="(_, index) in item.image_urls"
              :key="index"
              class="w-2 h-2 rounded-full transition-colors duration-300"
              :class="activeIndex === index ? 'bg-white' : 'bg-gray-300'"
            />
          </div>

          <button
            v-if="item.image_urls.length > 1"
            @click="prevImage"
            class="absolute left-2 top-1/2 transform -translate-y-1/2 bg-white/30 rounded-full p-2 backdrop-blur-sm"
          >
            ←
          </button>
          <button
            v-if="item.image_urls.length > 1"
            @click="nextImage"
            class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-white/30 rounded-full p-2 backdrop-blur-sm"
          >
            →
          </button>
        </div>
        
        <div 
          v-if="userInfo" 
          class="hidden md:block mt-4"
        >
          <div 
            class="flex items-center p-4 border border-gray-200 rounded-lg bg-gray-50 hover:bg-gray-100 cursor-pointer" 
            @click="viewUserProfile(item.user_id)"
          >
            <div class="flex items-center">
              <img 
                :src="userInfo.foto || notAvailableImage" 
                alt="Foto do usuário" 
                class="w-12 h-12 rounded-full object-cover border-2 border-laranja"
              />
              <div class="ml-4">
                <h3 class="text-sm font-semibold text-azul">Postado por:</h3>
                <p class="text-gray-800 font-medium">{{ 
                  userInfo.first_name && userInfo.last_name ? 
                    `${userInfo.first_name} ${userInfo.last_name}` : 
                  userInfo.first_name ? userInfo.first_name : 
                  userInfo.last_name ? userInfo.last_name : 
                  userInfo.username 
                }}</p>
              </div>
            </div>
            <div class="ml-auto">
              <span class="text-azul text-sm font-medium">Ver perfil</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block ml-1 text-azul" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="w-full md:col-span-1 mt-6 md:mt-0">
        <h1 class="text-lg md:text-2xl font-bold break-words">{{ item.name }}</h1>

        <p class="text-sm md:text-base text-gray-500 text-left mt-2">
          Achado em: {{ item.location_name || "Não especificado" }}
        </p>

        <p
          v-if="item.found_lost_date && itemStatus === 'found'"
          class="text-sm md:text-base text-gray-500 text-left mt-1"
        >
          Data do achado: {{ formatDateTime(item.found_lost_date) }}
        </p>
        <p
          v-else-if="item.found_lost_date && itemStatus === 'lost'"
          class="text-sm md:text-base text-gray-500 text-left mt-1"
        >
          Data da perda: {{ formatDateTime(item.found_lost_date) }}
        </p>

        <div class="flex flex-wrap gap-2 justify-start mt-4">
          <span
            v-if="item.category_name"
            class="px-4 py-2 rounded-full text-sm font-medium text-white bg-blue-500"
          >
            Categoria: {{ item.category_name }}
          </span>
          <span
            v-if="item.brand_name"
            class="px-4 py-2 rounded-full text-sm font-medium text-white bg-laranja"
          >
            Marca: {{ item.brand_name }}
          </span>
          <span
            v-if="item.color_name"
            class="px-4 py-2 rounded-full text-sm font-medium text-white bg-gray-500"
          >
            Cor: {{ item.color_name }}
          </span>
        </div>

        <h3 class="text-base md:text-lg font-semibold text-gray-800 mt-6 mb-2">Descrição</h3>
        <div class="max-h-40 md:max-h-60 lg:max-h-72 overflow-y-auto pr-2 border border-gray-200 rounded-lg p-3 bg-gray-50">
          <p class="text-sm md:text-base text-gray-700 text-left whitespace-pre-line break-words">
            {{ item.description || "Sem descrição disponível." }}
          </p>
        </div>
      </div>
    </div>

    <div class="w-full md:max-w-4xl lg:max-w-6xl xl:max-w-7xl md:flex md:flex-col">
      <div 
        v-if="userInfo" 
        class="w-full mt-6 md:hidden"
      >
        <div 
          class="flex items-center p-4 border border-gray-200 rounded-lg bg-gray-50 hover:bg-gray-100 cursor-pointer" 
          @click="viewUserProfile(item.user_id)"
        >
          <div class="flex items-center">
            <img 
              :src="userInfo.foto || notAvailableImage" 
              alt="Foto do usuário" 
              class="w-12 h-12 rounded-full object-cover border-2 border-laranja"
            />
            <div class="ml-4">
              <h3 class="text-sm font-semibold text-azul">Postado por:</h3>
              <p class="text-gray-800 font-medium">{{ 
                userInfo.first_name && userInfo.last_name ? 
                  `${userInfo.first_name} ${userInfo.last_name}` : 
                userInfo.first_name ? userInfo.first_name : 
                userInfo.last_name ? userInfo.last_name : 
                userInfo.username 
              }}</p>
            </div>
          </div>
          <div class="ml-auto">
            <span class="text-azul text-sm font-medium">Ver perfil</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block ml-1 text-azul" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <div class="w-full flex justify-center mt-8 md:mt-10 lg:mt-12">
      <button
        v-if="currentUser?.id !== item.user_id"
        class="bg-laranja text-white w-full md:w-[70%] lg:w-[50%] xl:w-[60%] font-medium py-4 md:py-5 lg:py-6 rounded-full hover:scale-110 transition-transform duration-300 text-center text-lg lg:text-xl xl:text-2xl shadow-lg border-2 border-laranja/20"
        @click="handleChat"
      >
        <span v-if="itemStatus === 'found'">É meu item</span>
        <span v-else>Achei este item</span>
      </button>

      <button
        v-else-if="currentUser?.id === item.user_id"
        class="bg-red-500 text-white w-full md:w-[70%] lg:w-[50%] xl:w-[60%] font-medium py-4 md:py-5 lg:py-6 rounded-full hover:scale-110 transition-transform duration-300 text-center text-lg lg:text-xl xl:text-2xl shadow-lg border-2 border-red-400/20"
        @click="openDeleteModal"
      >
        Excluir meu item
      </button>
    </div>
  </div>

  <Teleport to="body">
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div
        class="bg-azul p-6 rounded-lg shadow-lg w-full max-w-sm sm:max-w-md lg:max-w-lg text-center relative"
        @click.stop
      >
        <p class="text-white font-inter text-lg">
          Você realmente deseja excluir este item do AcheiUnB?
        </p>
        <div class="flex flex-col sm:flex-row justify-center mt-4 gap-4">
          <button
            class="bg-red-500 text-white font-inter px-4 py-2 rounded-md hover:bg-red-600 transition w-full sm:w-auto"
            @click="handleDeleteConfirmed"
          >
            Excluir
          </button>
          <button
            class="bg-white font-inter px-4 py-2 rounded-md hover:bg-gray-200 transition w-full sm:w-auto"
            @click="closeDeleteModal"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  </Teleport>

  <div class="fixed bottom-0 w-full">
    <MainMenu :activeIcon="itemStatus === 'found' ? 'found' : 'lost'" />
  </div>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />
  <Alert v-if="submitSuccess" type="success" :message="alertMessage" @closed="submitSuccess = false" />

  <!-- Modal de denúncia -->
  <div v-if="showReportModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg w-full max-w-md p-6 shadow-lg">
      <h3 class="text-xl font-bold mb-4 text-gray-800">Denunciar item</h3>
      
      <p class="text-sm text-gray-600 mb-4">
        Informe o motivo da sua denúncia. Nossa equipe irá analisar e tomar as medidas necessárias.
      </p>
      
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
        <select 
          v-model="reportForm.category" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-laranja"
        >
          <option value="" disabled>Selecione um motivo</option>
          <option value="Item ilegal/proibido">Item ilegal/proibido</option>
          <option value="Imagem inadequada">Imagem inadequada</option>
          <option value="Item falso">Item falso</option>
          <option value="Spam/golpe">Spam/golpe</option>
          <option value="Outros">Outros</option>
        </select>
      </div>
      
      <div class="mb-5">
        <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
        <textarea 
          v-model="reportForm.description" 
          rows="4" 
          placeholder="Descreva o problema com mais detalhes"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-laranja"
        ></textarea>
      </div>

      <div class="mb-5">
        <label class="block text-sm font-medium text-gray-700 mb-1">Anexo</label>
        <input 
          type="file" 
          @change="handleFileUpload" 
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-laranja"
        />
      </div>
      
      <div class="flex justify-end gap-3">
        <button 
          @click="closeReportModal" 
          class="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
        >
          Cancelar
        </button>
        <button 
          @click="submitReport" 
          :disabled="isReportSubmitting"
          class="px-4 py-2 text-white bg-laranja rounded-md hover:bg-laranja/80 transition-colors disabled:bg-gray-400"
        >
          {{ isReportSubmitting ? 'Enviando...' : 'Enviar denúncia' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import api from "../services/api";
import ItemHeader from "../components/Item-Header.vue";
import MainMenu from "../components/Main-Menu.vue";
import { useRoute, useRouter } from "vue-router";
import notAvailableImage from "@/assets/images/not-available.png";
import Alert from "@/components/Alert.vue";
import { deleteItem } from "@/services/apiItems";

const route = useRoute();
const router = useRouter();
const item = ref(null);
const itemStatus = ref("");
const currentUser = ref(null);
const userInfo = ref(null);
const activeIndex = ref(0);
const isMobile = ref(window.innerWidth < 768);

const alertMessage = ref("");
const submitError = ref(false);
const submitSuccess = ref(false);
const isSubmitting = ref(false);

const isLoaded = ref(false);

const confirmDelete = async (itemId) => {
  try {
    await deleteItem(itemId);
    router.push(`/${itemStatus.value}`);
  } catch (error) {
    console.error("Erro ao excluir item:", error);
    alertMessage.value = "Erro ao excluir item.";
    submitError.value = true;
  }
};

const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  return `${date.toLocaleDateString("pt-BR", {
    timeZone: "America/Sao_Paulo",
  })} às ${date.toLocaleTimeString("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "America/Sao_Paulo",
  })}`;
};

const nextImage = () => {
  if (!item.value?.image_urls?.length) return;
  activeIndex.value = (activeIndex.value + 1) % item.value.image_urls.length;
};

const prevImage = () => {
  if (!item.value?.image_urls?.length) return;
  activeIndex.value =
    (activeIndex.value - 1 + item.value.image_urls.length) % item.value.image_urls.length;
};

const handleResize = () => {
  isMobile.value = window.innerWidth < 768;
};

async function fetchItem() {
  try {
    const response = await api.get(`/items/${route.query.idItem}/`);
    item.value = response.data;
    itemStatus.value = item.value.status;
    isLoaded.value = true;
    
    if (item.value.user_id) {
      fetchUserInfo(item.value.user_id);
    }
  } catch (error) {
    console.error("Erro ao carregar item:", error);
    alertMessage.value = "Erro ao carregar item.";
    submitError.value = true;
  }
}

async function fetchCurrentUser() {
  try {
    const response = await api.get(`/auth/user/`);
    currentUser.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar usuário:", error);
    alertMessage.value = "Erro ao buscar usuário.";
    submitError.value = true;
  }
}

async function fetchUserInfo(userId) {
  try {
    const response = await api.get(`/auth/user-profile/${userId}/`);
    userInfo.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar informações do usuário:", error);
    userInfo.value = null;
  }
}

function viewUserProfile(userId) {
  if (!userId) return;
  router.push({ name: 'UserProfile', params: { id: userId } });
}

const handleChat = async () => {
  try {
    if (!item.value || !item.value.id) {
      console.error("Item inválido ou não carregado:", item.value);
      return;
    }
    if (!currentUser.value?.id || !item.value?.user_id) {
      console.error("IDs de usuário inválidos:", {
        currentUser: currentUser.value,
        item: item.value,
      });
      return;
    }

    isSubmitting.value = true;

    const searchParams = {
      participant_1: currentUser.value.id,
      participant_2: item.value.user_id,
      item_id: item.value.id,
    };

    const searchResponse = await api.get("/chat/chatrooms/", {
      params: searchParams,
    });
    const chatsEncontrados = searchResponse.data;

    if (chatsEncontrados && chatsEncontrados.length > 0) {
      router.push(`/chat/${chatsEncontrados[0].id}?itemId=${item.value.id}`);
      return;
    }

    const chatData = {
      participant_1: currentUser.value.id,
      participant_2: item.value.user_id,
      item_id: item.value.id,
    };

    const createResponse = await api.post("/chat/chatrooms/", chatData);

    if (createResponse.data?.id) {
      router.push(`/chat/${createResponse.data.id}?itemId=${item.value.id}`);
    } else {
      throw new Error("Resposta inválida ao criar chatroom");
    }
  } catch (error) {
    console.error("Erro ao criar/aceder chat:", error.response?.data || error.message);
    alertMessage.value = "Erro ao criar chat.";
    submitError.value = true;
  } finally {
    isSubmitting.value = false;
  }
};

// Variáveis para o modal de denúncia
const showReportModal = ref(false);
const isReportSubmitting = ref(false);
const reportForm = ref({
  category: "",
  description: "",
  attachment: null,
});

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  reportForm.value.attachment = file;
};

// Funções para abrir e fechar o modal
const openReportModal = () => {
  showReportModal.value = true;
  reportForm.value = {
    category: "",
    description: "",
    attachment: null,
  };
};

const closeReportModal = () => {
  showReportModal.value = false;
};

// Função para enviar a denúncia para a API
const submitReport = async () => {
  if (!reportForm.value.category) {
    alertMessage.value = "Por favor, selecione uma categoria para a denúncia.";
    submitError.value = true;
    return;
  }

  const formData = new FormData();
  formData.append("report_type", "item");
  formData.append("categories", reportForm.value.category);
  formData.append("description", reportForm.value.description);
  formData.append("item", item.value.id);
  if (reportForm.value.attachment) {
    formData.append("attachment", reportForm.value.attachment);
  }

  try {
    isReportSubmitting.value = true;

    const response = await api.post("/reports/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    alertMessage.value = "Denúncia enviada com sucesso!";
    submitSuccess.value = true;
    closeReportModal();
  } catch (error) {
    console.error("Erro ao enviar denúncia:", error);
    alertMessage.value = "Erro ao enviar denúncia. Só é possível enviar uma denúncia por item.";
    submitError.value = true;
  } finally {
    isReportSubmitting.value = false;
  }
};

const showDeleteModal = ref(false);

const openDeleteModal = () => {
  showDeleteModal.value = true;
  document.body.style.overflow = "hidden";
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  document.body.style.overflow = "";
};

const handleDeleteConfirmed = async () => {
  try {
    await deleteItem(item.value.id);
    closeDeleteModal();
    router.push(`/${itemStatus.value}`);
  } catch (error) {
    closeDeleteModal();
    console.error("Erro ao excluir item:", error);
    alertMessage.value = "Erro ao excluir item.";
    submitError.value = true;
  }
};

onMounted(async () => {
  await fetchCurrentUser();
  await fetchItem();
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
});
</script>

<style scoped></style>
