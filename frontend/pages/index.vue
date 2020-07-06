<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs12>
        <positions-table />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import PositionsTable from '../components/PositionsTable'

export default {
  components: { PositionsTable },
  data() {
    return {
      todoList: []
    }
  }
}
</script>
