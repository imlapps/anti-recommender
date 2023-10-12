module Main exposing (..)

import Http
import Browser
import Random
import Array exposing (Array)

-- import Html exposing (..)
-- import Html.Events exposing (..)
-- import Html.Attributes exposing (..)
import Html.Styled exposing (..)
import Html.Styled.Attributes exposing (..)
import Html.Styled.Events exposing (onClick)

import Parser exposing (..)
import WikipediaTypes exposing (..)
import String exposing (split)

import Css
import Css.Global
import Tailwind.Breakpoints as Breakpoints
import Tailwind.Utilities as Tw
import Tailwind.Theme as Tw

-- MAIN
main : Program () Model Msg
main = Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view >> toUnstyled
    }

-- INIT
init : () -> (Model, Cmd Msg)
init _ =
  ( {status = Loading , index = 0, randomIndex = 13, numberOfRecords = 0}
  , getFile
  )



-- MODEL
type LoadDataStatus = Failure | Loading | Success (Array WikipediaRecord)
type alias Model =  {status: LoadDataStatus, index: Int, randomIndex: Int, numberOfRecords: Int}


-- UPDATE
type Msg
  = GotText (Result Http.Error String) 
    | Next 
    | Back
    | RandomNumber Int

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
                         else model.index + 1}, 
                 Random.generate RandomNumber (Random.int 2 (model.numberOfRecords - 2)))
    Back ->
       ({model | index = if model.index <= 0  then model.numberOfRecords - 1 
                         else model.index - 1}, 
                 Random.generate RandomNumber (Random.int 2 (model.numberOfRecords - 2)))
    RandomNumber randomNumber->
       ({model | randomIndex = randomNumber}, Cmd.none)
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

      -- header  
      div[css[Tw.flex, 
              Tw.pl_8, 
              Tw.text_left, 
              Tw.text_color Tw.custom_pink,
              Tw.border_b_8,
              Tw.border_color Tw.black,
              Tw.bg_color Tw.gray_400,
              Tw.bg_radial_gradient
             ]]
             [h1[][text("NerdSwipe")]],
      -- main container
      div [css[Tw.flex, 
            Tw.flex_col, 
            Tw.justify_between,
            Tw.bg_color Tw.custom_black_2]]
      [ 
      
      -- gallery container
      div[css [Tw.flex, 
             Tw.flex_row, 
             Tw.justify_between, 
             Tw.bg_color Tw.black,
             Tw.border_b_8,
             Tw.border_color Tw.black,
             Tw.pr_4,
             Tw.pl_4]][
          
        -- previous wikipedia container
          div[
            css[Tw.flex, 
                Tw.items_center,
                Tw.justify_center]][

          -- previous button
         div[css [Tw.z_10,
                  Tw.absolute, 
                  Tw.transform,
                  Tw.translate_x_36,Tw.translate_y_0]][
            button [onClick Back,
                    css[
                    Tw.bg_color Tw.custom_pink,
                    Tw.border,
                    Tw.text_color Tw.zinc_100,
                    Tw.border_color Tw.black, 
                    Tw.rounded,
                    Tw.text_5xl, Tw.cursor_pointer,
                    Tw.px_4, Tw.py_3
            ] 
                    ] 
                [   
                i [class "fa-solid fa-chevron-left"][]
                ]
         ],
      
        -- previous content
        div [
          css [ Tw.hidden,
                Breakpoints.lg[
                Tw.block,
                Tw.opacity_20]
            ]
        ] [ 

        -- wikipedia image (Previous)
        div[
          css[
            Tw.flex, 
            Tw.self_center,
            Tw.justify_center, 
            Tw.border,
            Tw.border_color Tw.gray_900, 
            Tw.rounded,
            Tw.text_color Tw.zinc_100
            ]
        ][
           img[src (getWikipediaImageUrl (Array.get (model.index - 1) wikipediaRecordsArray)),
                    width 400,
                    height 400][]],
          
          -- wikipedia title (previous)
           div[
            css[ 
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.pink_400, 
              Tw.font_serif
              ]
            ][
             h2 [] [
                getWikipediaTitle (Array.get (model.index - 1) wikipediaRecordsArray)
                ]
              ]
          ]
        ],
           -- main content
        div [
            css [
            Tw.mb_4, 
            Tw.mt_4
            ]
            ] [ 

        -- wikipedia image  (Main)
        a[
            href (getWikipediaUrl (Array.get model.index wikipediaRecordsArray)),
            target "_blank",
            css [
                  Tw.no_underline,
                  Tw.text_color Tw.gray_900
            ]
        ][
        div[
          css[ 
            Tw.flex, 
            Tw.self_center,
            Tw.justify_center, 
            Tw.border,
            Tw.border_color Tw.gray_900, 
            Tw.rounded,
            Tw.text_color Tw.zinc_100
            ]
        ][
           img[src (getWikipediaImageUrl (Array.get model.index wikipediaRecordsArray)),
                    width 500,
                    height 500][]]
            ],

          -- wikipedia title (Main)
         div[
            css[ 
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.pink_400, 
              Tw.font_serif
              ]
            ][
             h1 [] [
                getWikipediaTitle (Array.get (model.index) wikipediaRecordsArray)
                ]
              ]
        ],
                 
        -- next wikipedia container
        div[css[Tw.flex, 
                Tw.items_center,
                Tw.justify_center]][

          -- next button
         div[css [Tw.z_10,
                  Tw.absolute, 
                  Tw.transform,
                  Tw.translate_x_64,Tw.translate_y_0]][
            button [onClick Next,
                    css[
                    Tw.bg_color Tw.pink_400,
                    Tw.border,
                    Tw.text_color Tw.zinc_100,
                    Tw.border_color Tw.black, 
                    Tw.rounded,
                    Tw.text_5xl, Tw.cursor_pointer,
                    Tw.px_4, Tw.py_3
            ] 
                    ] 
                [   
                i [class "fa-solid fa-chevron-right"][]
                ]
         ],
      
        -- next content
        div [
          css [ Tw.hidden,
                Breakpoints.lg[
                Tw.block,
                Tw.opacity_20]
            ]
        ] [ 

        -- wikipedia image (next)
        div[
          css[ 
            Tw.flex, 
            Tw.self_center,
            Tw.justify_center, 
            Tw.border,
            Tw.border_color Tw.gray_900, 
            Tw.rounded,
            Tw.text_color Tw.zinc_100
            ]
        ][
           img[src (getWikipediaImageUrl (Array.get (model.index + 1) wikipediaRecordsArray)),
                    width 400,
                    height 400][]],
            
           -- wikipedia title (next)
           div[
            css[ 
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.pink_400, 
              Tw.font_serif
              ]
            ][
             h2 [] [
                getWikipediaTitle (Array.get (model.index + 1) wikipediaRecordsArray)
                ]
              ]
            ]
          ]
        ]
      ],
      div[
        css[
          Tw.flex,
          Tw.flex_col,
          Tw.justify_center,
          Tw.bg_color Tw.custom_black_2,
          Breakpoints.lg[
          Tw.flex_row
          ]
        ]
      ][       

        -- Abstract and Table of Contents
        div[
          css[

            Breakpoints.lg[
            Tw.basis_1over4
            ]

          ]
        ][          
          
          div[
            css [
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.pink_400, 
              Tw.font_serif
          ]
          ][
            h1[][text("Abstract")]
          ],
          div[css[
                  Tw.text_lg, 
                  Tw.flex,
                  Tw.justify_center,
                  Tw.text_color Tw.gray_200
                 
            ]][
                p[] [getWikipediaAbstract (Array.get model.index wikipediaRecordsArray)]
              ],
          div[
            css [ 
              Tw.hidden,
              Breakpoints.lg[
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.pink_400, 
              Tw.font_serif]
            ]
          ][
            h1[][text("Table of Contents")]
          ],
          div[
           css [ Tw.hidden,
                Breakpoints.lg[
                Tw.block,
                Tw.flex_row,
                Tw.justify_evenly]
            ]

          ][
              ul [] (getWikipediaSublinks (Array.get model.index wikipediaRecordsArray))
          ]], 

        -- Ratings and Categories View       
        div[
          css[
            Tw.flex,
            Tw.flex_col_reverse,

            Breakpoints.lg[
            Tw.basis_1over2,
            Tw.flex_col
            ]

          ]
          ][
       
         div[
          css[
            Tw.flex,
            Tw.justify_center,
            Tw.pb_5
          ]
         ][
          ratings
         ],
         div[][
            div[
          
            css [
              
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.pink_400, 
              Tw.font_serif,
              Tw.mt_8
          ]
          ][
            h1[][text("Categories")]
          ],
          div[
            css [
 
          ]
          ][
              ul [] (getWikipediaCategories (Array.get model.index wikipediaRecordsArray))
          ]
         ]

     ],

        -- Explore View
        div[
          css [ Tw.hidden,
                Breakpoints.lg[
                Tw.block,
               Tw.basis_1over4]
            ]
        ][
          div[css [
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.pink_400, 
              Tw.font_serif
          ]][
            h1[][text("Explore")]
          ],
          div[
            css [
              Tw.flex_col,
              Tw.justify_evenly
            ]
          ][
         (getRandomItem (Array.get model.randomIndex wikipediaRecordsArray)),
         (getRandomItem (Array.get (model.randomIndex - 1) wikipediaRecordsArray)),
         (getRandomItem (Array.get (model.randomIndex + 1) wikipediaRecordsArray)),
         (getRandomItem (Array.get (model.randomIndex - 2) wikipediaRecordsArray)),
         (getRandomItem (Array.get (model.randomIndex + 2) wikipediaRecordsArray))
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
                text ("Nothing")
              Just abstract_info ->
                 text (abstract_info.title)

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

          a [href ("https://en.wikipedia.org/" ++ category.link), target "_blank"] 
          [ li [

          ][ text ((category.text))]]

-- Add Random List Item to HTML
getRandomItem : Maybe WikipediaRecord -> Html Msg
getRandomItem record =
        div[css[
            Tw.pr_6,
            Tw.pl_4,
            Tw.py_2,
            Tw.mb_4,
            Tw.border,
            Tw.border_color Tw.gray_900, 
            Tw.rounded_lg,
            Tw.bg_color Tw.black]][a[
            href (getWikipediaUrl record),
            target "_blank",
            css [
                  Tw.no_underline,
                  Tw.text_color Tw.gray_900
            ]
        ][
          div[
            css[      
                Tw.flex,
                Tw.flex_row,
                Tw.justify_start
            ]][
        div[
          css[ 
            Tw.border,
            Tw.border_color Tw.gray_900, 
            Tw.rounded,
            Tw.text_color Tw.zinc_100,
            Tw.pr_5
            ]
        ][
           img[src (getWikipediaImageUrl record),
                    width 100,
                    height 100][]],
                   div[
            css[ 
              Tw.text_color Tw.pink_400, 
              Tw.font_serif
              ]
            ][
             h2 [] [
                getWikipediaTitle record
                ]
              ]
                    ] 
          ]]

ratings : Html(msg)
ratings =     div
        [ class "rate"
        ]
        [ input
            [ type_ "radio"
            , id "star5"
            , name "rate"
            , value "5"
            ]
            []
        , label
            [ for "star5"
            , title "text"
            ]
            [ text "5 stars" ]
        , input
            [ type_ "radio"
            , id "star4"
            , name "rate"
            , value "4"
            ]
            []
        , label
            [ for "star4"
            , title "text"
            ]
            [ text "4 stars" ]
        , input
            [ type_ "radio"
            , id "star3"
            , name "rate"
            , value "3"
            ]
            []
        , label
            [ for "star3"
            , title "text"
            ]
            [ text "3 stars" ]
        , input
            [ type_ "radio"
            , id "star2"
            , name "rate"
            , value "2"
            ]
            []
        , label
            [ for "star2"
            , title "text"
            ]
            [ text "2 stars" ]
        , input
            [ type_ "radio"
            , id "star1"
            , name "rate"
            , value "1"
            ]
            []
        , label
            [ for "star1"
            , title "text"
            ]
            [ text "1 star" ]
        ]
    