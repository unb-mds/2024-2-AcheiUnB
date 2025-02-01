<template>
  <div
    class="w-[170px] sm:w-[190px] h-[230px] bg-cinza1 rounded-sm shadow-complete p-2 flex flex-col relative z-0 cursor-pointer"
    @click="viewItemDetails()"
  >
    <div class="w-full h-[120px] bg-cinza2 rounded-sm flex justify-center items-start">
      <img :src="image" class="rounded-sm w-full h-full max-w-full max-h-full object-cover" />
    </div>

    <button
      v-if="isMyItem"
      class="absolute p-1 bottom-2 border-2 border-laranja right-2 w-10 h-10 bg-white flex items-center justify-center text-xs rounded-full cursor-pointer"
      @click.stop="$emit('delete', id)"
    >
      <img src="../assets/icons/trash.svg" alt="Excluir" />
    </button>

    <div class="h-[2px] w-1/4 bg-laranja mt-4"></div>

    <div class="text-azul font-bold font-inter mt-1 truncate">{{ name }}</div>
    <div class="flex items-start">
      <img src="../assets/icons/locale.svg" alt="" class="w-[15px] h-[15px] mr-1" />
      <div class="text-azul font-inter text-sm">{{ location }}</div>
    </div>

    <span
      class="text-right font-inter font-bold text-xs text-cinza3 p-1 flex justify-end items-center"
    >
      <template v-if="!isMyItem">
        {{ time }}
      </template>
    </span>
  </div>
</template>

<script>
export default {
  name: "ItemCard",
  props: {
    id: Number,
    image: String,
    name: String,
    time: String,
    location: String,
    isMyItem: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    viewItemDetails() {
      this.$router.push({ name: "ListItem", query: { idItem: this.id } });
    },
  },
  methods: {
    viewItemDetails() {
      this.$router.push({ name: "ListItem", query: { idItem: this.id } });
    },
  },
};
</script>

<style scoped></style>
