<template>
  <form id="app" @submit="save">
    <div class="grid md:grid-cols-4 gap-4">
      <!-- Nome do item -->
      <div class="mb-4 col-span-2">
        <label for="name" class="font-inter block text-azul text-sm font-bold mb-2"
          >Item <span class="text-red-500">*</span></label
        >
        <input
          id="name"
          class="appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          v-model="item.name"
          type="text"
          name="name"
          placeholder="Escreva o nome do item"
        />
      </div>

      <!-- Categoria -->
      <div class="block relative mb-4 col-span-2">
        <label for="category" class="font-inter block text-azul text-sm font-bold mb-2"
          >Categoria <span class="text-red-500">*</span></label
        >
        <select
          id="category"
          class="appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
          :class="item.category === '' ? 'text-gray-400' : 'text-gray-700'"
          v-model="item.category"
          @change="handleSelectChange"
          name="category"
        >
          <option disabled value="">Selecione</option>
          <option value="clear">Limpar seleção</option>
          <option
            v-for="category of categories"
            :key="category.id"
            :value="category.id"
            class="block text-gray-700"
          >
            {{ category.name }}
          </option>
        </select>
        <div
          class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 mt-6"
        >
          <img
            src="../assets/icons/chevron-down.svg"
            alt="chevron-down"
            class="w-[15px] h-[15px]"
          />
        </div>
      </div>

      <!-- Location -->
      <div class="block relative mb-4 col-span-2">
        <label for="location" class="font-inter block text-azul text-sm font-bold mb-2"
          >Local <span class="text-red-500">*</span></label
        >
        <select
          id="location"
          class="appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
          :class="item.location === '' ? 'text-gray-400' : 'text-gray-700'"
          v-model="item.location"
          @change="handleSelectChange"
          name="location"
        >
          <option value="" disabled selected>Selecione</option>
          <option value="clear">Limpar seleção</option>
          <option
            v-for="location of locations"
            :key="location.id"
            :value="location.id"
            class="block text-gray-700"
          >
            {{ location.name }}
          </option>
        </select>
        <div
          class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 mt-6"
        >
          <img
            src="../assets/icons/chevron-down.svg"
            alt="chevron-down"
            class="w-[15px] h-[15px]"
          />
        </div>
      </div>

      <!-- Color -->
      <div class="block relative mb-4 col-span-2">
        <label for="color" class="font-inter block text-azul text-sm font-bold mb-2">Cor</label>
        <select
          id="color"
          class="appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
          :class="item.color === '' ? 'text-gray-400' : 'text-gray-700'"
          v-model="item.color"
          @change="handleSelectChange"
          name="color"
        >
          <option value="" disabled selected>Selecione</option>
          <option value="clear">Limpar seleção</option>
          <option
            v-for="color of colors"
            :key="color.id"
            :value="color.id"
            class="block text-gray-700"
          >
            {{ color.name }}
          </option>
        </select>
        <div
          class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 mt-6"
        >
          <img
            src="../assets/icons/chevron-down.svg"
            alt="chevron-down"
            class="w-[15px] h-[15px] fill-current text-white"
          />
        </div>
      </div>

      <!-- Brand -->
      <div class="block relative mb-4 col-span-2">
        <label for="color" class="font-inter block text-azul text-sm font-bold mb-2">Marca</label>
        <select
          id="brand"
          class="appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
          :class="item.brand === '' ? 'text-gray-400' : 'text-gray-700'"
          v-model="item.brand"
          @change="handleSelectChange"
          name="color"
        >
          <option value="" disabled selected>Selecione</option>
          <option value="clear">Limpar seleção</option>
          <option
            v-for="brand of brands"
            :key="brand.id"
            :value="brand.id"
            class="block text-gray-700"
          >
            {{ brand.name }}
          </option>
        </select>
        <div
          class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 mt-6"
        >
          <img
            src="../assets/icons/chevron-down.svg"
            alt="chevron-down"
            class="w-[15px] h-[15px] fill-current text-white"
          />
        </div>
      </div>

      <!-- Data -->
      <div class="mb-4 col-span-2">
        <label for="foundDate" class="font-inter block text-azul text-sm font-bold mb-2"
          >Data em que foi achado</label
        >
        <input
          id="foundDate"
          class="appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
          :class="item.foundDate === '' ? 'text-gray-400' : 'text-gray-700'"
          v-model="item.foundDate"
          type="date"
          name="foundDate"
        />
      </div>

      <!-- Horário -->
      <div class="mb-4 col-span-2">
        <label for="foundTime" class="font-inter block text-azul text-sm font-bold mb-2"
          >Horário em que foi achado</label
        >
        <input
          id="foundTime"
          class="appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
          :class="foundTime === '' ? 'text-gray-400' : 'text-gray-700'"
          v-model="foundTime"
          type="time"
          name="foundTime"
        />
      </div>

      <!-- Descrição -->
      <div class="mb-4 col-span-2">
        <label for="description" class="font-inter block text-azul text-sm font-bold mb-2">
          Descrição
        </label>
        <textarea
          id="description"
          v-model="item.description"
          name="description"
          rows="4"
          placeholder="Descreva detalhadamente o item"
          class="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        ></textarea>
      </div>

      <div>
        <!-- Upload de arquivo -->
        <label
          for="images"
          class="flex bg-azul text-white text-base px-5 py-3 outline-none rounded cursor-pointer font-inter"
          :class="item.images?.length > 1 ? 'opacity-50 cursor-not-allowed' : ''"
        >
          <img src="../assets/icons/add-item-white.svg" alt="" class="mr-2" />
          Adicionar imagens
          <input
            type="file"
            id="images"
            class="hidden"
            @change="onFileChange"
            :disabled="item.images?.length > 1"
          />
        </label>
      </div>

      <div class="flex flex-wrap gap-4 col-span-3">
        <!-- Loop de Imagens -->
        <div
          v-for="(image, index) in previews"
          :key="index"
          class="w-64 h-64 border rounded relative"
        >
          <!-- Imagem de Pré-visualização -->
          <img :src="image" alt="Preview" class="w-full h-full object-cover rounded" />

          <!-- Botão Remover -->
          <div
            class="absolute p-1 bottom-2 border-2 border-laranja right-2 w-12 h-12 bg-white flex items-center justify-center text-xs rounded-full cursor-pointer"
            @click="removeImage(index)"
          >
            <img src="../assets/icons/trash.svg" alt="" />
          </div>
        </div>
      </div>

      <!-- Enviar -->
      <div class="col-span-4">
        <button
          type="button"
          @click="save"
          class="inline-block text-center rounded-full bg-laranja px-5 py-3 text-md text-white w-full"
        >
          Enviar
        </button>
      </div>
    </div>
  </form>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />

  <Alert
    v-if="formSubmitted"
    type="success"
    message="Item publicado com sucesso"
    @closed="formSubmitted = false"
  />
</template>

<script>
import { fetchCategories } from "@/services/category-api";
import Form from "../models/Form";
import Item from "../models/Item";
import { fetchLocations } from "@/services/location-api";
import { fetchColors } from "@/services/color-api";
import { fetchBrands } from "@/services/brand-api";
import { saveItem } from "@/services/item-api";

export default {
  name: "FormComponent",
  data() {
    return {
      item: new Item(),
      foundTime: "",
      foundDate: "",
      previews: [],
      submitError: false,
      formSubmitted: false,
      alertMessage: "",
      categories: [],
      locations: [],
      colors: [],
      brands: [],
    };
  },
  mounted() {
    this.initializeData();
  },
  methods: {
    initializeData() {
      this.initializeCategories();
      this.initializeLocations();
      this.initializeColors();
      this.initializeBrands();
    },

    async initializeCategories() {
      this.categories = await fetchCategories();
    },

    async initializeLocations() {
      this.locations = await fetchLocations();
    },

    async initializeColors() {
      this.colors = await fetchColors();
    },

    async initializeBrands() {
      this.brands = await fetchBrands();
    },

    async save() {
      this.item.status = "found";

      const form = new Form(this.item);

      if (!form.validate()) {
        this.alertMessage = "Verifique os campos marcados com *.";
        this.submitError = true;
        return;
      }

      if (this.item.foundDate) {
        const formattedFoundLostDate = this.formatFoundLostDate();
        form.setFieldValue("found_lost_date", formattedFoundLostDate);
      }

      const formData = form.toFormData();
      try {
        await saveItem(formData);
        this.formSubmitted = true;

        setTimeout(() => {
          router.push({ name: "Found" });
        }, 1000);
      } catch (error) {
        this.alertMessage = "Erro ao publicar item.";
        this.submitError = true;
      }
    },

    onFileChange(event) {
      if (!this.item.images) {
        this.item.images = [];
      }

      const files = Array.from(event.target.files);
      this.item.images.push(...files);

      files.forEach((file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.previews.push(e.target.result);
        };
        reader.readAsDataURL(file);
      });
    },

    formatFoundLostDate() {
      const [year, month, day] = this.item.foundDate.split("-").map(Number);

      const [hours, minutes] = this.foundTime?.split(":").map(Number);

      const date = new Date(year, month - 1, day, hours ?? 0, minutes ?? 0);

      const timezoneOffset = date.getTimezoneOffset();
      const sign = timezoneOffset > 0 ? "-" : "+";
      const offset = Math.abs(timezoneOffset);
      const offsetHours = String(Math.floor(offset / 60)).padStart(2, "0");
      const offsetMinutes = String(offset % 60).padStart(2, "0");

      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}T${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}:${String(date.getSeconds()).padStart(2, "0")}${sign}${offsetHours}${offsetMinutes}`;
    },

    removeImage(index) {
      this.previews.splice(index, 1);
      this.item.images.splice(index, 1);
    },

    handleSelectChange(event) {
      const element = event.target;

      if (element.value == "clear") {
        this.item[`${element.id}`] = "";
      }
    },
  },
};
</script>

<style scoped></style>
