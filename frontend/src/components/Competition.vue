<template>
  <div class="card">
    <h5 class="card-header">{{ competition_name }}</h5>
    <div class="card-body">
      <h5 class="card-title">Información de la Competición</h5>
      <p class="card-text"><strong>ID:</strong> {{id}}</p>
      <p class="card-text"><strong>Nombre de la Competición:</strong> {{competition_name}}</p>
      <p class="card-text"><strong>Categoría:</strong> {{category}}</p>
      <p class="card-text"><strong>Deporte:</strong> {{sport}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Competition',
  props: ['id', 'competition_name', 'category', 'sport']
}
</script>

<style scoped>

</style>
