<template>
  <v-container fluid>
    <v-layout row>
      <v-flex xs6 order-lg2></v-flex>
      <v-flex xs6 order-lg2>
        <v-container fluid>
          <v-layout row>
            <v-flex xs12 order-lg2>
              <v-text-field
                v-model="search"
                color="teal"
                label="Найти сотрудника"
                append-icon="search"
              ></v-text-field>
            </v-flex>
          </v-layout>
          <v-layout>
            <v-flex xs4>
              <v-checkbox
                v-model="fired"
                @change="toggleFired"
                color="teal"
                label="Показывать уволенных"
              ></v-checkbox>
            </v-flex>
            <v-flex xs4 style="margin: auto 10px;">
              <v-btn block color="teal">Принять на должность</v-btn>
            </v-flex>
            <v-flex xs4 style="margin: auto 10px;">
              <v-btn block disabled color="success">Снять с должности</v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-flex>
    </v-layout>
    <v-data-table
      v-model="selected"
      :headers="headers"
      :items="getOccupations"
      :pagination.sync="pagination"
      :search="search"
      item-key="name"
      select-all
    >
      <template v-slot:headers="props">
        <tr>
          <th>
            <v-checkbox
              :input-value="props.all"
              :indeterminate="props.indeterminate"
              @click="toggleAll"
              primary
              hide-details
            ></v-checkbox>
          </th>
          <th
            v-for="header in props.headers"
            :key="header.text"
            :class="[
              'column sortable',
              pagination.descending ? 'desc' : 'asc',
              header.value === pagination.sortBy ? 'active' : ''
            ]"
            @click="changeSort(header.value)"
          >
            <v-icon small>arrow_upward</v-icon>
            {{ header.text }}
          </th>
        </tr>
      </template>
      <template v-slot:no-results>
        <v-alert :value="true" color="red lighten-3" icon="warning">
          Нет сотрудников по запросу "{{ search }}".
        </v-alert>
      </template>
      <template v-slot:items="props">
        <tr
          :class="{ 'red lighten-3': props.item.fireDate }"
          :active="props.selected"
        >
          <td>
            <v-checkbox
              v-if="!props.item.fireDate"
              :input-value="props.selected"
              primary
              hide-details
            ></v-checkbox>
          </td>
          <td>{{ props.item.name }}</td>
          <td class="text-xs-left">
            {{ props.item.companyName }}
          </td>
          <td class="text-xs-center">
            {{ props.item.positionName }}
          </td>
          <td class="text-xs-center">
            {{ props.item.hireDate }}
          </td>
          <td class="text-xs-center">
            {{ props.item.fireDate }}
          </td>
          <td class="text-xs-center">
            <v-edit-dialog
              :return-value.sync="props.item.salary"
              @save="save"
              @cancel="cancel"
              large
              lazy
              persistent
            >
              <div>{{ props.item.salary }}({{ props.item.fraction }}%)</div>
              <template v-slot:input>
                <div class="mt-3 title">Ставка></div>
              </template>
              <template v-slot:input>
                <v-text-field
                  v-model="props.item.salary"
                  :rules="[rules.nonEmptyField, rules.onlyInt]"
                  label="Ставка руб."
                  single-line
                  counter
                  autofocus
                ></v-text-field>
                <v-text-field
                  v-model="props.item.fraction"
                  :rules="[rules.nonEmptyField, rules.onlyInt, rules.max100]"
                  label="Ставка %."
                  single-line
                  counter
                  autofocus
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </td>
          <td class="text-xs-center">
            <v-edit-dialog
              :return-value.sync="props.item.base"
              @save="save"
              @cancel="cancel"
              large
              lazy
              persistent
            >
              <div>{{ props.item.base }} &#8381;</div>
              <template v-slot:input>
                <div class="mt-3 title">База></div>
              </template>
              <template v-slot:input>
                <v-text-field
                  v-model="props.item.base"
                  :rules="[rules.nonEmptyField, rules.onlyInt]"
                  label="База руб."
                  single-line
                  counter
                  autofocus
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </td>
          <td class="text-xs-center">
            <v-edit-dialog
              :return-value.sync="props.item.advance"
              @save="save"
              @cancel="cancel"
              large
              lazy
              persistent
            >
              <div>{{ props.item.advance }} &#8381;</div>
              <template v-slot:input>
                <div class="mt-3 title">Аванс</div>
              </template>
              <template v-slot:input>
                <v-text-field
                  v-model="props.item.advance"
                  :rules="[rules.nonEmptyField, rules.onlyInt]"
                  label="Аванс руб."
                  single-line
                  counter
                  autofocus
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </td>
          <td class="text-xs-center">
            <v-checkbox
              v-model="props.item.byHours"
              primary
              hide-details
            ></v-checkbox>
          </td>
        </tr>
      </template>
    </v-data-table>
    <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
      {{ snackText }}
      <template v-slot:action="{ attrs }">
        <v-btn v-bind="attrs" @click="snack = false" text>Close</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { GET_OCCUPATIONS } from '../graphql'
export default {
  name: 'PositionsTable',
  data() {
    return {
      rules: {
        nonEmptyField: value => !!value.length || 'Поле не должно быть пустым',
        onlyInt: value => Number.isInteger(parseInt(value)) || 'Укажите число',
        max100: value => value <= 100 || 'Максимум 100%'
      },
      snack: false,
      snackColor: '',
      snackText: '',
      search: '',
      fired: true,
      showFired: true,
      pagination: {
        sortBy: 'name'
      },
      selected: [],
      headers: [
        {
          text: 'Сотрудник',
          align: 'left',
          value: 'name'
        },
        { text: 'Компания', align: 'center', value: 'companyName' },
        { text: 'Должность', align: 'center', value: 'positionName' },
        { text: 'Дата приема', align: 'center', value: 'hireDate' },
        { text: 'Дата увольнения', align: 'center', value: 'fireDate' },
        { text: 'Ставка', align: 'center', value: 'salary' },
        { text: 'База', align: 'center', value: 'base' },
        { text: 'Аванс', align: 'center', value: 'advance' },
        { text: 'Почасовая', align: 'center', value: 'byHours' }
      ],
      getOccupations: [],
      positions: []
    }
  },
  apollo: {
    getOccupations: { query: GET_OCCUPATIONS }
  },
  created() {
    this.positions = this.getOccupations
  },
  methods: {
    save() {
      this.snack = true
      this.snackColor = 'teal'
      this.snackText = 'Изменения сохранены'
    },
    cancel() {
      this.snack = true
      this.snackColor = 'red lighten-3'
      this.snackText = 'Отмена'
    },
    toggleFired() {
      if (!this.fired) {
        this.getOccupations = this.getOccupations.filter(pos => !pos.fireDate)
      } else {
        this.filterAll()
      }
    },
    filterAll() {
      this.getOccupations = this.positions
    },
    toggleAll() {
      const toSlice = this.getOccupations.filter(pos => !pos.fireDate)
      if (this.selected.length) this.selected = []
      else this.selected = toSlice.slice()
    },
    changeSort(column) {
      if (this.pagination.sortBy === column) {
        this.pagination.descending = !this.pagination.descending
      } else {
        this.pagination.sortBy = column
        this.pagination.descending = false
      }
    }
  }
}
</script>
