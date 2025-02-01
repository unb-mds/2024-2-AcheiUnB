import axios from "axios";
import router from "@/router";

const baseAPI = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

baseAPI.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response.status === 401) {
      router.push({ name: "Login" });
    }

    return Promise.reject(error);
  },
);

export default baseAPI;
