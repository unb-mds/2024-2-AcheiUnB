<template>
  <form id="app" @submit="save">
    <div class="grid md:grid-cols-4 gap-4">
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
          maxlength="750"
        />
      </div>

      <div class="block relative mb-4 col-span-2">
        <label for="category" class="font-inter block text-azul text-sm font-bold mb-2">
          Categoria <span class="text-red-500">*</span>
        </label>
        <div class="relative">
          <input
            type="text"
            v-model="searchCategory"
            placeholder="Pesquisar Categoria..."
            class="w-full border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
            @focus="showCategoryDropdown = true"
            @blur="hideDropdown('category')"
          />
          <div class="absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            <img
              src="../assets/icons/chevron-down.svg"
              alt="chevron-down"
              class="w-[15px] h-[15px] cursor-pointer"
              @click="showCategoryDropdown = !showCategoryDropdown"
            />
          </div>
          <ul
            v-if="showCategoryDropdown"
            class="absolute z-10 bg-white border rounded mt-1 w-full max-h-48 overflow-y-auto shadow-lg"
          >
            <li
              v-for="category in filteredCategories"
              :key="category.id"
              @mousedown="selectCategory(category)"
              class="px-3 py-2 hover:bg-gray-200 cursor-pointer"
            >
              {{ category.name }}
            </li>
          </ul>
        </div>
      </div>

      <div class="block relative mb-4 col-span-2">
        <label for="location" class="font-inter block text-azul text-sm font-bold mb-2 mt-4">
          Localização <span class="text-red-500">*</span>
        </label>
        <div class="relative">
          <input
            type="text"
            v-model="searchLocation"
            placeholder="Pesquisar Localização..."
            class="w-full border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
            @focus="showLocationDropdown = true"
            @blur="hideDropdown('location')"
          />
          <div class="absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            <img
              src="../assets/icons/chevron-down.svg"
              alt="chevron-down"
              class="w-[15px] h-[15px] cursor-pointer"
              @click="showLocationDropdown = !showLocationDropdown"
            />
          </div>
          <ul
            v-if="showLocationDropdown"
            class="absolute z-10 bg-white border rounded mt-1 w-full max-h-48 overflow-y-auto shadow-lg"
          >
            <li
              v-for="location in filteredLocations"
              :key="location.id"
              @mousedown="selectLocation(location)"
              class="px-3 py-2 hover:bg-gray-200 cursor-pointer"
            >
              {{ location.name }}
            </li>
          </ul>
        </div>
      </div>

      <div class="block relative mb-4 col-span-2">
        <label for="color" class="font-inter block text-azul text-sm font-bold mb-2 mt-4">
          Cor
        </label>
        <div class="relative">
          <input
            type="text"
            v-model="searchColor"
            placeholder="Pesquisar Cor..."
            class="w-full border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
            @focus="showColorDropdown = true"
            @blur="hideDropdown('color')"
          />
          <div class="absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            <img
              src="../assets/icons/chevron-down.svg"
              alt="chevron-down"
              class="w-[15px] h-[15px] cursor-pointer"
              @click="showColorDropdown = !showColorDropdown"
            />
          </div>
          <ul
            v-if="showColorDropdown"
            class="absolute z-10 bg-white border rounded mt-1 w-full max-h-48 overflow-y-auto shadow-lg"
          >
            <li
              v-for="color in filteredColors"
              :key="color.id"
              @mousedown="selectColor(color)"
              class="px-3 py-2 hover:bg-gray-200 cursor-pointer"
            >
              {{ color.name }}
            </li>
          </ul>
        </div>
      </div>

      <div class="block relative mb-4 col-span-2">
        <label for="brand" class="font-inter block text-azul text-sm font-bold mb-2 mt-4">
          Marca
        </label>
        <div class="relative">
          <input
            type="text"
            v-model="searchBrand"
            placeholder="Pesquisar Marca..."
            class="w-full border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
            @focus="showBrandDropdown = true"
            @blur="hideDropdown('brand')"
          />
          <div class="absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            <img
              src="../assets/icons/chevron-down.svg"
              alt="chevron-down"
              class="w-[15px] h-[15px] cursor-pointer"
              @click="showBrandDropdown = !showBrandDropdown"
            />
          </div>
          <ul
            v-if="showBrandDropdown"
            class="absolute z-10 bg-white border rounded mt-1 w-full max-h-48 overflow-y-auto shadow-lg"
          >
            <li
              v-for="brand in filteredBrands"
              :key="brand.id"
              @mousedown="selectBrand(brand)"
              class="px-3 py-2 hover:bg-gray-200 cursor-pointer"
            >
              {{ brand.name }}
            </li>
          </ul>
        </div>
      </div>

      <div class="mt-4 mb-4 col-span-2">
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
          :max="today"
        />
      </div>

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

      <div class="mb-4 col-span-2">
        <label for="description" class="font-inter block text-azul text-sm font-bold mb-2">
          Descrição
        </label>
        <textarea
          id="description"
          v-model="item.description"
          name="description"
          rows="4"
          maxlength="750"
          placeholder="Descreva detalhadamente o item"
          class="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        ></textarea>
      </div>

      <div>
        <label
          for="images"
          class="flex bg-azul text-white text-base px-5 py-3 outline-none rounded cursor-pointer font-inter"
          :class="previews?.length > 1 ? 'opacity-50 cursor-not-allowed' : ''"
        >
          <img src="../assets/icons/add-item-white.svg" alt="" class="mr-2" />
          Adicionar imagens
          <input
            type="file"
            ref="fileInput"
            id="images"
            class="hidden"
            @change="onFileChange"
            :disabled="previews?.length > 1"
          />
        </label>
      </div>

      <div class="flex flex-wrap gap-4 col-span-3">
        <div
          v-for="(image, index) in previews"
          :key="index"
          class="w-64 h-64 border rounded relative"
        >
          <!-- Imagem de Pré-visualização -->
          <img :src="image" alt="Preview" class="w-full h-full object-cover rounded" />

          <div
            class="absolute p-1 bottom-2 border-2 border-laranja right-2 w-12 h-12 bg-white flex items-center justify-center text-xs rounded-full cursor-pointer"
            @click="removeImage(index)"
          >
            <img src="../assets/icons/trash.svg" alt="" />
          </div>
        </div>
      </div>
      <div class="col-span-4 flex justify-center mt-4">
        <button
          type="button"
          @click="save"
          :disabled="isSubmitting || formSubmitted"
          class="inline-block text-center rounded-full bg-laranja px-6 py-4 text-md font-bold text-white w-full md:w-1/2 lg:w-1/3 transition-all hover:bg-opacity-90 hover:scale-105 hover:shadow-lg shadow-md border-2 border-laranja border-opacity-80 disabled:opacity-50 disabled:cursor-not-allowed transform-gpu"
        >
          <span class="flex items-center justify-center">
            <svg v-if="isSubmitting" class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-lg">{{ isSubmitting ? "Enviando..." : (editMode ? "Salvar Alterações" : "Enviar") }}</span>
          </span>
        </button>
      </div>
    </div>
  </form>

  <Alert v-if="submitError" type="error" :message="alertMessage" @closed="submitError = false" />

  <Alert
    v-if="formSubmitted"
    type="success"
    :message="editMode ? 'Item editado com sucesso' : 'Item publicado com sucesso'"
    @closed="formSubmitted = false"
  />
</template>

<script>
import Form from "../models/Form";
import Item from "../models/Item";
import Alert from "./Alert.vue";
import api from "../services/api";

export default {
  name: "FormComponent",
  data() {
    return {
      item: new Item(),
      foundTime: "",
      foundDate: "",
      today: new Date().toISOString().split("T")[0],
      previews: [],
      imagesToRemove: [],
      submitError: false,
      formSubmitted: false,
      alertMessage: "",
      isSubmitting: false,

      categories: [
        {
          id: 1,
          name: "Anel",
          category_id: "01",
        },
        {
          id: 2,
          name: "Anotações",
          category_id: "02",
        },
        {
          id: 3,
          name: "Apostila",
          category_id: "03",
        },
        {
          id: 4,
          name: "Base",
          category_id: "04",
        },
        {
          id: 5,
          name: "Batom",
          category_id: "05",
        },
        {
          id: 6,
          name: "Blusa",
          category_id: "06",
        },
        {
          id: 7,
          name: "Blush",
          category_id: "07",
        },
        {
          id: 8,
          name: "Boné",
          category_id: "08",
        },
        {
          id: 9,
          name: "Borracha",
          category_id: "09",
        },
        {
          id: 10,
          name: "Brinco",
          category_id: "10",
        },
        {
          id: 11,
          name: "Caderno",
          category_id: "11",
        },
        {
          id: 12,
          name: "Calculadora",
          category_id: "12",
        },
        {
          id: 13,
          name: "Calculadora Científica",
          category_id: "13",
        },
        {
          id: 14,
          name: "Camiseta",
          category_id: "14",
        },
        {
          id: 15,
          name: "Caneta",
          category_id: "15",
        },
        {
          id: 16,
          name: "Carregador",
          category_id: "16",
        },
        {
          id: 17,
          name: "Carregador Portátil",
          category_id: "17",
        },
        {
          id: 18,
          name: "Carteira",
          category_id: "18",
        },
        {
          id: 19,
          name: "Carteira de Identidade",
          category_id: "19",
        },
        {
          id: 20,
          name: "Carteira de Motorista",
          category_id: "20",
        },
        {
          id: 21,
          name: "Cartão SUS",
          category_id: "21",
        },
        {
          id: 22,
          name: "Casaco",
          category_id: "22",
        },
        {
          id: 23,
          name: "Case Fone",
          category_id: "23",
        },
        {
          id: 24,
          name: "Case Notebook",
          category_id: "24",
        },
        {
          id: 25,
          name: "Celular",
          category_id: "25",
        },
        {
          id: 26,
          name: "Chapéu",
          category_id: "26",
        },
        {
          id: 27,
          name: "Chaves",
          category_id: "27",
        },
        {
          id: 28,
          name: "Chinelo",
          category_id: "28",
        },
        {
          id: 29,
          name: "Colar",
          category_id: "29",
        },
        {
          id: 30,
          name: "Estojo",
          category_id: "30",
        },
        {
          id: 31,
          name: "Fone de ouvido",
          category_id: "31",
        },
        {
          id: 32,
          name: "Garrafa de Água",
          category_id: "32",
        },
        {
          id: 33,
          name: "Gloss",
          category_id: "33",
        },
        {
          id: 34,
          name: "Grampeador",
          category_id: "34",
        },
        {
          id: 35,
          name: "Guarda-chuva",
          category_id: "35",
        },
        {
          id: 36,
          name: "Lapizeira",
          category_id: "36",
        },
        {
          id: 37,
          name: "Livro",
          category_id: "37",
        },
        {
          id: 38,
          name: "Lápis",
          category_id: "38",
        },
        {
          id: 39,
          name: "Lápis de olho",
          category_id: "39",
        },
        {
          id: 40,
          name: "Mochila",
          category_id: "40",
        },
        {
          id: 41,
          name: "Mouse",
          category_id: "41",
        },
        {
          id: 42,
          name: "Nessesair",
          category_id: "42",
        },
        {
          id: 43,
          name: "Notebook",
          category_id: "43",
        },
        {
          id: 44,
          name: "Passe Estudantil",
          category_id: "44",
        },
        {
          id: 45,
          name: "Passe de Ônibus",
          category_id: "45",
        },
        {
          id: 46,
          name: "Piercing",
          category_id: "46",
        },
        {
          id: 47,
          name: "Pingente",
          category_id: "47",
        },
        {
          id: 48,
          name: "Planner",
          category_id: "48",
        },
        {
          id: 49,
          name: "Presilha de Cabelo",
          category_id: "49",
        },
        {
          id: 50,
          name: "Pulseira",
          category_id: "50",
        },
        {
          id: 51,
          name: "Relógio",
          category_id: "51",
        },
        {
          id: 52,
          name: "Smartwatch",
          category_id: "52",
        },
        {
          id: 53,
          name: "Sombra",
          category_id: "53",
        },
        {
          id: 54,
          name: "Stylus",
          category_id: "54",
        },
        {
          id: 55,
          name: "Suporte Notebook",
          category_id: "55",
        },
        {
          id: 56,
          name: "Tablet",
          category_id: "56",
        },
        {
          id: 57,
          name: "Touca",
          category_id: "57",
        },
        {
          id: 58,
          name: "Óculos",
          category_id: "58",
        },
        {
          id: 59,
          name: "Outra",
          category_id: "00",
        },
      ],
      locations: [
        {
          id: 1,
          name: "Anfiteatro - UAC",
          location_id: "01",
        },
        {
          id: 2,
          name: "Banheiros - LDTEA",
          location_id: "02",
        },
        {
          id: 3,
          name: "Banheiros - RU",
          location_id: "03",
        },
        {
          id: 4,
          name: "Banheiros - UAC",
          location_id: "04",
        },
        {
          id: 5,
          name: "Banheiros - UED",
          location_id: "05",
        },
        {
          id: 6,
          name: "Bebedouros - UAC",
          location_id: "06",
        },
        {
          id: 7,
          name: "Bebedouros - UED",
          location_id: "07",
        },
        {
          id: 8,
          name: "Biblioteca - UAC",
          location_id: "08",
        },
        {
          id: 9,
          name: "Box - RU",
          location_id: "09",
        },
        {
          id: 10,
          name: "Caixa - RU",
          location_id: "10",
        },
        {
          id: 11,
          name: "Diretório Acadêmico - DA",
          location_id: "11",
        },
        {
          id: 12,
          name: "Estacionamento - LDTEA",
          location_id: "12",
        },
        {
          id: 13,
          name: "Estacionamento - UAC",
          location_id: "13",
        },
        {
          id: 14,
          name: "Estacionamento - UED",
          location_id: "14",
        },
        {
          id: 15,
          name: "Guarita Estacionamento Norte",
          location_id: "15",
        },
        {
          id: 16,
          name: "Guarita Estacionamento Sul",
          location_id: "16",
        },
        {
          id: 17,
          name: "I1 - UAC",
          location_id: "17",
        },
        {
          id: 18,
          name: "I10 - UAC",
          location_id: "18",
        },
        {
          id: 19,
          name: "I2 - UAC",
          location_id: "19",
        },
        {
          id: 20,
          name: "I3 - UAC",
          location_id: "20",
        },
        {
          id: 21,
          name: "I4 - UAC",
          location_id: "21",
        },
        {
          id: 22,
          name: "I5 - UAC",
          location_id: "22",
        },
        {
          id: 23,
          name: "I6 - UAC",
          location_id: "23",
        },
        {
          id: 24,
          name: "I7 - UAC",
          location_id: "24",
        },
        {
          id: 25,
          name: "I8 - UAC",
          location_id: "25",
        },
        {
          id: 26,
          name: "I9 - UAC",
          location_id: "26",
        },
        {
          id: 27,
          name: "Jardim - RU",
          location_id: "27",
        },
        {
          id: 28,
          name: "Jardim - UAC",
          location_id: "28",
        },
        {
          id: 29,
          name: "LDTEA",
          location_id: "29",
        },
        {
          id: 30,
          name: "Laboratórios - LDTEA",
          location_id: "30",
        },
        {
          id: 31,
          name: "Laboratórios - UED",
          location_id: "31",
        },
        {
          id: 32,
          name: "Mesa de estudos - UED",
          location_id: "32",
        },
        {
          id: 33,
          name: "Mesanino - UAC",
          location_id: "33",
        },
        {
          id: 34,
          name: "Mesanino - UED",
          location_id: "34",
        },
        {
          id: 35,
          name: "Mesas - RU",
          location_id: "35",
        },
        {
          id: 36,
          name: "Mesas O Belisco - UAC",
          location_id: "36",
        },
        {
          id: 37,
          name: "Mesas Redondas - UED",
          location_id: "37",
        },
        {
          id: 38,
          name: "Mesas de Dama - UAC",
          location_id: "38",
        },
        {
          id: 39,
          name: "Mesas de Estudos - UAC",
          location_id: "39",
        },
        {
          id: 40,
          name: "Mocap - UED",
          location_id: "40",
        },
        {
          id: 41,
          name: "Monumento lado ru",
          location_id: "41",
        },
        {
          id: 42,
          name: "Quadra Poliesportiva",
          location_id: "42",
        },
        {
          id: 43,
          name: "RU",
          location_id: "43",
        },
        {
          id: 44,
          name: "Restaurante - RU",
          location_id: "44",
        },
        {
          id: 45,
          name: "S1 - UAC",
          location_id: "45",
        },
        {
          id: 46,
          name: "S10 - UAC",
          location_id: "46",
        },
        {
          id: 47,
          name: "S2 - UAC",
          location_id: "47",
        },
        {
          id: 48,
          name: "S3 - UAC",
          location_id: "48",
        },
        {
          id: 49,
          name: "S4 - UAC",
          location_id: "49",
        },
        {
          id: 50,
          name: "S5 - UAC",
          location_id: "50",
        },
        {
          id: 51,
          name: "S6 - UAC",
          location_id: "51",
        },
        {
          id: 52,
          name: "S7 - UAC",
          location_id: "52",
        },
        {
          id: 53,
          name: "S8 - UAC",
          location_id: "53",
        },
        {
          id: 54,
          name: "S9 - UAC",
          location_id: "54",
        },
        {
          id: 55,
          name: "Sala de Professor - UED",
          location_id: "55",
        },
        {
          id: 56,
          name: "UAC",
          location_id: "56",
        },
        {
          id: 57,
          name: "UED",
          location_id: "57",
        },
        {
          id: 58,
          name: "Outro",
          location_id: "00",
        },
      ],
      colors: [
        {
          id: 1,
          name: "Amarelo",
          color_id: "01",
        },
        {
          id: 2,
          name: "Azul",
          color_id: "02",
        },
        {
          id: 3,
          name: "Bege",
          color_id: "03",
        },
        {
          id: 4,
          name: "Branco",
          color_id: "04",
        },
        {
          id: 5,
          name: "Bronze",
          color_id: "05",
        },
        {
          id: 6,
          name: "Cinza",
          color_id: "06",
        },
        {
          id: 7,
          name: "Dourado",
          color_id: "07",
        },
        {
          id: 8,
          name: "Estampado",
          color_id: "08",
        },
        {
          id: 9,
          name: "Laranja",
          color_id: "09",
        },
        {
          id: 10,
          name: "Marrom",
          color_id: "10",
        },
        {
          id: 11,
          name: "Prata",
          color_id: "11",
        },
        {
          id: 12,
          name: "Preto",
          color_id: "12",
        },
        {
          id: 13,
          name: "Rosa",
          color_id: "13",
        },
        {
          id: 14,
          name: "Verde",
          color_id: "14",
        },
        {
          id: 15,
          name: "Vermelho",
          color_id: "15",
        },
        {
          id: 16,
          name: "Outra",
          color_id: "00",
        },
      ],
      brands: [
        {
          id: 1,
          name: "Acer",
          brand_id: "01",
        },
        {
          id: 2,
          name: "Adidas",
          brand_id: "02",
        },
        {
          id: 3,
          name: "Apple",
          brand_id: "03",
        },
        {
          id: 4,
          name: "Asus",
          brand_id: "04",
        },
        {
          id: 5,
          name: "Avon",
          brand_id: "05",
        },
        {
          id: 6,
          name: "Bic",
          brand_id: "06",
        },
        {
          id: 7,
          name: "Dell",
          brand_id: "07",
        },
        {
          id: 8,
          name: "Dior",
          brand_id: "08",
        },
        {
          id: 9,
          name: "FCTE",
          brand_id: "09",
        },
        {
          id: 10,
          name: "FGA",
          brand_id: "10",
        },
        {
          id: 11,
          name: "HP",
          brand_id: "11",
        },
        {
          id: 12,
          name: "Havaianas",
          brand_id: "12",
        },
        {
          id: 13,
          name: "Hay-Ban",
          brand_id: "13",
        },
        {
          id: 14,
          name: "Huawei",
          brand_id: "14",
        },
        {
          id: 15,
          name: "JBL",
          brand_id: "15",
        },
        {
          id: 16,
          name: "Kingston",
          brand_id: "16",
        },
        {
          id: 17,
          name: "LG",
          brand_id: "17",
        },
        {
          id: 18,
          name: "Lenovo",
          brand_id: "18",
        },
        {
          id: 19,
          name: "Levi's",
          brand_id: "19",
        },
        {
          id: 20,
          name: "Motorola",
          brand_id: "20",
        },
        {
          id: 21,
          name: "New Balance",
          brand_id: "21",
        },
        {
          id: 22,
          name: "Nike",
          brand_id: "22",
        },
        {
          id: 23,
          name: "Nokia",
          brand_id: "23",
        },
        {
          id: 24,
          name: "O Boticário",
          brand_id: "24",
        },
        {
          id: 25,
          name: "Oakley",
          brand_id: "25",
        },
        {
          id: 26,
          name: "Puma",
          brand_id: "26",
        },
        {
          id: 27,
          name: "RRDD",
          brand_id: "27",
        },
        {
          id: 28,
          name: "Razer",
          brand_id: "28",
        },
        {
          id: 29,
          name: "Samsung",
          brand_id: "29",
        },
        {
          id: 30,
          name: "SanDisk",
          brand_id: "30",
        },
        {
          id: 31,
          name: "Sony",
          brand_id: "31",
        },
        {
          id: 32,
          name: "Stanley",
          brand_id: "32",
        },
        {
          id: 33,
          name: "Tapaware",
          brand_id: "33",
        },
        {
          id: 34,
          name: "Toshiba",
          brand_id: "34",
        },
        {
          id: 35,
          name: "UnB",
          brand_id: "35",
        },
        {
          id: 36,
          name: "Vaio",
          brand_id: "36",
        },
        {
          id: 37,
          name: "Vans",
          brand_id: "37",
        },
        {
          id: 38,
          name: "Xiaomi",
          brand_id: "38",
        },
        {
          id: 39,
          name: "Outra",
          brand_id: "00",
        },
      ],
      searchCategory: "",
      searchLocation: "",
      searchBrand: "",
      searchColor: "",
      showCategoryDropdown: false,
      showLocationDropdown: false,
      showBrandDropdown: false,
      showColorDropdown: false,
    };
  },
  props: {
    editMode: {
      type: Boolean,
      default: false,
    },
    existingItem: {
      type: Object,
      default: null,
    },
  },
  mounted() {
    if (this.editMode && this.existingItem) {
      this.item = Object.assign(new Item(), this.existingItem);
      this.previews.push(...this.existingItem.image_urls);

      if (this.item.category) {
        const cat = this.categories.find(c => c.category_id == this.item.category || c.id == this.item.category);
        if (cat) this.searchCategory = cat.name;
      }
      if (this.item.location) {
        const loc = this.locations.find(l => l.location_id == this.item.location || l.id == this.item.location);
        if (loc) this.searchLocation = loc.name;
      }
      if (this.item.brand) {
        const brand = this.brands.find(b => b.brand_id == this.item.brand || b.id == this.item.brand);
        if (brand) this.searchBrand = brand.name;
      }
      if (this.item.color) {
        const color = this.colors.find(c => c.color_id == this.item.color || c.id == this.item.color);
        if (color) this.searchColor = color.name;
      }

      if (this.item.found_lost_date) {
        try {
          const date = new Date(this.item.found_lost_date);
          this.item.foundDate =
            date.getFullYear() +
            "-" +
            String(date.getMonth() + 1).padStart(2, "0") +
            "-" +
            String(date.getDate()).padStart(2, "0");
          this.foundTime =
            String(date.getHours()).padStart(2, "0") +
            ":" +
            String(date.getMinutes()).padStart(2, "0");
        } catch (error) {
          console.error("Erro ao processar found_lost_date:", error);
          this.alertMessage = "Erro ao processar data.";
          this.submitError = true;
        }
      }
    }
  },
  computed: {
    filteredCategories() {
      return this.categories.filter((category) =>
        category.name.toLowerCase().includes(this.searchCategory.toLowerCase()),
      );
    },
    filteredLocations() {
      return this.locations.filter((location) =>
        location.name.toLowerCase().includes(this.searchLocation.toLowerCase()),
      );
    },
    filteredBrands() {
      return this.brands.filter((brand) =>
        brand.name.toLowerCase().includes(this.searchBrand.toLowerCase()),
      );
    },
    filteredColors() {
      return this.colors.filter((color) =>
        color.name.toLowerCase().includes(this.searchColor.toLowerCase()),
      );
    },
  },
  methods: {
    async initializeCategories() {
      try {
        const result = await api.get("/categories/");
        this.categories = result.data.results;
      } catch {
        console.log("Erro ao carregar categorias");
        this.alertMessage = "Erro ao carregar categorias.";
        this.submitError = true;
      }
    },

    async initializeLocations() {
      try {
        const result = await api.get("/locations/");
        this.locations = result.data.results;
      } catch {
        console.log("Erro ao carregar locais");
        this.alertMessage = "Erro ao carregar locais.";
        this.submitError = true;
      }
    },

    async initializeColors() {
      try {
        const result = await api.get("/colors/");
        this.colors = result.data.results;
      } catch {
        console.log("Erro ao carregar cores");
        this.alertMessage = "Erro ao carregar cores.";
        this.submitError = true;
      }
    },

    async initializeBrands() {
      try {
        const result = await api.get("/brands/");
        this.brands = result.data.results;
      } catch {
        console.log("Erro ao carregar marcas");
        this.alertMessage = "Erro ao carregar marcas.";
        this.submitError = true;
      }
    },
    async save() {
    if (this.isSubmitting) return;
        this.isSubmitting = true;
        this.alertMessage = '';
        this.submitError = false;

      this.item.status = "found";
      const form = new Form(this.item);

      if (!form.validate()) {
        this.alertMessage = "Verifique os campos marcados com *.";
        this.submitError = true;
        this.isSubmitting = false
        return;
      }

      if (this.item.foundDate) {
        // Cria a data/hora completa combinando data e hora
        const [year, month, day] = this.item.foundDate.split("-").map(Number);
        const timeValue = this.foundTime?.trim();
        const [hours, minutes] = timeValue && timeValue !== '' 
          ? timeValue.split(":").map(Number) 
          : [0, 0];
        
        const selectedDateTime = new Date(year, month - 1, day, hours, minutes, 0, 0);
        const currentDateTime = new Date();
        
        // Valida se a data/hora selecionada é futura
        if (selectedDateTime > currentDateTime) {
          this.alertMessage = "Ops! Não é possível selecionar uma data e hora no futuro.";
          this.submitError = true;
          this.isSubmitting = false;
          return;
        }
        
        const formattedFoundLostDate = this.formatFoundLostDate();
        form.setFieldValue("found_lost_date", formattedFoundLostDate);
      }

      const formData = form.toFormData();

      if (this.imagesToRemove.length > 0) {
        this.imagesToRemove.forEach((id) => formData.append("remove_images", id));
      }

      try {
        if (this.editMode) {
          if (this.item.images?.length > 0) {
            this.item.images.forEach((image) => {
              formData.append("images", image);
            });
          }

          await api.patch(`/items/${this.item.id}/`, formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });

          this.formSubmitted = true;

          /*for (let pair of formData.entries()) {
            console.log(pair[0], pair[1]);
          }*/

        } else {
          await api.post("/items/", formData);
          this.formSubmitted = true;
        }
        setTimeout(() => {
          window.location.replace(`${import.meta.env.VITE_URL_PROD}/#/found`);
        }, 2050);
      } catch (error) {
        this.alertMessage = "Erro ao publicar item.";
        this.submitError = true;
      }
      finally {
        this.isSubmitting = false;
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
      if (this.existingItem && index < (this.existingItem.image_urls?.length || 0)) {
        this.imagesToRemove.push(this.existingItem.image_ids[index]);
        if (this.imagesToRemove.length > 0) {
          // Remove a imagem dos arrays de imagens existentes
          this.existingItem.image_urls?.splice(index, 1);
          this.existingItem.image_ids.splice(index, 1);
        }
      } else {
        // Imagem nova (ainda não foi enviada para a API)
        const newIndex = index - (this.existingItem?.image_urls?.length || 0);
        this.item.images.splice(newIndex, 1);
      }

      this.previews.splice(index, 1);

      this.$forceUpdate();
      this.$refs.fileInput.value = "";
    },

    handleSelectChange(event) {
      const element = event.target;

      if (element.value == "clear") {
        this.item[`${element.id}`] = "";
      }
    },

    selectCategory(category) {
      this.item.category = category.id;
      this.searchCategory = category.name;
      this.showCategoryDropdown = false;
    },

    selectLocation(location) {
      this.item.location = location.id;
      this.searchLocation = location.name;
      this.showLocationDropdown = false;
    },

    selectBrand(brand) {
      this.item.brand = brand.id;
      this.searchBrand = brand.name;
      this.showBrandDropdown = false;
    },

    selectColor(color) {
      this.item.color = color.id;
      this.searchColor = color.name;
      this.showBrandDropdown = false;
    },

    hideDropdown(field) {
      setTimeout(() => {
        if (field === "category") this.showCategoryDropdown = false;
        if (field === "location") this.showLocationDropdown = false;
        if (field === "brand") this.showBrandDropdown = false;
        if (field === "color") this.showColorDropdown = false;
      }, 100);
    },
  },
};
</script>

<style scoped></style>
