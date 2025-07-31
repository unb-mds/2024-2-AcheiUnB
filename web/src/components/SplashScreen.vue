<template>
  <div v-if="isLoading" class="fixed inset-0 bg-laranja flex items-center justify-center z-50">
    <div class="text-center">
      <img 
        src="@/assets/icons/Favicon2.png" 
        alt="AcheiUnB" 
        class="w-24 h-24 mx-auto mb-4 animate-pulse"
      />
      <h1 class="text-white text-2xl font-bold mb-2">AcheiUnB</h1>
      <div class="w-48 h-1 bg-white/20 rounded-full mx-auto">
        <div class="h-full bg-white rounded-full animate-progress"></div>
      </div>
      <p class="text-white/80 mt-4 text-sm">Carregando...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const isLoading = ref(true);

onMounted(() => {
  // Simular carregamento inicial
  setTimeout(() => {
    isLoading.value = false;
  }, 2000);
});
</script>

<style scoped>
.bg-laranja {
  background-color: #E97316;
}

@keyframes progress {
  0% { width: 0%; }
  100% { width: 100%; }
}

.animate-progress {
  animation: progress 2s ease-in-out;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}
</style>
