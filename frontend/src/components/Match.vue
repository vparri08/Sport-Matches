<template>
  <div class="card">
    <h5 class="card-header">{{ match_name }}</h5>
    <div class="card-body">
      <h5 class="card-title">Información del Partido</h5>
      <p class="card-text"><strong>ID:</strong> {{id}}</p>
      <p class="card-text"><strong>Nombre del Partido:</strong> {{match_name}}</p>
      <p class="card-text"><strong>Equipo Local:</strong> {{local_team}}</p>
      <p class="card-text"><strong>Equipo Visitante:</strong> {{visitor_team}}</p>
      <p class="card-text"><strong>Competición:</strong> {{competition}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Match',
  props: ['id', 'match_name', 'local_team', 'visitor_team', 'competition']
}
</script>

<style scoped>

</style>
