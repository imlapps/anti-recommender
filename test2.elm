    
                Styled.div[][
                -- header
                Styled.div[Attr.css [Tw.flex, 
                                     Tw.pl_8, 
                                     Tw.text_left, 
                                     Tw.text_color Tw.pink_400,
                                     Tw.border_b_8,
                                     Tw.border_color Tw.black,
                                     Tw.bg_color Tw.gray_900,
                                     Tw.bg_radial_gradient
                                     ]]
                                     [Styled.h1[][Styled.text "NerdSwipe"]],
                -- main container
                Styled.div [Attr.css[Tw.flex, Tw.flex_col, Tw.justify_between]]
                [ 

                -- gallery container
                Styled.div[Attr.css [Tw.flex, 
                            Tw.flex_row, 
                            Tw.justify_between, 
                            Tw.bg_color Tw.gray_900,
                            Tw.border_b_8,
                            Tw.border_color Tw.black]][
                
                -- Previous Wikipedia container
                Styled.div[Attr.css[Tw.flex, Tw.items_center]][

                -- Previous Button
                Styled.div[
                  Attr.css [Tw.z_10, Tw.translate_x_20, Tw.translate_y_0]
                ][
                  Styled.button [
                      Attr.type_ "button",
                      Attr.attribute "onClick" Back,
                       Attr.css[
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
                Styled.i [Attr.class "fa-solid fa-chevron-left"][]
                ]
         ]

        -- Previous Content
        -- Styled.div [Attr.css [ 
        --         Tw.flex, 
        --         Tw.flex_row, 
        --         Tw.pr_12,
        --         Tw.opacity_20,
        --         Tw.z_0
        --     ]] [ 

        -- -- Wikipedia Image  
        -- Styled.div[Attr.css[ 
        --     Tw.flex, 
        --     Tw.self_center,
        --     Tw.justify_center, 
        --     Tw.border,
        --     Tw.border_color Tw.gray_900, 
        --     Tw.rounded,
        --     Tw.text_color Tw.zinc_100
        --     ]
        --     ][
        --    Styled.img[Attr.src (getWikipediaImageUrl (Array.get (model.index - 1) wikipediaRecordsArray)),
        --             Attr.width 400,
        --             Attr.height 400][]],
        --    Styled.div[Attr.css
        --     [ Tw.flex, 
        --       Tw.text_color Tw.pink_400, 
        --       Tw.justify_center,
        --       Tw.font_serif
        --     ]][
        --         Styled.h1 [] [
        --         Styled.text (getWikipediaTitle (Array.get (model.index - 1) wikipediaRecordsArray))
        --         ]]    
        --   ]
        ],  



           -- Main Content
        Styled.div [
             Attr.css[ Tw.flex
            , Tw.flex_col
            , Tw.mb_4
            , Tw.mt_4
            ]
            ] [ 

            -- Wikipedia Image  
        Styled.a[
            Attr.href (getWikipediaUrl (Array.get model.index wikipediaRecordsArray)),
            Attr.target "_blank",
            Attr.css[
              Tw.no_underline
            ]
        ][
            Styled.div[
              Attr.css[ 
                Tw.flex, 
                Tw.self_center,
                Tw.justify_center, 
                Tw.border,
                Tw.border_color Tw.gray_900, 
                Tw.rounded,
                Tw.text_color Tw.zinc_100
            ]
              
            ][
           Styled.img[Attr.src (getWikipediaImageUrl (Array.get model.index wikipediaRecordsArray)),
                    Attr.width 500,
                    Attr.height 500][]]
            ]
        ],
              -- alternative wikipedia container
                Styled.div[Attr.css[Tw.flex, Tw.items_center]][

                -- next button (Z-index should be 1)
                Styled.div[Attr.css [Tw.z_10, Tw.translate_x_64]][
                Styled.button [
                Attr.attribute "onclick" "Next",
                Attr.css [
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
                Styled.i [Attr.class "fa-solid fa-chevron-right"][]
                ]
         ],

        -- Next Content
        Styled.div [Attr.css [ 
                Tw.flex, 
                Tw.flex_row, 
                Tw.pr_12,
                Tw.opacity_20
            ]] [ 

        -- Wikipedia Image  
        Styled.div[Attr.css[ 
            Tw.flex, 
            Tw.self_center,
            Tw.justify_center, 
            Tw.border,
            Tw.border_color Tw.gray_900, 
            Tw.rounded,
            Tw.text_color Tw.zinc_100,
            Tw.z_0
            ]
            ][
           Styled.img[Attr.src (getWikipediaImageUrl (Array.get (model.index - 1) wikipediaRecordsArray)),
                    Attr.width 400,
                    Attr.height 400][]],
           Styled.div[Attr.css
            [ Tw.flex, 
              Tw.text_color Tw.pink_400, 
              Tw.justify_center,
              Tw.font_serif
            ]][
                Styled.h1 [] [
                Styled.text (getWikipediaTitle (Array.get (model.index - 1) wikipediaRecordsArray))
                ]]    
          ]]
       
      --   Styled.div[class "alt-wikipedia-container"][
        
      --   -- Next Button
      --   Styled.div [class "next-button-container"] [

      --       Styled.button [onClick Next, class "button"
      --               ] [ 
      --              Styled.i [class "fa-solid fa-chevron-right"][] 
      --                 ]
      --     ],

      --   -- Next Content
      --   Styled.div [
      --         class "next-wikipedia-content"
      --       ] [ 

      --   -- Wikipedia Image  

      --   Styled.div[class "wikipedia-image"][
      --      Styled.img[src (getWikipediaImageUrl (Array.get (model.index + 1) wikipediaRecordsArray)),
      --               width 400,
      --               height 400][]],
      --                             Styled.div[class "wikipedia-title"][
      --           Styled.h1 [] [
      --           getWikipediaTitle (Array.get (model.index + 1) wikipediaRecordsArray)
      --           ]]    
        

      --     ]]
      --   ],

      -- -- Additional Content
      -- Styled.div[class "additional-content"][
      --       Styled.div[][],
      --       Styled.div[class "descriptive-content "][

      --         -- Wikipedia Title
      --         Styled.a[
      --           Attr.href (getWikipediaUrl (Array.get model.index wikipediaRecordsArray)),
      --           Attr.target "_blank",
      --           class "wikipedia-url"
      --         ][
      --         Styled.div[class "wikipedia-title"][
      --           Styled.h1 [] [
      --           getWikipediaTitle (Array.get model.index wikipediaRecordsArray)
      --           ]]
      --       ],
              
      --       -- Wikipedia Abstract
      --       Styled.div[class "wikipedia-abstract"][
      --           Styled.p[] [getWikipediaAbstract (Array.get model.index wikipediaRecordsArray)]
      --         ]
            
            -- Styled.div[class "wiki-content-category"][

            --   -- Categories List
            --   Styled.div[class "categories"][                                  
            --     input[type_ "checkbox", id  "wikipedia-categories"][],
                
            --     label[for "wikipedia-categories"][
            --           i [class "fa-solid fa-bars",
            --              class "bars-icon-categories"][], 
            --             text("Categories"),
            --           i [class "fa-solid fa-chevron-down", 
            --              class "chevron-icon-categories"][]],
            --     ul [] (getWikipediaCategories (Array.get model.index wikipediaRecordsArray))
            --   ]
            --       ]
                                 
      ]
          ]
               
                ]