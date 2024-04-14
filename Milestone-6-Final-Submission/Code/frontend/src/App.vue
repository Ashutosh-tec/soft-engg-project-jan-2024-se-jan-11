<template>
  <div id="app">
    <NavBar />
    <!-- <LoginComponent /> -->
      <router-view></router-view>
  </div>
</template>

<script>

// import LoginComponent from './components/LoginComponent.vue'
import NavBar from './components/NavBar.vue'
export default {
  name: 'App',
  components: {
    // LoginComponent,
    NavBar
  }
}
</script>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
