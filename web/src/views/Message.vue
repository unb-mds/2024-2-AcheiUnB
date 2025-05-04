<template>
  <div class="relative flex flex-col h-screen bg-gray-100">

    <div class="flex absolute inset-0 justify-center items-center pointer-events-none z-0">
      <img
        src="@/assets/icons/Favicon.png"
        alt="Watermark"
        class="w-48 md:w-64 lg:w-80 opacity-20"
      />
    </div>

    <HeaderMessage
      v-if="receiverId && itemId"
      :itemId="String(itemId)" 
      :userId="String(receiverId)"
      class="fixed top-0 left-0 w-full z-20"
    />

    <div ref="messagesContainer" class="relative flex-1 pt-32 pb-24 px-4 overflow-y-auto z-10">
      <div v-for="message in messages" :key="message.id" class="mb-2 flex">
        
        <div v-if="message.sender === currentUser?.id" class="flex w-full justify-end">
          <div class="bg-laranja text-white p-3 rounded-2xl max-w-[70%] break-words shadow-md">
            <p class="text-sm">{{ message.content }}</p>
            <span class="text-xs opacity-75 mt-1 block text-right">
              {{ formatTime(message.timestamp) }}
            </span>
          </div>
        </div>

        <div v-else class="flex w-full justify-start">
          <div class="bg-gray-300 text-gray-800 p-3 rounded-2xl max-w-[70%] break-words shadow-md">
            <p class="text-sm">{{ message.content }}</p>
            <span class="text-xs opacity-75 mt-1 block text-left">
              {{ formatTime(message.timestamp) }}
            </span>
          </div>
        </div>

      </div>
    </div>
    
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 z-20">
      <div class="flex">
        <input
          v-model="messageContent"
          @keyup.enter="sendMessage"
          type="text"
          maxlength="80"
          placeholder="Digite uma mensagem (máx. 80 caracteres)..."
          class="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:border-laranja"
        />
        <button
          @click="sendMessage"
          :disabled="!messageContent.trim()"
          class="ml-2 bg-laranja text-white px-4 py-2 rounded-full hover:bg-laranja-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Enviar
        </button>
      </div>
    </div>
    
  </div>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "../services/api";
import HeaderMessage from "@/components/Header-Message.vue";
import Alert from "@/components/Alert.vue";
import { io } from "socket.io-client";

const route = useRoute();
const messages = ref([]);
const messageContent = ref("");
const currentUser = ref(null);
const item = ref(null);
const receiverId = ref(null);
const alertMessage = ref("");
const submitError = ref(false);

const chatroomId = ref(route.params.chatroomId || route.query.chatroomId);
const itemId = ref(route.params.itemId || route.query.itemId);

const socket = ref(null);

const connectWebSocket = () => {
  const WS_URL = import.meta.env.VITE_WS_URL;

  socket.value = io(WS_URL, {
    transports: ["websocket"],
    path: "/socket.io/", // caminho padrão do socket.io, seu nginx já está configurado para /socket.io/
    query: { chatroomId: chatroomId.value }
  });

  socket.value.on("connect", () => {
    console.log("Socket.IO conectado:", socket.value.id);
  });

  socket.value.on("receive_message", (data) => {
    console.log("Nova mensagem recebida via Socket.IO:", data);
    messages.value.push(data);
    scrollToBottom();
  });

  socket.value.on("disconnect", () => {
    console.warn("Socket.IO desconectado.");
  });

  socket.value.on("connect_error", (err) => {
    console.error("Erro ao conectar no Socket.IO:", err);
  });
};


if (!chatroomId.value) {
  console.error("ID do chat não encontrado na rota");
} else {
  console.log("chatroomId:", chatroomId.value);
}

// const sendMessage = async () => {
//   if (!chatroomId.value) {
//     console.error("ID do chat não encontrado, não é possível enviar mensagem");
//     return;
//   }
//   if (!messageContent.value.trim()) {
//     console.warn("Mensagem vazia, nada a enviar");
//     return;
//   }
  
//   try {
//     console.log("Enviando mensagem para room:", chatroomId.value, "Conteúdo:", messageContent.value);
//     // Chama a API para enviar a mensagem
//     await api.post("/chat/messages/", {
//       room: chatroomId.value,
//       content: messageContent.value
//     });
//     messageContent.value = "";
//     await fetchMessages();
//   } catch (error) {
//     console.error("Erro ao enviar mensagem:", error.response?.data || error.message);
//   }
// };

const sendMessage = async () => {
  if (!chatroomId.value) {
    console.error("ID do chat não encontrado, não é possível enviar mensagem");
    return;
  }
  if (!messageContent.value.trim()) {
    console.warn("Mensagem vazia, nada a enviar");
    return;
  }

  const conteudo = messageContent.value.trim();

  try {
    console.log("Enviando mensagem para room:", chatroomId.value, "Conteúdo:", conteudo);

    // Primeiro, salva no banco de dados via API REST
    const response = await api.post("/chat/messages/", {
      room: chatroomId.value,
      content: conteudo
    });

    const mensagemSalva = response.data;

    // Agora, envia a mensagem pelo Socket.IO
    if (socket.value && socket.value.connected) {
      socket.value.emit("send_message", mensagemSalva);
    } else {
      console.warn("Socket.IO não está conectado. Mensagem salva no banco, mas não enviada em tempo real.");
    }

    messageContent.value = "";
    await fetchMessages();

  } catch (error) {
    console.error("Erro ao enviar mensagem:", error.response?.data || error.message);
    alertMessage.value = "Erro ao enviar mensagem.";
    submitError.value = true;
  }
};


const fetchMessages = async () => {
  if (!chatroomId.value) return;
  try {
    const response = await api.get("/chat/messages/", {
      params: { room: chatroomId.value }
    });
    messages.value = response.data.results || response.data;
  } catch (error) {
    console.error("Erro ao buscar mensagens:", error);
  }
};

const fetchCurrentUser = async () => {
  try {
    const response = await api.get("/auth/user/");
    currentUser.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar usuário:", error);
  }
};

const fetchItem = async () => {
  if (!itemId.value) return;
  try {
    const response = await api.get(`/items/${itemId.value}`);
    item.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar item:", error);
  }
};

const fetchReceiverId = async () => {
  if (!itemId.value) return;
  try {
    const response = await api.get(`/items/${itemId.value}`);
    receiverId.value = response.data.user_id;
  } catch (error) {
    console.error("Erro ao buscar dono do item:", error);
  }
};

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString("pt-BR", {
    hour: "2-digit",
    minute: "2-digit"
  });
};

const fetchChatroomData = async () => {
  if (!chatroomId.value) return;
  try {
    await api.get(`/chat/chatrooms/${chatroomId.value}/`);
    // Se necessário, processar os dados do chatroom aqui.
  } catch (error) {
    console.error("Erro ao buscar dados do chatroom:", error);
  }
};
const messagesContainer = ref(null);


const scrollToBottom = () => {
  const container = messagesContainer.value;
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
};



onMounted(async () => {
  await fetchCurrentUser();
  await fetchItem();
  await fetchReceiverId();
  await fetchChatroomData();
  await fetchMessages();
  connectWebSocket();
});
</script>

<style scoped></style>