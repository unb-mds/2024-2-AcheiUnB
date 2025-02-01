<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import api from "../services/api";

const router = useRouter();
const route = useRoute();
const chatId = ref(route.params.chatroomId); // ID do chat na URL
const chatUser = ref({ name: "Carregando...", profile_picture: "" });
const currentUser = ref({});
const messages = ref([]);
const newMessage = ref("");
const suggestions = ref(["Ainda está com o item?", "Posso te entregar na faculdade?"]);

// Pegando parâmetros da URL caso um chatroom ainda não exista
const participant_2 = ref(route.query.participant_2);
const item_id = ref(route.query.item_id);

// Atualiza o chat caso a URL mude
watch(
  () => route.params.chatroomId,
  (newId) => {
    chatId.value = newId;
    fetchChat();
  },
);

// Buscar usuário logado
const fetchCurrentUser = async () => {
  try {
    const response = await api.get(`/api/users/me/`);
    currentUser.value = {
      id: response.data.id,
      name: response.data.nome,
      profile_picture: response.data.foto || "https://via.placeholder.com/40",
    };
  } catch (error) {
    console.error("Erro ao buscar usuário logado:", error);
  }
};

// Buscar informações do usuário com quem está conversando
const fetchChatUser = async (userId) => {
  try {
    const response = await api.get(`/api/users/${userId}/`);
    return {
      id: response.data.id,
      name: response.data.nome,
      profile_picture: response.data.foto || "https://via.placeholder.com/40",
    };
  } catch (error) {
    console.error("Erro ao buscar usuário do chat:", error);
    return { name: "Usuário desconhecido", profile_picture: "https://via.placeholder.com/40" };
  }
};

// Buscar informações do chat e carregar mensagens
const fetchChat = async () => {
  if (!chatId.value) {
    console.log("❌ Nenhum chatroomId na URL. Criando novo chat...");
    await createChat();
    return;
  }

  try {
    console.log(`🔍 Buscando chatroom com ID: ${chatId.value}`);
    const response = await api.get(`/chat/chatrooms/${chatId.value}/`);
    console.log("✅ Dados do chat recebidos:", response.data);

    // Definir o usuário com quem está conversando
    const otherUserId =
      response.data.participant_1 === currentUser.value.id
        ? response.data.participant_2
        : response.data.participant_1;

    chatUser.value = await fetchChatUser(otherUserId); // Busca os dados do outro usuário

    messages.value = response.data.messages;
  } catch (error) {
    console.error("Erro ao buscar chat:", error);
  }
};

// Criar um novo chatroom automaticamente se não existir
const createChat = async () => {
  if (!participant_2.value || !item_id.value) {
    console.error("⚠️ Erro: participant_2 ou item_id não foram passados na URL.");
    return;
  }

  try {
    console.log("🔨 Criando novo chatroom...");
    const response = await api.post("/chat/chatrooms/", {
      participant_1: currentUser.value.id,
      participant_2: participant_2.value,
      item_id: item_id.value,
    });

    chatId.value = response.data.id; // Atualiza o ID do chat
    router.replace(`/chat/${chatId.value}`); // Atualiza a URL com o novo chatroomId
    console.log("✅ Novo chatroom criado:", response.data);
    await fetchChat(); // Carrega as mensagens do novo chat criado
  } catch (error) {
    console.error("Erro ao criar chatroom:", error);
  }
};

// Enviar nova mensagem
const sendMessage = async (text) => {
  if (!text.trim() || !chatId.value) {
    console.error("❌ Erro: Nenhum chatroom associado para enviar mensagem.");
    return;
  }

  try {
    console.log(`💬 Enviando mensagem para chatroom ${chatId.value}...`);
    const response = await api.post("/chat/messages/", {
      room: chatId.value,
      content: text,
    });

    messages.value.push(response.data);
    newMessage.value = "";
    console.log("✅ Mensagem enviada:", response.data);
  } catch (error) {
    console.error("Erro ao enviar mensagem:", error);
  }
};

// Retornar para a tela anterior
const goBack = () => {
  router.push("/chats");
};

// Carregar os dados quando a tela for aberta
onMounted(async () => {
  await fetchCurrentUser();
  await fetchChat();
});
</script>
