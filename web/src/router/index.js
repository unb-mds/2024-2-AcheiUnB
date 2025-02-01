import { createRouter, createWebHashHistory } from "vue-router";
import Login from "../views/Login.vue";
import About from "../views/About.vue";
import Lost from "../views/Lost.vue";
import Found from "../views/Found.vue";
import RegisterLost from "../views/Register-Lost.vue";
import RegisterFound from "../views/Register-Found.vue";
import User from "../views/User.vue";
import Chats from "../views/Chats.vue";
import ListItem from "../views/ListItem.vue";
import UserItemsLost from "../views/UserItems-Lost.vue";
import UserItemsFound from "../views/UserItems-Found.vue";
import Message from "../views/Message.vue";

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
    meta: { requiresAuth: true },
  },
  {
    path: "/lost",
    name: "Lost",
    component: Lost,
    meta: { requiresAuth: true },
  },
  {
    path: "/found",
    name: "Found",
    component: Found,
    meta: { requiresAuth: true },
  },
  {
    path: "/register-lost",
    name: "RegisterLost",
    component: RegisterLost,
    meta: { requiresAuth: true },
  },
  {
    path: "/register-found",
    name: "RegisterFound",
    component: RegisterFound,
    meta: { requiresAuth: true },
  },
  {
    path: "/user",
    name: "User",
    component: User,
    meta: { requiresAuth: true },
  },
  {
    path: "/chats",
    name: "Chats",
    component: Chats,
    meta: { requiresAuth: true },
  },
  {
    path: "/list-item",
    name: "ListItem",
    component: ListItem,
    meta: { requiresAuth: true },
  },
  {
    path: "/user-items-lost",
    name: "UserItemsLost",
    component: UserItemsLost,
  },
  {
    path: "/user-items-found",
    name: "UserItemsFound",
    component: UserItemsFound,
  },
  /*{
    path: "/message",
    name: "Message",
    component: Message,
  },*/
  {
    path: "/chat/new",
    name: "NewChat",
    component: Message, // A mesma tela de chat será usada para criar um novo chat
    meta: { requiresAuth: true },
  },
  {
    path: "/chat/:chatroomId",
    name: "Chat",
    component: Message,
    meta: { requiresAuth: true },
    props: true, // Permite passar o `chatroomId` como propriedade
  },
  { path: "/:catchAll(.*)", name: "NotFound", component: Login },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
