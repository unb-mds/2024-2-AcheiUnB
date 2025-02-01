import baseAPI from "./base-api";

const API_BASE_URL = "/auth";

export const validateToken = async () => {
  try {
    const response = await baseAPI.get(`${API_BASE_URL}/validate/`);
    return response;
  } catch (error) {
    console.log("Uusário não autenticado.", error);
  }
};

export const fetchUserData = async () => {
  try {
    const response = await baseAPI.get(`${API_BASE_URL}/user/`);
    return response.data;
  } catch (error) {
    console.log("Uusário não autenticado.", error);
  }
};
