module Main exposing (..)

import Http
import Browser
import Array exposing (Array)
import String exposing (split)

import Html exposing (..)
import Html.Events exposing (..)
import Html.Attributes exposing (..)

import Json.Decode exposing (Decoder, at,map2, map3, field, string, decodeString)



-- MAIN
main : Program () Model Msg
main = Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

-- INIT
init : () -> (Model, Cmd Msg)
init _ =
  ( {status = Loading , index = 0}
  , getFile
  )



-- MODEL
type LoadDataStatus = Failure | Loading | Success (Array WikipediaRecord)
type alias Model =  {status: LoadDataStatus, index: Int}

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



-- UPDATE
type Msg
  = GotText (Result Http.Error String) 
    | Next 
    | Back

-- Read Wikipedia JSONL file
getFile: Cmd Msg
getFile = Http.get
      { url = "http://localhost:8000/src/storage/mini-wikipedia.output.txt"
      , expect = Http.expectString GotText
      }

-- Entry point to parse JSONL
buildWikipediaRecordsList: String -> List (WikipediaRecord)
buildWikipediaRecordsList fileText =
                          fileText |> split "\n"
                                   |> List.map(parseWikipediaJsonl)
                                   |> List.filter(filterWikipediaRecords)

-- Main function to parse JSONL
parseWikipediaJsonl : String -> WikipediaRecord
parseWikipediaJsonl wikiString =
      let res = (decodeString wikipediaRecordDecoder wikiString ) in case res of
          Ok record -> record
          Err _ -> WikipediaRecord Nothing Nothing

-- Filter out suitable WikipediaRecords
-- A suitable WikipediaRecord is a record that has at least the abstract_info filled 
filterWikipediaRecords : WikipediaRecord -> Bool
filterWikipediaRecords wikiRecord = 
                      case wikiRecord.abstract_info of 
                          Nothing -> 
                                  False
                          Just _ ->
                                  True

-- WikipediaRecord Decoder
wikipediaRecordDecoder : Decoder WikipediaRecord
wikipediaRecordDecoder = map2 WikipediaRecord
                           (Json.Decode.nullable (at ["record","abstract_info"] abstractInfoDecoder))
                           (Json.Decode.nullable (at ["record","sublinks"] (Json.Decode.list sublinkDecoder)))

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
    Next ->
       ({model | index = model.index + 1}, Cmd.none)
    Back ->
       ({model | index = model.index - 1 }, Cmd.none)
    GotText result ->
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
      [ 
        div [class "sidenav"] [ul [] 
        (printWikipediaSublinks (Array.get model.index wikipediaRecordsArray))],
        div [class "content"] [ 
          h2 [] [printWikipediaTitle (Array.get model.index wikipediaRecordsArray)],
          div [] [
            p [] [printWikipediaUrl (Array.get model.index wikipediaRecordsArray)]
          ],
          div [] [
            p [] [printWikipediaAbstract (Array.get model.index wikipediaRecordsArray)]
          ],
          div [] [
              button [ onClick Back ] [ text "Back" ],
              button [ onClick Next ] [ text "Next" ]
          ]
          ]
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

-- Add Wikipedia Title to HTML
printWikipediaUrl : Maybe WikipediaRecord -> Html Msg
printWikipediaUrl record =
        case record of 
        Nothing ->
          text ("Nothing")
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                text("Nothing")
              Just abstract_info ->
                 text(abstract_info.url)

-- Add Wikipedia Abstract to HTML
printWikipediaAbstract : Maybe WikipediaRecord -> Html Msg
printWikipediaAbstract record =
        case record of 
        Nothing ->
          text ("Nothing")
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                text("Nothing")
              Just abstract_info ->
                 text(abstract_info.abstract)

-- Add Wikipedia Sublinks List to HTML
printWikipediaSublinks: Maybe WikipediaRecord -> List(Html Msg)
printWikipediaSublinks record =
        case record of 
          Nothing ->
            [li [] [a [][text("Nothing")]]]
          Just wikiRecord ->
            case wikiRecord.sublinks of 
              Nothing ->
               [li [] [a [][text("Nothing")]]]
              Just sublinks ->
                (List.map toli sublinks)

-- Add Sublink Item to List
toli : Sublink -> Html msg
toli sublink = 
        li [] [a [href sublink.link] [ text (( sublink.anchor)) ]]
        
