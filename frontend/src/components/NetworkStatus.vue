<script setup>
import { ref } from 'vue';

const isOnline = ref(navigator.onLine);
const showOfflineBanner = ref(!navigator.onLine);

// Listen for online/offline events
window.addEventListener('online', () => {
  isOnline.value = true;
  showOfflineBanner.value = false;
});

window.addEventListener('offline', () => {
  isOnline.value = false;
  showOfflineBanner.value = true;
});
</script>

<template>
  <!-- Offline Banner -->
  <Transition name="slide-down">
    <div 
      v-if="showOfflineBanner" 
      class="fixed top-0 left-0 right-0 bg-warning-900 border-b border-warning-600 text-warning-200 p-3 z-50"
    >
      <div class="container mx-auto flex items-center gap-2">
        <i class="pi pi-wifi-slash"></i>
        <span class="text-sm font-medium">Offline - Einige Funktionen sind möglicherweise nicht verfügbar</span>
      </div>
    </div>
  </Transition>

  <!-- Connection Status Indicator -->
  <div class="fixed bottom-4 right-4 z-40">
    <div 
      :class="[
        'w-3 h-3 rounded-full border-2 border-gray-700',
        isOnline ? 'bg-success-500' : 'bg-error-500'
      ]"
      :title="isOnline ? 'Online' : 'Offline'"
    ></div>
  </div>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}

.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>