import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  css: {
    postcss: "./postcss.config.cjs",
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  base: "/static/dist/",
  build: {
    outDir: path.resolve(__dirname, "../API/AcheiUnB/static/dist"),
    manifest: true,
    emptyOutDir: true,
    assetsDir: "static/dist/assets", // Pasta onde as imagens e outros arquivos estáticos serão armazenados

    rollupOptions: {
      output: {
        // Define o nome dos arquivos JS
        entryFileNames: "js/[name]-[hash].js",

        // Define o nome dos arquivos de assets (imagens, fontes)
        assetFileNames: "assets/[name]-[hash][extname]", // As imagens serão armazenadas em 'static/dist/assets/'
      },
    },
  },

  // Adicionando uma configuração global para que o Vite processe as imagens corretamente
  assetsInclude: [
    "**/*.png",
    "**/*.jpg",
    "**/*.jpeg",
    "**/*.gif",
    "**/*.svg",
    "**/*.webp",
  ],
});
