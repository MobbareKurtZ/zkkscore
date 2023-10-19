<template>
  <div id="app">
    <Slide :updateKey="updateKey"/>
    <Kaffe />
  </div>
</template>

<script>
import Slide from './components/Slide.vue'
import Kaffe from './components/Kaffe.vue'

export default {
  name: 'App',
  components: {
    Kaffe, Slide
  },
  data() {
    return {
      updateKey: 0,
    };
  },
  mounted: () => {
    window.setInterval(() => {
      this.forceRerender()
    }, 3600000)
  }
}
</script>

<style lang="scss">
@import "@/scss/style.scss";
</style>
