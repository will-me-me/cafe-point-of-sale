// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from "vite-plugin-vuetify";
export default defineNuxtConfig({
  modules: [
    "@pinia/nuxt",
    (_options, nuxt) => {
      nuxt.hooks.hook("vite:extendConfig", (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }));
      });
    },
  ],
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
  build: {
    transpile: [
      "vuetify",
      "chart.js",
      "vue-chartjs",
      "@point-of-sale/receipt-printer-encoder",
      "esc-pos-encoder",
    ],
  },
  plugins: [{ src: "~/plugins/chart.client.ts", mode: "client" }],
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
});
