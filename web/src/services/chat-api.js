import baseAPI from "./base-api";

const API_BASE_URL = "/chat";

export const createChatroom = async (paticipant_1, paticipant_2, item_id) => {
  try {
    const response = await baseAPI.post(`${API_BASE_URL}/chat/chatrooms/`, {
      paticipant_1,
      paticipant_2,
      item_id,
    });
    return response.data;
  } catch (error) {
    console.error("Erro criar o chat", error);
    throw error;
  }
};
