<template>
  <div class="relative flex flex-col bg-gray-100" style="min-height: 100dvh; height: 100dvh;">

    <div class="flex absolute inset-0 justify-center items-center pointer-events-none z-0">
      <img
        src="@/assets/icons/Favicon2.png"
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

    <div ref="messagesContainer" class="relative flex-1 pt-32 pb-28 px-4 overflow-y-auto z-10">
      <!-- Indicador de carregamento com barra de progresso -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center h-full">
        <img
          src="@/assets/icons/Favicon.png"
          alt="AcheiUnB"
          class="w-16 h-16 mb-4 animate-pulse"
        />
        <div class="w-48 h-1.5 bg-gray-200 rounded-full overflow-hidden">
          <div class="loading-bar-progress bg-laranja h-full"></div>
        </div>
        <p class="mt-4 text-sm text-gray-600">Carregando mensagens...</p>
      </div>
      
      <!-- Exibe as mensagens quando não estiver carregando -->
      <template v-else>
        <div v-for="group in groupedMessages" :key="group.date" class="mb-4">
        <!-- Data separator com estilo de balão WhatsApp -->
        <div class="flex justify-center mb-3">
          <div class="bg-gray-200 text-gray-600 text-xs font-medium px-4 py-1.5 rounded-full shadow-sm">
            {{ group.formattedDate }}
          </div>
        </div>
        
        <div v-for="message in group.messages" :key="message.id" class="mb-2 flex">
          
          <div v-if="message.sender === currentUser?.id" class="flex w-full justify-end">
            <div class="bg-laranja text-white p-3 rounded-2xl max-w-[70%] break-words shadow-md">
              <p class="text-sm">{{ message.content }}</p>
              <div class="flex items-center justify-end mt-1">
                <!-- Check de mensagem lida - COMENTADO PARA NÃO MOSTRAR VISUALMENTE -->
                <!-- <span v-if="message.is_read" class="text-xs mr-1 text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="inline-block" viewBox="0 0 16 16">
                    <path d="M8.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L2.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093L8.95 4.992a.252.252 0 0 1 .02-.022zm-.92 5.14.92.92a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 1 0-1.091-1.028L9.477 9.417l-.485-.486-.943 1.179z"/>
                  </svg>
                </span>
                <span v-else class="text-xs mr-1 text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="inline-block" viewBox="0 0 16 16">
                    <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
                  </svg>
                </span> -->
                <span class="text-xs opacity-75">
                  {{ formatTime(message.timestamp) }}
                </span>
              </div>
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
      </template>
    </div>
    
    <div class="fixed left-0 right-0 bg-white border-t border-gray-200 p-4 z-20 chat-bar-fix">
      <div class="relative">
        <div v-if="showEmojiPicker" class="absolute bottom-full mb-2 bg-white p-2 rounded-lg shadow-lg border border-gray-300 z-30 max-h-64 overflow-y-auto emoji-picker-area">
          <div class="grid grid-cols-8 gap-1">
            <button 
              v-for="emoji in emojis" 
              :key="emoji" 
              @click="addEmoji(emoji)" 
              class="text-xl p-1 hover:bg-gray-100 rounded transition-colors"
            >
              {{ emoji }}
            </button>
          </div>
        </div>
        
        <div class="flex items-center">
          <button
            @click="toggleEmojiPicker"
            class="p-1 px-0.5 text-gray-500 hover:text-laranja focus:outline-none mr-1 emoji-picker-area"
            title="Inserir emoji"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
            </svg>
          </button>
          
          <input
            ref="inputRef"
            v-model="messageContent"
            @focus="handleInputFocus"
            @keyup.enter="sendMessage"
            :desabled="isSubmitting"
            type="text"
            maxlength="80"
            placeholder="Digite uma mensagem..."
            class="flex-1 border border-gray-300 rounded-full px-4 py-2 text-base focus:outline-none focus:border-laranja"
          />
          
          <button
            @click="sendMessage"
            :disabled="!messageContent.trim()"
            class="ml-1 bg-laranja text-white p-2.5 rounded-full hover:bg-laranja-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            title="Enviar mensagem"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import HeaderMessage from "@/components/Header-Message.vue";
import { io } from "socket.io-client";

const route = useRoute();
const router = useRouter();
const messages = ref([]);
const messageContent = ref("");
const currentUser = ref(null);
const item = ref(null);
const receiverId = ref(null);
const showEmojiPicker = ref(false);
const isLoading = ref(true); // Adicionando estado de loading
const isSubmitting = ref(false);

const emojis = [
  "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", 
  "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚", 
  "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩", 
  "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣", "😖", 
  "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", 
  "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", 
  "👍", "👎", "👏", "🙌", "🤝", "🙏", "✌️", "🤞", "🤟", "🤘"
];

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
    if (chatroomId.value) {
      socket.value.emit('join_chat', chatroomId.value);
    }
  });

  // Adicionado handler para quando uma mensagem é recebida
  socket.value.on("receive_message", (data) => {
    console.log("Nova mensagem recebida via Socket.IO:", data);

    // Verificar se a mensagem pertence ao chat atual
    if (data.chatroomId !== chatroomId.value) {
      console.warn("Mensagem recebida para um chat diferente. Ignorando.");
      return;
    }

    messages.value.push(data);
    
    // Processar as mensagens para agrupá-las por data
    processMessages();
    
    scrollToBottom();
    
    // Marcar mensagem como lida se não for do usuário atual
    if (data.sender !== currentUser.value?.id) {
      markMessageAsRead(data.id);
    }
  });
  
  // Listener para atualização de status de mensagens
  socket.value.on("message_status_updated", (data) => {
    console.log("Status de mensagem atualizado:", data);
    if (data.chat_id === chatroomId.value) {
      updateMessagesReadStatus(data.message_ids);
    }
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

// Adicionar validação no envio de mensagens
const sendMessage = async () => {
  if (!chatroomId.value) {
    console.error("ID do chat não encontrado, não é possível enviar mensagem");
    return;
  }
  if (!messageContent.value.trim()) {
    console.warn("Mensagem vazia, nada a enviar");
    return;
  }

  isSubmitting.value = true;
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
      socket.value.emit("send_message", { ...mensagemSalva, chatroomId: chatroomId.value });
    } else {
      console.warn("Socket.IO não está conectado. Mensagem salva no banco, mas não enviada em tempo real.");
      // Como Socket.IO não está conectado, adicionamos a mensagem manualmente ao array
      messages.value.push(mensagemSalva);
      processMessages();
      scrollToBottom();
    }

    messageContent.value = "";
    await nextTick();
    scrollToBottom();
    // Removida a chamada fetchMessages() pois agora usamos apenas WebSocket para atualização

  } catch (error) {
    console.error("Erro ao enviar mensagem:", error.response?.data || error.message);
  } finally {
    isSubmitting.value = false;
  }
};


const fetchMessages = async () => {
  if (!chatroomId.value) return;
  isLoading.value = true; // Ativa o estado de carregamento
  
  try {
    const response = await api.get("/chat/messages/", {
      params: { room: chatroomId.value }
    });
    messages.value = response.data.results || response.data;
    
    // Processar as mensagens para agrupá-las por data
    processMessages();
    
    // Marcar mensagens como lidas
    markMessagesAsRead();
    
    setTimeout(() => {
      scrollToBottom();
    }, 100);
  } catch (error) {
    console.error("Erro ao buscar mensagens:", error);
  } finally {
    isLoading.value = false; // Finaliza o estado de carregamento independentemente do resultado
  }
};

// Função para marcar mensagens como lidas
const markMessagesAsRead = async () => {
  if (!chatroomId.value || !currentUser.value?.id) return;
  
  try {
    const unreadMessages = messages.value.filter(
      msg => !msg.is_read && msg.sender !== currentUser.value.id
    );
    
    if (unreadMessages.length === 0) return;
    
    const messageIds = unreadMessages.map(msg => msg.id);
    
    const response = await api.post("/chat/messages/mark_as_read/", {
      chat_id: chatroomId.value
    });
    console.log("Mensagens marcadas como lidas");
    
    // Atualizar status das mensagens localmente
    updateMessagesReadStatus(messageIds);
    
    // Emitir evento para atualizar o Main-Menu e remover animação
    const event = new CustomEvent('unread-messages-updated');
    window.dispatchEvent(event);
    
    // Emitir evento via socket para notificar o outro usuário sobre as mensagens lidas
    if (socket.value && socket.value.connected) {
      socket.value.emit('messages_read', {
        chat_id: chatroomId.value,
        message_ids: messageIds
      });
    }
  } catch (error) {
    console.error("Erro ao marcar mensagens como lidas:", error);
  }
};

// Função para marcar uma mensagem específica como lida
const markMessageAsRead = async (messageId) => {
  if (!chatroomId.value || !currentUser.value?.id) return;
  
  try {
    await api.post("/chat/messages/mark_as_read/", {
      chat_id: chatroomId.value,
      message_id: messageId
    });
    
    // Emitir evento via socket para notificar o outro usuário sobre a mensagem lida
    if (socket.value && socket.value.connected) {
      socket.value.emit('messages_read', {
        chat_id: chatroomId.value,
        message_ids: [messageId]
      });
    }
  } catch (error) {
    console.error(`Erro ao marcar mensagem ${messageId} como lida:`, error);
  }
};

// Função para atualizar localmente o status das mensagens
const updateMessagesReadStatus = (messageIds) => {
  messages.value = messages.value.map(msg => {
    if (messageIds.includes(msg.id)) {
      return { ...msg, is_read: true };
    }
    return msg;
  });
  
  // Reprocessar as mensagens para garantir que as alterações de status sejam refletidas
  processMessages();
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

// Função para lidar com o foco no input
const handleInputFocus = () => {
  // Marcar mensagens como lidas quando o usuário foca no input
  markMessagesAsRead();
};

const scrollToBottom = () => {
  const container = messagesContainer.value;
  if (container) {
    nextTick(() => {
      container.scrollTop = container.scrollHeight - container.clientHeight;
    });
  }
};

// Função para adicionar o emoji selecionado à mensagem
const addEmoji = (emoji) => {
  messageContent.value += emoji;
};

// Função para alternar a visibilidade do seletor de emojis
const toggleEmojiPicker = () => {
  showEmojiPicker.value = !showEmojiPicker.value;
  
  // Se o seletor estiver aberto, configuramos um listener de clique para fechá-lo quando clicar fora
  if (showEmojiPicker.value) {
    setTimeout(() => {
      window.addEventListener('click', closeEmojiPickerOnClickOutside);
    }, 100);
  } else {
    window.removeEventListener('click', closeEmojiPickerOnClickOutside);
  }
};

// Função para fechar o seletor de emojis quando clicar fora dele
const closeEmojiPickerOnClickOutside = (event) => {
  const emojiPickerElements = document.querySelectorAll('.emoji-picker-area');
  let clickedInside = false;
  
  emojiPickerElements.forEach(element => {
    if (element.contains(event.target)) {
      clickedInside = true;
    }
  });
  
  if (!clickedInside) {
    showEmojiPicker.value = false;
    window.removeEventListener('click', closeEmojiPickerOnClickOutside);
  }
};

// Função para agrupar mensagens por data
const groupMessagesByDate = (messages) => {
  const groups = {};
  
  messages.forEach(message => {
    const date = new Date(message.timestamp);
    const dateStr = date.toLocaleDateString('pt-BR');
    
    if (!groups[dateStr]) {
      groups[dateStr] = [];
    }
    
    groups[dateStr].push(message);
  });
  
  return Object.entries(groups).map(([date, messages]) => {
    return {
      date,
      formattedDate: formatDateLabel(new Date(messages[0].timestamp)),
      messages
    };
  }).sort((a, b) => new Date(a.date.split('/').reverse().join('-')) - new Date(b.date.split('/').reverse().join('-')));
};

// Função para formatar a data como "Hoje", "Ontem", "Anteontem" ou a data completa
const formatDateLabel = (date) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  
  const twoDaysAgo = new Date(today);
  twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);
  
  const messageDate = new Date(date);
  messageDate.setHours(0, 0, 0, 0);
  
  if (messageDate.getTime() === today.getTime()) {
    return 'Hoje';
  } else if (messageDate.getTime() === yesterday.getTime()) {
    return 'Ontem';
  } else if (messageDate.getTime() === twoDaysAgo.getTime()) {
    return 'Anteontem';
  } else {
    return date.toLocaleDateString('pt-BR', { 
      day: '2-digit', 
      month: '2-digit', 
      year: 'numeric' 
    });
  }
};

// Computar mensagens agrupadas por data
const groupedMessages = ref([]);

// Função para processar as mensagens e agrupá-las por data
const processMessages = () => {
  groupedMessages.value = groupMessagesByDate(messages.value);
};

// Quando o componente é montado
onMounted(async () => {
  await fetchCurrentUser();
  await fetchItem();
  await fetchReceiverId();
  await fetchChatroomData();
  await fetchMessages();
  connectWebSocket();
  
  // Garantir rolagem para o final mesmo após todas as operações assíncronas
  setTimeout(() => {
    scrollToBottom();
  }, 300);
});

// Cleanup ao desmontar o componente
onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.disconnect();
  }
  window.removeEventListener('click', closeEmojiPickerOnClickOutside);
});

</script>

<style scoped>
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.6; }
  100% { opacity: 1; }
}

.animate-pulse {
  animation: pulse 1.5s infinite;
}

@keyframes progress {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(200%); }
}

.loading-bar-progress {
  animation: progress 1.8s ease-in-out infinite;
  width: 50%;
}

.chat-bar-fix {
  bottom: 0;
  height: max-content;
  padding-bottom: 16px;
}
@media (max-width: 640px) {
  .chat-bar-fix {
    bottom: env(keyboard-inset-height, 0px);
    padding-bottom: env(safe-area-inset-bottom, 0);
  }
}
</style>