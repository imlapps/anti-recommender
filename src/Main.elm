module Main exposing (..)

import Http
import Browser
import Array exposing (Array)

import Html exposing (..)
import Html.Events exposing (..)
import Html.Attributes exposing (..)

import Parser exposing (..)
import WikipediaTypes exposing (..)
import String exposing (split)


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
  ( {status = Loading , index = 0, numberOfRecords = 0}
  , getFile
  )



-- MODEL
type LoadDataStatus = Failure | Loading | Success (Array WikipediaRecord)
type alias Model =  {status: LoadDataStatus, index: Int, numberOfRecords: Int}


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



-- UPDATE
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Next ->
       ({model | index = if model.index >= model.numberOfRecords - 1 then 0 
                         else model.index + 1}, Cmd.none)
    Back ->
       ({model | index = if model.index <= 0  then model.numberOfRecords - 1 
                         else model.index - 1}, Cmd.none)
    GotText result ->
      case result of
        Ok fileText ->
          let wikipediaRecordsArray = Array.fromList(buildWikipediaRecordsList(fileText)) in
          ({model | status = Success wikipediaRecordsArray, 
                    numberOfRecords = Array.length wikipediaRecordsArray}, 
          Cmd.none)
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
      div[][    
        div[class "header"][h1[][text("NerdSwipe")]],

      div [style "display" "flex",
           style "column-gap" "465px"]
      [ 
        -- Back Button
        div[
            style "margin-top" "300px",
            style "margin-left" "50px"]
        [              
          button [onClick Back,
                  style "background-color" "DodgerBlue",
                  style "border" "none",
                  style "color" "white",
                  style "padding" "12px 16px",
                  style "font-size" "16px",
                  style "cursor" "pointer"
                  ] 
                [ 
                i [class "fa-solid fa-chevron-left"][]
                ]
        ],
        -- Main Content
        div [
             style "width" "500px",
             style "height" "500px",
             style "margin-top" "30px"
            ] [ 
              div[style "display" "flex",
                  style "justify-content" "center"][
                  a[
                  href (getWikipediaUrl (Array.get model.index wikipediaRecordsArray)),
                  target "_blank",
                  style "color" "#222",
                  style "text-decoration" "none"
                ][
                  h1 [] [getWikipediaTitle (Array.get model.index wikipediaRecordsArray)]]],
                 div[style "display" "flex",
                 style "justify-content" "center"][
                
                img[src (getWikipediaImageUrl (Array.get model.index wikipediaRecordsArray)),
                    width 300,
                    height 300][]],

              div[style "display" "flex"
              ][p [] [getWikipediaAbstract (Array.get model.index wikipediaRecordsArray)]],
              
              div[class "wrapper"][                                  
                input[type_ "checkbox", id  "wikipedia-items"][],
                label[for "wikipedia-items", class "first"][i [class "fa-solid fa-bars",
                                                               style "padding-right" "10px"][], 
                                                            text("Contents"),
                                                            i [class "fa-solid fa-chevron-down",
                                                               style "padding-left" "45px"][]],
                ul [] (getWikipediaSublinks (Array.get model.index wikipediaRecordsArray))
              ]
              , div[style "height" "20px"][]  
          ],

        -- Next Button
        div [
            style "margin-top" "300px",
            style "margin-right" "50px"] [

              button [onClick Next, 
                      style "background-color" "DodgerBlue",
                      style "border" "none",
                      style "color" "white",
                      style "padding" "12px 16px",
                      style "font-size" "16px",
                      style "cursor" "pointer" 
                     ] [ 
                  i [class "fa-solid fa-chevron-right"][] 
              ]
          ]

      ] ]

        
-- Add Wikipedia Title to HTML
getWikipediaTitle : Maybe WikipediaRecord -> Html Msg
getWikipediaTitle record =
        case record of 
        Nothing ->
          text ("Nothing")
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                text("Nothing")
              Just abstract_info ->
                 text(abstract_info.title)

-- Add Wikipedia URL to HTML
getWikipediaUrl : Maybe WikipediaRecord -> String
getWikipediaUrl record =
        case record of 
        Nothing ->
          "Nothing"
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                "Nothing"
              Just abstract_info ->
                 abstract_info.url

-- Add Wikipedia Abstract to HTML
getWikipediaAbstract : Maybe WikipediaRecord -> Html Msg
getWikipediaAbstract record =
        case record of 
        Nothing ->
          text ("Nothing")
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                text("Nothing")
              Just abstract_info ->
                 if ((List.length (split " " abstract_info.abstract)) >= 20) then
                 text(abstract_info.abstract) else text(" ")

-- Add Wikipedia Image to HTML
getWikipediaImageUrl : Maybe WikipediaRecord -> String 
getWikipediaImageUrl record = 
        case record of 
        Nothing ->
          ""
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                ""
              Just abstract_info ->
                 abstract_info.image

-- Add Wikipedia Sublinks List to HTML
getWikipediaSublinks: Maybe WikipediaRecord -> List(Html Msg)
getWikipediaSublinks record =
        case record of 
          Nothing ->
            [li [] [a [][text("Nothing")]]]
          Just wikiRecord ->
            case wikiRecord.sublinks of 
              Nothing ->
               [li [] [a [][text("Nothing")]]]
              Just sublinks ->
                (List.map getSublinkItem sublinks)

-- Add Sublink Item to List
getSublinkItem : Sublink -> Html msg
getSublinkItem sublink = 
        a [href sublink.link, target "_blank"] [ li [][ text (( sublink.anchor)) ]]