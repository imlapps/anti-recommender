module CreateElements exposing (createCategoryItemElement,
                                createExternalLinkItemElement,
                                createSublinkItemElement)


import WikipediaTypes exposing (..)

import Html.Styled exposing (..)
import Html.Styled.Attributes exposing (..)

import Css
import Tailwind.Utilities as Tw
import Tailwind.Theme as Tw

-- extract Sublink Item from Sublink List and create HTML element
createSublinkItemElement : Sublink -> Html msg
createSublinkItemElement sublink = 
        a [href sublink.link, target "_blank",
                              css [
                  Tw.no_underline,
                  Tw.text_color Tw.gray_900
            ]] [ li [
        css[ 
              Tw.block,
              Tw.text_xl
            , Tw.bg_color Tw.black
            , Tw.text_color Tw.white
            , Tw.rounded
            , Tw.px_2
            , Tw.py_4
            , Tw.my_0_dot_5
            , Tw.font_serif
            , Css.hover [ Tw.bg_color Tw.custom_blue, Tw.text_color Tw.white ],
            Tw.mr_1
            , Css.lastChild
                [ Tw.mr_0
                ]
          ]
        ][ text (( sublink.anchor)) ]]



-- extract ExternalLink Item from Sublink List and create HTML element
createExternalLinkItemElement : ExternalLink -> Html msg
createExternalLinkItemElement externallink = 
        a [href externallink.link, target "_blank",
                              css [
                  Tw.no_underline,
                  Tw.text_color Tw.gray_900
            ]] [ li [
        css[ 
              Tw.block,
              Tw.text_xl
            , Tw.bg_color Tw.black
            , Tw.text_color Tw.white
            , Tw.rounded
            , Tw.px_2
            , Tw.py_4
            , Tw.my_0_dot_5
            , Tw.font_serif
            , Css.hover [ Tw.bg_color Tw.custom_blue],
            Tw.mr_1
            , Css.lastChild
                [ Tw.mr_0
                ]
          ]
        ][ text (( externallink.title)) ]]




-- extract Category Item from Category List and create HTML element
createCategoryItemElement : Category -> Html msg
createCategoryItemElement category = 

          a [href ("https://en.wikipedia.org/" ++ category.link), target "_blank",
                      css [
                  Tw.no_underline,
                  Tw.text_color Tw.gray_900
            ]] 
          [ li [
          css[ 
              Tw.block,
              Tw.text_xl
            , Tw.font_serif
            , Tw.bg_color Tw.black
            , Tw.text_color Tw.white
            , Tw.rounded
            , Tw.px_2
            , Tw.py_4
            , Tw.my_0_dot_5
            , Css.hover [ Tw.bg_color Tw.custom_blue],
            Tw.mr_1
            , Css.lastChild
                [ Tw.mr_0
                ]
          ]
          ][ text ((category.text))]]