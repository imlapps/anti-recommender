module Button exposing (..)

import Msg exposing (..) 

import Html.Styled exposing (..)
import Html.Styled.Attributes exposing (..)
import Html.Styled.Events exposing (onClick)

import Tailwind.Theme as Tw
import Tailwind.Utilities as Tw

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
