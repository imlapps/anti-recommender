module Parser exposing (parseWikipediaJsonl, buildWikipediaRecordsList)

import String exposing (split)
import WikipediaTypes exposing (..)
import Json.Decode exposing (Decoder, at,map2, map4, field, string, decodeString)

-- Main function to parse JSONL
parseWikipediaJsonl : String -> WikipediaRecord
parseWikipediaJsonl wikiString =
      let res = (decodeString wikipediaRecordDecoder wikiString ) in case res of
          Ok record -> record
          Err _ -> WikipediaRecord Nothing Nothing Nothing Nothing


-- Entry point to parse JSONL
buildWikipediaRecordsList: String -> List (WikipediaRecord)
buildWikipediaRecordsList fileText =
                          fileText |> split "\n"
                                   |> List.map(parseWikipediaJsonl)
                                   |> List.filter(filterWikipediaRecords)

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
wikipediaRecordDecoder = map4 WikipediaRecord
                           (Json.Decode.nullable (at ["record","abstract_info"] abstractInfoDecoder))
                           (Json.Decode.nullable (at ["record","sublinks"] (Json.Decode.list sublinkDecoder)))
                           (Json.Decode.nullable (at ["record","categories"] (Json.Decode.list categoryDecoder)))
                           (Json.Decode.nullable (at ["record","externallinks"] (Json.Decode.list externalLinksDecoder)))

-- AbstractInfo Decoder
abstractInfoDecoder : Decoder AbstractInfo
abstractInfoDecoder = 
        map4 AbstractInfo
                  (field "title" string)
                  (field "url" string)
                  (field "abstract" string)
                  (field "image" string)

-- Sublink Decoder
sublinkDecoder : Decoder Sublink 
sublinkDecoder = 
    map2 Sublink 
       (field "anchor" string)
       (field "link" string)

-- Category Decoder
categoryDecoder : Decoder Category
categoryDecoder = 
        map2 Category
        (field "text" string)
        (field "link" string)

-- ExternalLinks Decoder
externalLinksDecoder : Decoder ExternalLink
externalLinksDecoder = 
        map2 ExternalLink
        (field "title" string)
        (field "link" string)