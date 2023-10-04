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
      { url = "/src/storage/mini-wikipedia.output.txt"
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
      
      div [class "main"]
      [ 
        div[class "gallery"][
          div[class "alt-wikipedia-container"][

          -- Back Button
         div[class "previous-button-container"][
            button [onClick Back, class "button"] 
                [   
                i [class "fa-solid fa-chevron-left"][]
                ]
         ],
      
        -- Previous Content
        div [class "previous-wikipedia-content"] [ 

        -- Wikipedia Image  
        div[class "wikipedia-image"][
           img[src (getWikipediaImageUrl (Array.get (model.index - 1) wikipediaRecordsArray)),
                    width 400,
                    height 400][]],
                                  div[class "wikipedia-title"][
                h1 [] [
                getWikipediaTitle (Array.get (model.index - 1) wikipediaRecordsArray)
                ]]    
          ]

        ],
           -- Main Content
        div [
              class "wikipedia-content"
            ] [ 

            -- Wikipedia Image  
        a[
            href (getWikipediaUrl (Array.get model.index wikipediaRecordsArray)),
            target "_blank",
            class "wikipedia-url"
        ][
                  div[class "wikipedia-image"][
           img[src (getWikipediaImageUrl (Array.get model.index wikipediaRecordsArray)),
                    width 500,
                    height 500][]]
            ]
        ],
       
        div[class "alt-wikipedia-container"][
        
        -- Next Button
        div [class "next-button-container"] [

            button [onClick Next, class "button"
                    ] [ 
                   i [class "fa-solid fa-chevron-right"][] 
                      ]
          ],

        -- Next Content
        div [
              class "next-wikipedia-content"
            ] [ 

        -- Wikipedia Image  

        div[class "wikipedia-image"][
           img[src (getWikipediaImageUrl (Array.get (model.index + 1) wikipediaRecordsArray)),
                    width 400,
                    height 400][]],
                                  div[class "wikipedia-title"][
                h1 [] [
                getWikipediaTitle (Array.get (model.index + 1) wikipediaRecordsArray)
                ]]    
        

          ]]
        ],

      -- Additional Content
      div[class "additional-content"][
            div[][],
            div[class "descriptive-content "][

              -- Wikipedia Title
              a[
                href (getWikipediaUrl (Array.get model.index wikipediaRecordsArray)),
                target "_blank",
                class "wikipedia-url"
              ][
              div[class "wikipedia-title"][
                h1 [] [
                getWikipediaTitle (Array.get model.index wikipediaRecordsArray)
                ]]
            ],
              
            -- Wikipedia Abstract
            div[class "wikipedia-abstract"][
                p[] [getWikipediaAbstract (Array.get model.index wikipediaRecordsArray)]
              ],
            
            div[class "wiki-content-category"][

              -- Categories List
              div[class "categories"][                                  
                input[type_ "checkbox", id  "wikipedia-categories"][],
                
                label[for "wikipedia-categories"][
                      i [class "fa-solid fa-bars",
                         class "bars-icon-categories"][], 
                        text("Categories"),
                      i [class "fa-solid fa-chevron-down", 
                         class "chevron-icon-categories"][]],
                ul [] (getWikipediaCategories (Array.get model.index wikipediaRecordsArray))
              ]
                  ]
                      ]                   
      ]
          ]
               ]
      
      
        
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
                 if ((List.length (split " " abstract_info.abstract)) >= 10) then
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


-- Add Wikipedia Category List to HTML
getWikipediaCategories: Maybe WikipediaRecord -> List(Html Msg)
getWikipediaCategories record =
        case record of 
          Nothing ->
            [li [] [a [][text("Nothing")]]]
          Just wikiRecord ->
            case wikiRecord.categories of 
              Nothing ->
               [li [] [a [][text("Nothing")]]]
              Just categories ->
                (List.map getCategoryItem categories)

-- Add Category Item to List
getCategoryItem : Category -> Html msg
getCategoryItem category = 
        a [href ("https://en.wikipedia.org/" ++ category.link), target "_blank"] [ li [][ text ((category.text)) ]]