<template>
  <div class="flex flex-col items-center justify-center h-64 text-center">
    <img :src="box" class="w-20 h-20 mb-4 opacity-15" />
    <p class="text-cinza3 font-inter text-lg">
      Parece que o <span class="text-azul font-bold">AcheiUnB</span> {{ computedMessage }}
    </p>
  </div>
</template>

<script setup>
import { computed, toRefs } from "vue";
import { filtersState } from "@/store/filters";
import box from "@/assets/icons/box.svg";

const props = defineProps({
  type: {
    type: String,
    required: true,
  },
});

const { searchQuery, activeCategory, activeLocation } = toRefs(filtersState);

const computedMessage = computed(() => {
  const itemType = props.type === "achado" ? "achado" : "perdido";

  if (searchQuery.value != "") {
    return `não encontrou resultados para "${searchQuery.value}" nos itens ${itemType}s.`;
  }
  if (activeCategory.value != null) {
    return `não encontrou itens ${itemType}s da categoria "${activeCategory.value}".`;
  }
  if (activeLocation.value != null) {
    return `não encontrou itens ${itemType}s no local "${activeLocation.value}".`;
  }

  return `está sem itens ${itemType}s... Você pode adicionar um!`;
});
</script>
