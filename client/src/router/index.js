import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Pbl from "../pages/Pbl.vue";
import sp from "../pages/spVote.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/pbls/:pblId",
    name: "Pbl",
    component: Pbl,
  },
  {
    path: "/pbls/:pblId/:backlogId",
    name: "sp",
    component: sp,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
