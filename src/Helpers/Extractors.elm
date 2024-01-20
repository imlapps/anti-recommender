module Extractors exposing (extractExternalWikipediaLinksFromWikipediaRecord, 
                            extractWikipediaCategoriesFromWikipediaRecord, 
                            extractWikipediaImageURLFromWikipediaRecord, 
                            extractWikipediaSublinksFromWikipediaRecord, 
                            extractWikipediaAbstractFromWikipediaRecord, 
                            extractWikipediaTitleFromWikipediaRecord, 
                            extractWikipediaURLFromWikipediaRecord)

import WikipediaTypes exposing (..)
import Msg exposing (..) 

import CreateElements exposing (..)

import String exposing (split)
import Html.Styled exposing (..)
import Html.Styled.Attributes exposing (..)


-- extract Wikipedia Abstract from Wikipedia Record
extractWikipediaAbstractFromWikipediaRecord : Maybe WikipediaRecord -> Html Msg
extractWikipediaAbstractFromWikipediaRecord record =
        case record of 
        Nothing ->
          text ("Nothing")
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                text("Nothing")
              Just abstract_info ->
                 if ((List.length (split " " abstract_info.abstract)) >= 20) then
                 text(abstract_info.abstract) else text("Not Available")

-- extract Wikipedia Image URL from Wikipedia Record
extractWikipediaImageURLFromWikipediaRecord : Maybe WikipediaRecord -> String 
extractWikipediaImageURLFromWikipediaRecord record = 
        case record of 
        Nothing ->
          ""
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                ""
              Just abstract_info ->
                 abstract_info.image

-- extract Wikipedia Title from Wikipedia Record
extractWikipediaTitleFromWikipediaRecord : Maybe WikipediaRecord -> Html Msg
extractWikipediaTitleFromWikipediaRecord record =
        case record of 
        Nothing ->
          text ("Nothing")
        Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                text ("Nothing")
              Just abstract_info ->
                 text (abstract_info.title)

-- extract Wikipedia URL from Wikipedia Record
extractWikipediaURLFromWikipediaRecord : Maybe WikipediaRecord -> String
extractWikipediaURLFromWikipediaRecord record =
        case record of 
          Nothing ->
            "Nothing"
          Just wikiRecord ->
            case wikiRecord.abstract_info of 
              Nothing ->
                "Nothing"
              Just abstract_info ->
                 abstract_info.url


-- extract Wikipedia Sublinks List from Wikipedia Record
extractWikipediaSublinksFromWikipediaRecord: Maybe WikipediaRecord -> List(Html Msg)
extractWikipediaSublinksFromWikipediaRecord record =
        case record of 
          Nothing ->
            [li [] [a [][text("Nothing")]]]
          Just wikiRecord ->
            case wikiRecord.sublinks of 
              Nothing ->
               [li [] [a [][text("Nothing")]]]
              Just sublinks ->
                (List.map createSublinkItemElement sublinks)

-- extract external Wikipedia Links List from Wikipedia Record
extractExternalWikipediaLinksFromWikipediaRecord: Maybe WikipediaRecord -> List(Html Msg)
extractExternalWikipediaLinksFromWikipediaRecord record =
        case record of 
          Nothing ->
            [li [] [a [][text("Nothing")]]]
          Just wikiRecord ->
            case wikiRecord.external_links of 
              Nothing ->
               [li [] [a [][text("Nothing")]]]
              Just external_links ->
                (List.map createExternalLinkItemElement external_links)


-- extract Wikipedia Category List from Wikipedia Record
extractWikipediaCategoriesFromWikipediaRecord: Maybe WikipediaRecord -> List(Html Msg)
extractWikipediaCategoriesFromWikipediaRecord record =
        case record of 
          Nothing ->
            [li [] [a [][text("Nothing")]]]
          Just wikiRecord ->
            case wikiRecord.categories of 
              Nothing ->
               [li [] [a [][text("Nothing")]]]
              Just categories ->
                (List.map createCategoryItemElement categories)

