<template>
  <div id="app">
    <Slide/>
    <Kaffe/>
  </div>
</template>

<script>
import Slide from './components/Slide.vue'
import Kaffe from './components/Kaffe.vue'

export default {
  name: 'App',
  components: {
    Kaffe, Slide
  }
}
</script>

<style lang="scss">
@import "@/scss/style.scss";
</style>
