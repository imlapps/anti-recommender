module WikipediaTypes exposing (..)

-- Type Aliases for the Wikipedia Record 
type alias WikipediaRecord = {
  abstract_info : Maybe AbstractInfo,
  sublinks : Maybe (List Sublink),
  categories: Maybe (List Category)}  

type alias AbstractInfo = {
  title: String,
  url: String,
  abstract: String,
  image: String} 

type alias Sublink = {
  anchor: String,
  link: String}

type alias Category = {
  text: String,
  link: String}