<template>
  <div v-if="showInstallPrompt" class="fixed bottom-4 left-4 right-4 bg-laranja text-white p-4 rounded-lg shadow-lg z-50">
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <svg class="w-8 h-8 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
        </svg>
        <div>
          <h3 class="font-semibold">Instalar AcheiUnB</h3>
          <p class="text-sm opacity-90">Acesse mais rápido instalando o app</p>
        </div>
      </div>
      <div class="flex space-x-2">
        <button @click="installApp" class="bg-white text-laranja px-4 py-2 rounded-md font-medium hover:bg-gray-100 transition-colors">
          Instalar
        </button>
        <button @click="dismissPrompt" class="text-white/70 hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const showInstallPrompt = ref(false);
const deferredPrompt = ref(null);

onMounted(() => {
  // Escutar o evento beforeinstallprompt
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt.value = e;
    
    // Verificar se o usuário já dismissou o prompt
    if (!localStorage.getItem('pwa-dismissed')) {
      showInstallPrompt.value = true;
    }
  });

  // Escutar quando o app é instalado
  window.addEventListener('appinstalled', () => {
    console.log('PWA foi instalado');
    showInstallPrompt.value = false;
    localStorage.setItem('pwa-dismissed', 'true');
  });
});

const installApp = async () => {
  if (deferredPrompt.value) {
    deferredPrompt.value.prompt();
    const { outcome } = await deferredPrompt.value.userChoice;
    
    if (outcome === 'accepted') {
      console.log('Usuário aceitou instalar o PWA');
    } else {
      console.log('Usuário rejeitou instalar o PWA');
    }
    
    deferredPrompt.value = null;
    showInstallPrompt.value = false;
  }
};

const dismissPrompt = () => {
  showInstallPrompt.value = false;
  localStorage.setItem('pwa-dismissed', 'true');
};
</script>

<style scoped>
.bg-laranja {
  background-color: #E97316;
}

.text-laranja {
  color: #E97316;
}
</style>
