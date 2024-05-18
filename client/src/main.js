import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import axios from "axios";
import VueAxios from "vue-axios";
import router from "./router";

import vuetify from "./plugins/vuetify";

const axiosInstance = axios.create();
axiosInstance.interceptors.request.use((config) => {
  config.headers = {
    // Basic認証対策
    //Authorization: "Bearer hogehoge",
  };
  return config;
});

const app = createApp(App);
app.use(VueAxios, axiosInstance);
// <script setup>内でaxiosをinjectできるように設定する
app.provide("axios", app.config.globalProperties.axios);
app.use(router);
app.use(vuetify).mount("#app");
