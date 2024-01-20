module Main exposing (..)


import Random
import Browser

import Array 

import Html.Styled exposing (..)
import Html.Styled.Attributes exposing (..)
import Html.Styled.Events exposing (onClick)

import Lenses exposing (..)
import Parser exposing (..)
import Extractors exposing (..)
import HammerEvents exposing (HammerEvent, onSwipe, onSwipeRight)

import Ratings exposing (..)

import Msg exposing (..)
import Model exposing (..)
import WikipediaTypes exposing (..)

import Css
import Tailwind.Theme as Tw
import Tailwind.Utilities as Tw
import Tailwind.Breakpoints as Breakpoints


-- MAIN
main : Program String Model Msg
main = Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view >> toUnstyled
    }

-- INIT
init : String -> (Model, Cmd Msg)
init flags = (
  let wikipediaRecordsArray = Array.fromList(buildWikipediaRecordsList(flags)) in
           {loadDataStatus = (Success wikipediaRecordsArray), 
             currentWikipediaIndex = 0, 
             randomWikipediaIndex = 13, 
             numberOfWikipediaRecords = (Array.length wikipediaRecordsArray)},
  Cmd.none)


-- UPDATE
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Next ->
       (
        if model.currentWikipediaIndex >= model.numberOfWikipediaRecords - 1 
        then modelCurrentWikipediaIndexLens.set 0 model
        else modelCurrentWikipediaIndexLens.set (model.currentWikipediaIndex + 1) model, 
        randomNumberGenerator model
      )
    Previous ->
       (
        if model.currentWikipediaIndex <= 0  
        then modelCurrentWikipediaIndexLens.set (model.numberOfWikipediaRecords - 1) model
        else modelCurrentWikipediaIndexLens.set (model.currentWikipediaIndex - 1) model, 
        randomNumberGenerator model
      ) 
    RandomNumber randomNumber->
       (
        modelRandomWikipediaIndexLens.set randomNumber model, 
        Cmd.none
       )

    GotText result ->
      case result of
        Ok fileText ->
          let wikipediaRecordsArray = Array.fromList(buildWikipediaRecordsList(fileText)) in
          (model 
                 |> modelLoadDataStatusLens.set (Success wikipediaRecordsArray)
                 |> modelNumberOfWikipediaRecordsLens.set (Array.length wikipediaRecordsArray),
            Cmd.none
          )
        Err _ ->
          (
            modelLoadDataStatusLens.set Failure model, 
            Cmd.none
          )

-- Function to generate a random number 
-- between 2 and the number of wikipedia records
randomNumberGenerator : Model -> Cmd Msg
randomNumberGenerator model = 
                 Random.generate RandomNumber (Random.int 2 (model.numberOfWikipediaRecords - 2))


-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none

-- VIEW
view : Model -> Html Msg
view model =
  case model.loadDataStatus of
    Failure ->
      text "Unable to load Wikipedia Data"

    Loading ->
      text "Loading..."

    Success wikipediaRecordsArray ->

      div[css[Tw.bg_color Tw.neutral_950]]
      
      [
      -- header  
      div[ css[Tw.flex, 
              Tw.pl_8, 
              Tw.text_left, 
              Tw.bg_color Tw.custom_blue,
              Tw.py_4,
              Tw.font_serif,
              Tw.text_color Tw.white
             ] ][h1[][text("NerdSwipe")]],
             
      -- main container
      div [css[
            Tw.pt_8,
            Tw.flex, 
            Tw.flex_col, 
            Tw.justify_between]]
      [ 
      -- gallery container
      div[ css [Tw.flex, 
               Tw.flex_row, 
               Tw.justify_between, 
               Tw.bg_color Tw.black,
               Tw.pr_10,
               Tw.pl_10,
          Breakpoints.lg[
            Tw.pr_4,
            Tw.pl_4
          ]] ][
          
        -- previous wikipedia container
          div[
            HammerEvents.onSwipeRight( \_ -> Previous),
            css[Tw.flex, 
                  Tw.items_center,
                  Tw.justify_center]
      ][

        -- previous button
         div[
         css [Tw.z_10,
              Tw.absolute, 
              Tw.transform, 
              Tw.translate_y_0,
              Tw.translate_x_36]          
        ][
            buttonComponent Previous
         ],
      
        -- previous content
         div [ css [Tw.hidden,
               Breakpoints.lg[
                    Tw.block,
                    Tw.opacity_40]
            ] ] [ 
    
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
           img[src (extractWikipediaImageURLFromWikipediaRecord (Array.get (model.currentWikipediaIndex - 1) wikipediaRecordsArray)),
                    width 400,
                    height 400,
                css[
                  Tw.bg_color Tw.white,
                  Tw.border,
                  Tw.border_color Tw.gray_900, 
                  Tw.rounded
                ]][]],
          
          -- wikipedia title (previous)
           div[
            css[ 
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.white, 
              Tw.font_serif
              ]
            ][
             h2 [
              css[ Tw.py_2 ]] [
                extractWikipediaTitleFromWikipediaRecord (Array.get (model.currentWikipediaIndex - 1) wikipediaRecordsArray)
                ]
              ]
          ]
        ],
        
        -- main content
        div [
            css[
            Tw.mb_4, 
            Tw.mt_4
            ]] [ 

          -- wikipedia image  (Main)
          a[
            href (extractWikipediaURLFromWikipediaRecord (Array.get model.currentWikipediaIndex wikipediaRecordsArray)),
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
              Tw.text_color Tw.zinc_100
            ]
          ][
           img[src (extractWikipediaImageURLFromWikipediaRecord (Array.get model.currentWikipediaIndex wikipediaRecordsArray)),
                    width 500,
                    height 500,
            css[
              Tw.bg_color Tw.white,
              Tw.border_8,
              Tw.border_color Tw.gray_900, 
              Tw.rounded
            ]][]]
            ],

          -- wikipedia title (Main)
         div[
            css[ 
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.white, 
              Tw.font_serif
              ]
            ][
             h1 [
              css[Tw.py_2]] [
                extractWikipediaTitleFromWikipediaRecord (Array.get (model.currentWikipediaIndex) wikipediaRecordsArray)
                ]
              ]
        ],
                 
        -- next wikipedia container
        div[ 
          HammerEvents.onSwipeLeft( \_ -> Next),
        css[
                Tw.flex, 
                Tw.items_center,
                Tw.justify_center
            ]
             ][
          -- next button
          div[  css [Tw.z_10,
                  Tw.absolute, 
                  Tw.transform,
                  Tw.translate_x_36, Tw.translate_y_0
              ]][
                buttonComponent Next
         ],
      
        -- next content
        div [
          css [ Tw.hidden,
                Breakpoints.lg[
                Tw.block,
                Tw.opacity_40]
            ]
        ] [ 

        -- wikipedia image (next)
        div[
          css[ 
            Tw.flex, 
            Tw.self_center,
            Tw.justify_center, 
            Tw.text_color Tw.zinc_100
            ]
        ][
           img[src (extractWikipediaImageURLFromWikipediaRecord (Array.get (model.currentWikipediaIndex + 1) wikipediaRecordsArray)),
                    width 400,
                    height 400,
           css[
              Tw.bg_color Tw.white,
              Tw.border,
              Tw.border_color Tw.gray_900, 
              Tw.rounded
            ]
            ][]],
            
           -- wikipedia title (next)
           div[
            css[ 
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.white, 
              Tw.font_serif
              ]
            ][
             h2 [
              css[ Tw.py_2 ]] [
                extractWikipediaTitleFromWikipediaRecord (Array.get (model.currentWikipediaIndex + 1) wikipediaRecordsArray)
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
          Tw.bg_color Tw.neutral_950,
          Tw.pb_6,
        Breakpoints.lg[
          Tw.flex_row,
          Tw.pt_4
          ]
        ]
      ][       
        -- Abstract
        div[
          css [
          Breakpoints.lg[
            Tw.basis_1over4,
            Tw.pl_12
            ]
          ]
        ][         
          div[
            css [
              Tw.pt_4
          ]][
             div[
            css [
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.white, 
              Tw.font_serif
            ]
          ][
            h1[
              css[ Tw.py_2,
                   Tw.pb_4]

            ][
              text("ABSTRACT")
            ]
          ],
          div[css [
                  Tw.text_2xl, 
                  Tw.flex,
                  Tw.justify_center,
                  Tw.self_center,
                  Tw.text_color Tw.white
              ]][
                p[] [extractWikipediaAbstractFromWikipediaRecord (Array.get model.currentWikipediaIndex wikipediaRecordsArray)]
              ]
          ] ,
              -- External Links
          div[
            css [ 
              Tw.hidden,

              Breakpoints.lg[
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.white, 
              Tw.font_serif,
              Tw.py_4]
            ]
          ][
            h1[][text("EXTERNAL LINKS")]
          ]
          ,
          div[
            class "scrollbar",
            css [ 
              Tw.hidden,
                Breakpoints.lg[
                Tw.block,   
                Tw.overflow_y_auto,
                Tw.h_144,
                Tw.flex_row,
                Tw.justify_center,
                Tw.border_4,
                Tw.border_color Tw.black]
            ]

          ][
              ul [] (extractExternalWikipediaLinksFromWikipediaRecord (Array.get model.currentWikipediaIndex wikipediaRecordsArray))
          ]
              ], 

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
        
        -- Ratings
        div[
          css[
            Tw.flex,
            Tw.justify_center,
            Tw.pb_10,
          Breakpoints.lg[
              Tw.pb_5
             ]
          ]
         ][
          ratings
         ],

         -- Categories View  
         div[][
          div[
            css [
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.white, 
              Tw.font_serif,
              Tw.mt_8
            ]
          ][
            h1[
              css[Tw.py_4]
            ][text("CATEGORIES")]
          ],
        div[
          css[
          Tw.flex,
          Tw.justify_center
        ]
      ][
        div[
          class "scrollbar",
            css [
              Tw.overflow_y_auto,        
              Tw.h_144
          ]
          ][
                ul [] (extractWikipediaCategoriesFromWikipediaRecord (Array.get model.currentWikipediaIndex wikipediaRecordsArray))
          ]
        ]
         ]
     ],
      -- Explore View
      div[
          css [ 
          Tw.hidden, 
          Breakpoints.lg
            [
               Tw.block,
               Tw.basis_1over4,
               Tw.pr_12
            ]
          ]
        ][
          div[ 
            css [
              Tw.flex, 
              Tw.justify_center, 
              Tw.text_color Tw.white, 
              Tw.font_serif
            ]][
          h1[
            css[Tw.pt_2, Tw.pb_4]][text("EXPLORE")]
          ],

          -- Generate 5 random Wikipedia Articles
          div[
            css [
              Tw.flex_col,
              Tw.justify_evenly
            ]
          ][
         (createRandomItemElement (Array.get model.randomWikipediaIndex wikipediaRecordsArray)),
         (createRandomItemElement (Array.get (model.randomWikipediaIndex - 1) wikipediaRecordsArray)),
         (createRandomItemElement (Array.get (model.randomWikipediaIndex + 1) wikipediaRecordsArray)),
         (createRandomItemElement (Array.get (model.randomWikipediaIndex - 2) wikipediaRecordsArray)),
         (createRandomItemElement (Array.get (model.randomWikipediaIndex + 2) wikipediaRecordsArray))
          ]
        ]
      ],

      -- footer
      div[][
      div[css[ 
              Tw.bg_color Tw.custom_blue,
              Tw.p_4, 
              Tw.text_center,
              Tw.text_color Tw.white]
      ][
        text("© 2024 NerdSwipe. All Rights Reserved.")
      ]
      ]
      ]
   


-- Create HTML Element for random items
createRandomItemElement : Maybe WikipediaRecord -> Html Msg
createRandomItemElement record =
        div[
          css[
            Tw.pr_6,
            Tw.pl_4,
            Tw.py_2,
            Tw.mb_4,
            Tw.border,
            Tw.border_color Tw.gray_900, 
            Tw.rounded_lg,
            Tw.bg_color Tw.black,
            Css.hover [ Tw.bg_color Tw.custom_blue]
            ]
        ][
          a[
            href (extractWikipediaURLFromWikipediaRecord record),
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
           img[src (extractWikipediaImageURLFromWikipediaRecord record),
               width 100,
               height 100,
               css [Tw.bg_color Tw.white]][]],
          div[
            css[ 
              Tw.text_color Tw.white, 
              Tw.font_serif,
              Css.hover [Tw.text_color Tw.white ]
              ]
            ][
          h2 [] [extractWikipediaTitleFromWikipediaRecord record]
          ]
        ] 
  ]]



buttonComponent: Msg -> Html Msg 
buttonComponent msg = button [onClick msg,  
                  css[
                    Tw.bg_color Tw.custom_blue,
                    Tw.border,
                    Tw.text_color Tw.zinc_100,
                    Tw.border_color Tw.custom_blue, 
                    Tw.rounded,
                    Tw.text_5xl, Tw.cursor_pointer,
                    Tw.px_4, Tw.py_3] ][ 
                case msg of 
                  Next -> i [class "fa-solid fa-chevron-right"][]
                  Previous -> i [class "fa-solid fa-chevron-left"][]
                  _ -> i[][]
                ]

