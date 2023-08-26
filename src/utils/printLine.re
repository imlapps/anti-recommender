/*
   A simple module to print a list to console.
   TODO: Get this working for Wikipedia Records.
*/

// module type Stringable = {
//   type t;
//   let toString: (t) => string;
// };

// module Printer = (Item: Stringable) => {
//   let print = (t: Item.t) => {
//     print_endline(Item.toString(t));
//   };

//   let printList = (list: list(Item.t)) => {
//     list
//     |> List.map(Item.toString)
//     |> String.concat(", ")
//     |> print_endline;
//   };
// };

// module IntPrinter = Printer({
//   type t = DecodeJson.obj;
//   let toString = (t: DecodeJson.obj) => t.name;
// });