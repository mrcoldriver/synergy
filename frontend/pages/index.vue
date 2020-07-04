<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs6 order-lg2>
        <h1>
          Занимаемые должности
        </h1>
      </v-flex>
    </v-layout>
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
