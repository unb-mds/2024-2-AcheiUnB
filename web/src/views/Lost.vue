<template>
  <div class="min-h-screen">
    <div class="fixed w-full top-0">
      <SearchHeader />
    </div>

    <div class="pt-24 pb-8">
      <SubMenu />
    </div>

    <div
      class="grid grid-cols-[repeat(auto-fit,_minmax(180px,_1fr))] sm:grid-cols-[repeat(auto-fit,_minmax(200px,_1fr))] justify-items-center align-items-center lg:px-3 gap-y-3 pb-10"
    >
      <ItemCard :image="imagem1" time="Agora a pouco" />
      <ItemCard :image="imagem2" time="Há uma hora" />
      <ItemCard :image="imagem3" time="Há 2 seg" />
      <ItemCard :image="imagem3" time="Agora a pouco" />
      <ItemCard :image="imagem5" time="Há uma hora" />
      <ItemCard :image="imagem4" time="Agora a pouco" />
      <ItemCard :image="imagem5" time="Agora a pouco" />
      <ItemCard :image="imagem6" time="Há uma hora" />
      <ItemCard :image="imagem4" time="Há 2 seg" />
      <ItemCard :image="imagem5" time="Agora a pouco" />
      <ItemCard :image="imagem6" time="Há uma hora" />
      <ItemCard :image="imagem1" time="Há 2 seg" />
      <ItemCard :image="imagem2" time="Há uma hora" />
      <ItemCard :image="imagem6" time="Há uma hora" />
      <ItemCard :image="imagem1" time="Há uma hora" />
      <ItemCard :image="imagem2" time="Agora a pouco" />
      <ItemCard :image="imagem3" time="Há 2 seg" />
      <ItemCard :image="imagem4" time="Há uma hora" />
    </div>

    <div
      class="flex w-full justify-start sm:justify-center gap-x-6 pb-[120px] px-10"
    >
      <img
        src="../assets/icons/arrow-left.svg"
        alt=""
        class="w-[30px] h-[30px]"
      />
      <img
        src="../assets/icons/arrow-right.svg"
        alt=""
        class="w-[30px] h-[30px]"
      />
    </div>

    <ButtonAdd />
    <div class="fixed bottom-0 w-full">
      <MainMenu activeIcon="search" />
    </div>
  </div>
</template>

<script setup>
import MainMenu from "../components/Main-Menu.vue";
import ItemCard from "../components/Item-Card.vue";
import ButtonAdd from "../components/Button-Add-Lost.vue";
import SearchHeader from "../components/Search-Header.vue";
import SubMenu from "../components/Sub-Menu-Lost.vue";
import imagem1 from "/src/assets/images/carteira.png";
import imagem2 from "/src/assets/images/bone.png";
import imagem3 from "/src/assets/images/caneta.png";
import imagem4 from "/src/assets/images/gloss.png";
import imagem5 from "/src/assets/images/not-available.png";
import imagem6 from "/src/assets/images/sombrinha.png";
</script>

<style scoped></style>
