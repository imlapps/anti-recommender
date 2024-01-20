module Ratings exposing (ratings)

import Html.Styled exposing (..)
import Html.Styled.Attributes exposing (..)

-- HTML Element for a 5-Star rating scale
ratings : Html(msg)
ratings =  div
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
    