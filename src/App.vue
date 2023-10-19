<template>
  <div id="app">
    <Slide ref="$slideref"/>
    <Kaffe @triggerFunc="triggerFunc"/>
  </div>
</template>

<script>
import Slide from './components/Slide.vue'
import Kaffe from './components/Kaffe.vue'

export default {
  import {ref} from 'vue'
  name: 'App',
  components: {
    Kaffe, Slide
  }
  methods: {
    triggerFunc(){
      this.$refs.$slideref.forceRerender()
    }
  }
}
</script>

<style lang="scss">
@import "@/scss/style.scss";
</style>
