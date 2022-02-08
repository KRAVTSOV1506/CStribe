<template>
<div id="app">
    <core-view />
</div>
</template>

<script>
  export default { 
    name: 'Index',
    components: {
      CoreView: () => import('../components/CoreView'),
    },
  }
</script>