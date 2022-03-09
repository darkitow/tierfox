<template>
  <div>
    <div class="top">
    </div>
    
    <div class="app">
      <Tierlist/>
      <p class="desc"> made by maia <a href="https://github.com/darkitow">github</a></p>
    </div>
  </div>
</template>

<script>
import Tierlist from './components/Tierlist.vue'

export default {
  name: 'app',
  components: {
    Tierlist
  }
}
</script>

<style>
@import './assets/style.css';
</style>
