import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Header from "./components/Search-Header.vue";
import Alert from "./components/Alert.vue";

const app = createApp(App);

app.use(router);
app.component("Header", Header);
app.component("Alert", Alert);
app.mount("#app");

// Registrar PWA Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .then((registration) => {
        console.log('SW registered: ', registration);
      })
      .catch((registrationError) => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}
