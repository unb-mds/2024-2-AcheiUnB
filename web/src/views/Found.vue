<template>
  <div class="min-h-screen pb-32">
    <div class="fixed w-full top-0 z-30">
      <SearchHeader />
    </div>

    <div class="pt-24 pb-8">
      <SubMenu />
    </div>

    <EmptyState
      v-if="!loading && foundItems.length === 0"
      type ="achado"
    />

    <div
      v-else
      class="grid grid-cols-[repeat(auto-fit,_minmax(180px,_1fr))] sm:grid-cols-[repeat(auto-fit,_minmax(200px,_1fr))] justify-items-center align-items-center lg:px-3 gap-y-3 pb-10"
    >
      <ItemCard
        v-for="item in foundItems"
        :key="item.id"
        :name="item.name"
        :location="item.location_name"
        :time="formatTime(item.created_at)"
        :image="item.image_urls?.[0] ?? NotAvailableImage"
        :id="item.id"
      />
    </div>

    <div v-if="foundItems.length" class="flex w-full justify-start sm:justify-center">
      <div class="bottom-32 ml-24 transform -translate-x-1/2 flex gap-4 z-10">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-10 text-azul hover:text-laranja transition duration-200 cursor-pointer"
          @click="goToPreviousPage"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="m11.25 9-3 3m0 0 3 3m-3-3h7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
          />
        </svg>

        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-10 text-azul hover:text-laranja transition duration-200 cursor-pointer"
          @click="goToNextPage"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="m12.75 15 3-3m0 0-3-3m3 3h-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
          />
        </svg>
      </div>
    </div>

    <ButtonAdd />
    <div class="fixed bottom-0 w-full">
      <MainMenu activeIcon="search" />
    </div>
  </div>
</template>

<script setup>
import MainMenu from "../components/Main-Menu.vue";
import ItemCard from "../components/Item-Card.vue";
import ButtonAdd from "../components/Button-Add-Found.vue";
import SearchHeader from "../components/Search-Header.vue";
import SubMenu from "../components/Sub-Menu-Found.vue";
import { ref, watch, onMounted } from "vue";
import { fetchFoundItems } from "@/services/apiItems";
import { formatTime } from "@/utils/dateUtils";
import NotAvailableImage from "@/assets/images/not-available.png";
import { filtersState } from "@/store/filters";
import EmptyState from "@/components/Empty-State.vue";

const foundItems = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const loading = ref(true);

const fetchItems = async (page = 1) => {
  try {
    loading.value = true;
    const { searchQuery, activeCategory, activeLocation } = filtersState;

    const response = await fetchFoundItems({
      page,
      search: searchQuery,
      category_name: activeCategory,
      location_name: activeLocation,
    });

    if (response.count !== undefined) {
      foundItems.value = response.results;
      totalPages.value = Math.ceil(response.count / 27);
    } else {
      console.error("Resposta da API inválida:", response);
    }
  } catch (error) {
    console.error("Erro ao buscar itens:", error);
  } finally {
    loading.value = false;
  }
};

const goToPreviousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value -= 1;
    fetchItems(currentPage.value);
  }
};

const goToNextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value += 1;
    fetchItems(currentPage.value);
  }
};

watch(
  () => [filtersState.searchQuery, filtersState.activeCategory, filtersState.activeLocation],
  () => {
    currentPage.value = 1;
    fetchItems();
  }
);

onMounted(() => fetchItems(currentPage.value));
</script>
