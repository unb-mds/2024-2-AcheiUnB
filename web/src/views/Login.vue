<template>
  <div id="transition-screen" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="fixed inset-0 flex items-center justify-center z-50">
      <Logo customClass="text-azul" />
    </div>
  </div>

  <div
    id="main-content"
    class="flex flex-col lg:flex-row bg-azul text-white p-4 min-h-screen hidden"
  >
    <div>
      <div class="titulo flex space-x-1 mt-20 mb-16 ml-12 md:ml-0 md:flex md:ml-12 md:mb-24">
        <Logo />
      </div>
      <div class="slogan max-w-72 ml-12 md:mr-8 md:max-w-none md:w-auto">
        <p class="text-5xl font-bold mb-7 md:text-5xl fade-in">Perdeu algo no campus?</p>
        <p class="text-5xl italic font-thin mb-4 md:text-5xl fade-in">A gente te ajuda!</p>
      </div>

      <div class="flex mt-24">
        <button
          ref="animatedButton"
          @click="redirectToLoginMicrosoft"
          class="flex items-center rounded-full bg-gray-50 px-10 py-4 md:px-24 md:py-5 text-azul ring-1 ring-inset ring-gray-500/10 ml-12 shadow-sm transition transform transition duration-300 hover:scale-105"
        >
          <img
            src="../assets/icons/Microsoft_logo2.svg"
            alt="Logo Microsoft"
            class="h-6 w-auto mr-4"
          />
          <span class="font-bold font-inter text-lg md:text-xl">
            Entre com a conta da Microsoft
          </span>
        </button>
      </div>
    </div>

    <div
      v-if="foundItems.length"
      class="relative flex flex-col items-center w-full max-w-xl mx-auto p-6 rounded-lg lg:ml-10 mt-10 min-h-screen lg:min-h-full bg-azul"
      @click="animateButton()"
    >
      <div class="grid grid-cols-2 gap-8 flex-grow">
        <ItemCard
          v-for="item in foundItems"
          :key="item.id"
          :name="item.name"
          :location="item.location_name"
          :time="formatTime(item.created_at)"
          :image="item.image_urls[0] || NotAvailableImage"
          :id="item.id"
          :disabled="true"
        />
      </div>
      <div
        class="absolute bottom-0 left-0 w-full h-60 bg-gradient-to-t from-azul to-transparent flex justify-center items-end pb-4"
      >
        <button
          class="bg-laranja text-white font-semibold px-16 py-2 rounded-lg shadow-sm transition transform transition duration-300 hover:scale-105"
        >
          Ver Mais
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import Logo from "../components/Logo.vue";
import { fetchFoundItems } from "@/services/apiItems";
import { formatTime } from "@/utils/dateUtils";
import ItemCard from "../components/Item-Card.vue";

const foundItems = ref([]);
const animatedButton = ref(null);

onMounted(async () => {
  const transitionScreen = document.getElementById("transition-screen");
  const mainContent = document.getElementById("main-content");

  setTimeout(() => {
    transitionScreen.classList.add("fade-out");
  }, 500);

  transitionScreen.addEventListener("animationend", () => {
    transitionScreen.classList.add("hidden");
    mainContent.classList.remove("hidden");
    mainContent.classList.add("fade-in");
  });

  const response = await fetchFoundItems({
    page: 1,
    search: "",
    category_name: "",
    location_name: "",
  });

  foundItems.value = response.results.slice(0, 4);
});

function animateButton() {
  if (animatedButton.value) {
    window.scrollTo({ top: 0, behavior: "smooth" });

    let checkScroll = setInterval(() => {
      if (window.scrollY === 0) {
        clearInterval(checkScroll);

        animatedButton.value.classList.add("scale-125");

        setTimeout(() => {
          animatedButton.value.classList.remove("scale-125");
        }, 300);
      }
    }, 50);
  }
}

function redirectToLoginMicrosoft() {
  window.location.href =
    "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=f1b79927-10ff-4601-a361-f9cab58fb250&scope=User.Read&response_type=code&state=Zay5NfY4tSn7JgvO&domain=alunos.unb.br";
}
</script>

<style scoped>
.fade-out {
  animation: fadeOut 1s forwards;
}

@keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.fade-in {
  animation: fadeIn 1s forwards;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
