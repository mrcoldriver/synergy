import gql from 'graphql-tag'

// т.к. внутренности записи Todo используются практически во всех запросах,
// то резонно вынести их в отдельный фрагмент
// https://www.apollographql.com/docs/react/data/fragments/
const OCCUPATION_FRAGMENT = gql`
  fragment OccupationContents on OccupationType {
    id
    name
    positionName
    companyName
    hireDate
    fireDate
    salary
    fraction
    base
    advance
    byHours
  }
`

const ADD_OCCUPATION = gql`
  mutation(
    $name: String!
    $company_name: String!
    $position_name: String!
    $hire_date: Date!
    $fire_date: Date
    $salary: Int!
    $fraction: Int!
    $base: Int!
    $advance: Int!
    $by_hours: Boolean!
  ) {
    addOccupation(
      name: $name
      companyName: $company_name
      positionName: $position_name
      hireDate: $hire_date
      fireDate: $fire_date
      salary: $salary
      fraction: $fraction
      base: $base
      advance: $advance
      byHours: $by_hours
    ) {
      ...OccupationContents
    }
  }
  ${OCCUPATION_FRAGMENT}
`

const GET_OCCUPATIONS = gql`
  {
    getOccupations {
      ...OccupationContents
    }
  }
  ${OCCUPATION_FRAGMENT}
`

export { ADD_OCCUPATION, GET_OCCUPATIONS }
