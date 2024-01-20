module Msg exposing (..)

-- Msg type for UPDATE
type Msg
  = GotText (Result String String) 
    | Next 
    | Previous
    | RandomNumber Int
