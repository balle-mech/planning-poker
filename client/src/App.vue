<template>
  <div id="app">
    <v-app>
      <header>
        <v-app-bar id="app-bar" color="rgb(0, 64, 152)">
          <v-app-bar-title class="text-h5"> ESTiNET </v-app-bar-title>
        </v-app-bar>
      </header>
      <v-main>
        <v-container>
          <router-view></router-view>
        </v-container>
      </v-main>

      <v-footer class="d-flex aligin-center justify-center" color="rgb(230,0,45)" id="app-footer" app>
      </v-footer>

    </v-app>
  </div>

</template>

<script setup>
// import MainHeader from './components/MainHeader.vue';
// import MainFooter from './components/MainFooter.vue';
</script>

