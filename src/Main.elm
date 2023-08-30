module Main exposing (..)

import Http
import Browser
import Array exposing (Array)
import String exposing (split)
import Html exposing (Html, text, div)
import Json.Decode exposing (Decoder, at,map2, map3, list, field, string, decodeString)



-- MAIN
main : Program () Model Msg
main = Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

type LoadDataStatus = Failure | Loading | Success (Array WikipediaRecord)

-- MODEL
type alias Model =  {status: LoadDataStatus}


-- Type Aliases for the Wikipedia Record 
type alias WikipediaRecord = {
  abstract_info : Maybe AbstractInfo,
  sublinks : Maybe (List Sublink)}  

type alias AbstractInfo = {
  title: String,
  url: String,
  abstract: String} 

type alias Sublink = {
  anchor: String,
  link: String}


init : () -> (Model, Cmd Msg)
init _ =
  ( {status = Loading}
  , getFile
  )


-- UPDATE
type Msg
  = GotFile (Result Http.Error String) 


-- Read Wikipedia JSONL file
getFile: Cmd Msg
getFile = Http.get
      { url = "http://localhost:8000/src/storage/mini-wikipedia.output.txt"
      , expect = Http.expectString GotFile
      }

-- Entry point to parse JSONL
buildWikipediaRecordsList: String -> List (WikipediaRecord)
buildWikipediaRecordsList fileText =
                          fileText |> split "\n"
                                   |> List.map(parseWikipediaJsonl)

-- Main function to parse JSONL
parseWikipediaJsonl : String -> WikipediaRecord
parseWikipediaJsonl wikipediaString =
      let res = (decodeString wikipediaRecordDecoder wikipediaString) in case res of
          Ok record -> record
          Err _ -> WikipediaRecord Nothing Nothing

-- WikipediaRecord Decoder
wikipediaRecordDecoder : Decoder WikipediaRecord
wikipediaRecordDecoder = map2 WikipediaRecord
                           (Json.Decode.nullable (at ["record","abstract_info"] abstractInfoDecoder))
                           (Json.Decode.nullable (at ["record","sublinks"] (list sublinkDecoder)))

-- AbstractInfo Decoder
abstractInfoDecoder : Decoder AbstractInfo
abstractInfoDecoder = 
        map3 AbstractInfo
                  (field "title" string)
                  (field "url" string)
                  (field "abstract" string)

-- Sublink Decoder
sublinkDecoder : Decoder Sublink 
sublinkDecoder = 
    map2 Sublink 
       (field "anchor" string)
       (field "link" string)

-- UPDATE
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    GotFile result ->
      case result of
        Ok fileText ->
          let wikipediaRecordsArray = Array.fromList(buildWikipediaRecordsList(fileText)) in
          ({model | status = Success wikipediaRecordsArray}, Cmd.none)
        Err _ ->
          ({model | status = Failure}, Cmd.none)
    


-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none

-- VIEW
view : Model -> Html Msg
view model =
  case model.status of
    Failure ->
      text "Unable to load Wikipedia Data"

    Loading ->
      text "Loading..."

    Success wikipediaRecordsArray ->
      div []
      [ div [] [ printWikipediaTitle (Array.get 1 wikipediaRecordsArray) ]
      ]

-- Add Wikipedia Title to HTML
printWikipediaTitle : Maybe WikipediaRecord -> Html Msg
printWikipediaTitle record =
        case record of 
        Nothing ->
          text ("Nothing")
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                text("Nothing")
              Just abstract_info ->
                 text(abstract_info.title)