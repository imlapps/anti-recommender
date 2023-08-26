type info = {
  title: string,
  abstract: string,
  url: string
};

type sublinkInfo = {
anchor: string,
link: string
};

type wikipediaObj = {
  abstractInfo: info,
  sublinks: array(sublinkInfo)
};

/* Main module to decode the Wikipedia JSON data*/
module Decode = {
  let abstractInfoObj = json => 
    Json.Decode.{
        title: json |> field("title", string),
        abstract: json |> field("abstract", string),
        url: json |> field("url", string),
    };
  
  let sublinkObj = json => 
    Json.Decode.{
        anchor: json |> field("anchor", string),
        link: json |> field("link", string)
  };
  
  let wikipediaObj = (json) =>
      Json.Decode.{
        abstractInfo: json |> field("abstract_info", abstractInfoObj),
        sublinks: json |> field("sublinks", array(sublinkObj))
      };
  
};

/* Entry point to decode the Wikipedia JSON data*/
module DecodeWikipediaJson = {

let decodedWikipediaObj = value => {
 value |> Json.parseOrRaise
       |> Decode.wikipediaObj};

let decodedSublinkObj = value => {
 value |> Json.parseOrRaise
       |> Decode.sublinkObj};

let decodedData = (data: array(string)) => {
  data |> Array.map(decodedWikipediaObj);
};

};