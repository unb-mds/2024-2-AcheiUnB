import { createRouter, createWebHashHistory } from "vue-router";
import Login from "../views/Login.vue";
import About from "../views/About.vue";
import Lost from "../views/Lost.vue";
import Found from "../views/Found.vue";
import RegisterLost from "../views/Register-Lost.vue";
import RegisterFound from "../views/Register-Found.vue";
import User from "../views/User.vue";
import Chats from "../views/Chats.vue";

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  {
    path: "/about",
    name: "About",
    component: About,
  },
  {
    path: "/lost",
    name: "Lost",
    component: Lost,
  },
  {
    path: "/found",
    name: "Found",
    component: Found,
  },
  {
    path: "/register-lost",
    name: "RegisterLost",
    component: RegisterLost,
  },
  {
    path: "/register-found",
    name: "RegisterFound",
    component: RegisterFound,
  },
  {
    path: "/user",
    name: "User",
    component: User,
  },
  {
    path: "/chats",
    name: "Chats",
    component: Chats,
  },
];

const router = createRouter({
  history: createWebHashHistory(), // Usar histórico do navegador
  routes,
});

export default router;
