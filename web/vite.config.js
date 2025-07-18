import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";
import { VitePWA } from 'vite-plugin-pwa';
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(), 
    vueDevTools(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
      manifest: {
        name: 'AcheiUnB',
        short_name: 'AcheiUnB',
        description: 'Aplicativo para encontrar e vender itens na UnB',
        theme_color: '#E97316',
        background_color: '#ffffff',
        display: 'standalone',
        orientation: 'portrait',
        scope: '/',
        start_url: '/',
        icons: [
          {
            src: 'src/assets/icons/Favicon.png',
            sizes: '64x64',
            type: 'image/png'
          },
          {
            src: 'src/assets/icons/Favicon2.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'src/assets/icons/Favicon3.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,webp}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\.acheiunb\.com\.br\//,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 24 * 60 * 60 // 24 horas
              }
            }
          }
        ]
      }
    })
  ],
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
