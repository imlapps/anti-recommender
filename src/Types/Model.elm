module Model exposing (..)


import WikipediaTypes exposing (..)
import Array exposing (Array)

-- MODEL
type LoadDataStatus = Failure | Loading | Success (Array WikipediaRecord)
type alias Model =  
                  {  
                    loadDataStatus: LoadDataStatus
                   , currentWikipediaIndex: Int
                   , randomWikipediaIndex: Int
                   , numberOfWikipediaRecords: Int
                  }