import api from "./api";
import { filtersState } from "@/store/filters";

const API_BASE_URL = `${import.meta.env.VITE_URL_PROD}/api/items`;

// Função para buscar itens perdidos com filtros opcionais
export const fetchLostItems = async ({
  page = 1,
  search = "",
  category_name = "",
  location_name = "",
}) => {
  const params = {
    page,
    ...(filtersState.searchQuery && { search: filtersState.searchQuery }),
    ...(filtersState.activeCategory && { category_name: filtersState.activeCategory }),
    ...(filtersState.activeLocation && { location_name: filtersState.activeLocation }),
  };

  const response = await api.get(`${API_BASE_URL}/lost/`, { params });
  return response.data;
};

// Função para buscar itens encontrados com filtros opcionais
export const fetchFoundItems = async ({
  page = 1,
  search = "",
  category_name = "",
  location_name = "",
}) => {
  try {
    const params = {
      page,
      ...(filtersState.searchQuery && { search: filtersState.searchQuery }),
      ...(filtersState.activeCategory && { category_name: filtersState.activeCategory }),
      ...(filtersState.activeLocation && { location_name: filtersState.activeLocation }),
    };

    const response = await api.get(`${API_BASE_URL}/found/`, { params });
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar itens encontrados:", error);
    throw error;
  }
};

export const fetchMyItemsFound = async () => {
  try {
    const response = await api.get(`${API_BASE_URL}/found/my-items/`);
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar itens encontrados:", error);
    throw error;
  }
};

export const fetchMyItemsLost = async () => {
  try {
    const response = await api.get(`${API_BASE_URL}/lost/my-items/`);
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar itens encontrados:", error);
    throw error;
  }
};

export const deleteItem = async (itemId) => {
  try {
    await api.delete(`${API_BASE_URL}/${itemId}/`);
  } catch (error) {
    console.error("Erro ao deletar o item:", error);
    throw error;
  }
};
