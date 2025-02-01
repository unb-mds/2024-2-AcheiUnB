<template>
  <div class="fixed w-full top-0" style="z-index: 1">
    <AboutHeader />
  </div>
  <div class="pt-[120px] flex justify-center my-6 text-azul">
    <Logo />
  </div>
  <span
    class="font-inter text-azul text-center flex justify-center items-center mx-auto max-w-3xl mt-7"
  >
    Somos um grupo da disciplina Métodos de Desenvolvimento de Software da Universidade de
    Brasília.<br />
    Temos como objetivo solucionar um dos problemas da faculdade, que é a falta de ferramentas para
    organizar itens achados e perdidos pelos estudantes.<br />
    Com o AcheiUnB você consegue de forma simples e intuitiva procurar pelo seu item perdido ou
    cadastrar um item que você encontrou.
  </span>

  <div class="max-w-3xl mx-auto mt-10 p-5 pb-[140px]">
    <div class="text-azul text-lg text-center font-semibold mb-7">Criado por:</div>

    <div class="space-y-3">
      <div class="flex items-center justify-center space-x-4">
        <a href="https://github.com/anaelisaramos" target="_blank">
          <img
            src="https://github.com/anaelisaramos.png"
            alt="Ana Elisa Ramos"
            class="w-[100px] rounded-full hover:scale-110 transition-transform"
          />
        </a>

        <div class="text-left">
          <p class="font-inter font-medium">Ana Elisa Ramos</p>
          <p class="text-sm text-cinza3">Engenharia de Software</p>
        </div>
      </div>
      <div class="flex items-center justify-center space-x-4">
        <a href="https://github.com/DaviCamilo23" target="_blank">
          <img
            src="https://github.com/DaviCamilo23.png"
            alt="Davi Camilo"
            class="w-[100px] rounded-full hover:scale-110 transition-transform"
          />
        </a>

        <div class="text-left">
          <p class="font-inter font-medium">Davi Camilo</p>
          <p class="text-sm text-cinza3">Engenharia de Software</p>
        </div>
      </div>
      <div class="flex items-center justify-center space-x-4">
        <a href="https://github.com/potatoyz908" target="_blank">
          <img
            src="https://github.com/potatoyz908.png"
            alt="Euller Júlio da Silva"
            class="w-[100px] rounded-full hover:scale-110 transition-transform"
          />
        </a>

        <div class="text-left">
          <p class="font-inter font-medium">Euller Júlio da Silva</p>
          <p class="text-sm text-cinza3">Engenharia de Software</p>
        </div>
      </div>
      <div class="flex items-center justify-center space-x-4">
        <a href="https://github.com/leoramiroo" target="_blank">
          <img
            src="https://github.com/leoramiroo.png"
            alt="Leonardo Ramiro"
            class="w-[100px] rounded-full hover:scale-110 transition-transform"
          />
        </a>

        <div class="text-left">
          <p class="font-inter font-medium">Leonardo Ramiro</p>
          <p class="text-sm text-cinza3">Engenharia de Software</p>
        </div>
      </div>
      <div class="flex items-center justify-center space-x-4">
        <a href="https://github.com/pedroeverton217" target="_blank">
          <img
            src="https://github.com/pedroeverton217.png"
            alt="Pedro Everton"
            class="w-[100px] rounded-full hover:scale-110 transition-transform"
          />
        </a>

        <div class="text-left">
          <p class="font-inter font-medium">Pedro Everton</p>
          <p class="text-sm text-cinza3">Engenharia de Software</p>
        </div>
      </div>
      <div class="flex items-center justify-center space-x-4">
        <a href="https://github.com/314dro" target="_blank">
          <img
            src="https://github.com/314dro.png"
            alt="Pedro Martins Silva"
            class="w-[100px] rounded-full hover:scale-110 transition-transform"
          />
        </a>

        <div class="text-left">
          <p class="font-inter font-medium">Pedro Martins Silva</p>
          <p class="text-sm text-cinza3">Engenharia de Software</p>
        </div>
      </div>
      <div class="flex items-center justify-center space-x-4">
        <a href="https://github.com/TiagoBalieiro" target="_blank">
          <img
            src="https://github.com/TiagoBalieiro.png"
            alt="Tiago Balieiro"
            class="w-[100px] rounded-full hover:scale-110 transition-transform"
          />
        </a>

        <div class="text-left">
          <p class="font-inter font-medium">Tiago Balieiro</p>
          <p class="text-sm text-cinza3">Engenharia de Software</p>
        </div>
      </div>
    </div>
  </div>

  <ButtonAdd />
  <div class="fixed bottom-0 w-full">
    <MainMenu activeIcon="info" />
  </div>
</template>

<script setup>
import AboutHeader from "../components/Header-About.vue";
import MainMenu from "../components/Main-Menu.vue";
import Logo from "../components/Logo.vue";
</script>

<style scoped></style>
