module Lenses exposing (..)

import Model exposing (..)
import Monocle.Lens exposing (Lens)

-- Lenses

-- Lens for the model's currentWikipediaIndex field
modelCurrentWikipediaIndexLens : Lens Model Int
modelCurrentWikipediaIndexLens = 
     Lens .currentWikipediaIndex (\b a -> { a | currentWikipediaIndex = b})

-- Lens for the model's randomWikipediaIndex field
modelRandomWikipediaIndexLens : Lens Model Int
modelRandomWikipediaIndexLens = 
     Lens .randomWikipediaIndex (\b a -> { a | randomWikipediaIndex = b})

-- Lens for the model's numberOfWikipediaRecords field
modelNumberOfWikipediaRecordsLens : Lens Model Int
modelNumberOfWikipediaRecordsLens = 
     Lens .numberOfWikipediaRecords (\b a -> { a | numberOfWikipediaRecords = b})

-- Lens for the model's loadDataStatus field
modelLoadDataStatusLens : Lens Model LoadDataStatus
modelLoadDataStatusLens =
     Lens .loadDataStatus (\b a -> { a | loadDataStatus = b})

