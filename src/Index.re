/* Main ReasonReact File */

open Mui.MaterialData;
open Parser;
open Reader;

type root;

// JS binding for ReactDOM.createRoot()
[@bs.module "react-dom/client"]
external createRoot: Dom.element => root = "createRoot";

// JS Binding for ReactDOM.createRoot.render()
[@bs.send] external render: (root, React.element) => unit = "render";

module App = {

let file = ReadFile.ReadFile.readFile(); // Read in JSON Data
let parsedWikipediaData = DecodeJson.DecodeWikipediaJson.decodedData(file); // Decode JSON 

[@react.component]
let make = () => {

// React Hook to define a state that keeps track of parsedWikipediaData's index 
let (index, setIndex) = React.useState(() => 0);

// React Hook to cache the result of the current wikipediaData record 
let wikipediaData = React.useMemo2(() => parsedWikipediaData[index], (index, parsedWikipediaData));

// Handler to increment the index of the parsedWikipediaData array
let setNext = () => {
  if(index + 1 < Array.length(parsedWikipediaData))
  {
    setIndex(_  => index + 1)
  } else {
    setIndex(_ => 0)
  };
};

// Handler to decrement the index of the parsedWikipediaData array
let setBack = () => {
    if(index> 0)
    { 
      setIndex(_ => index - 1)
    } else {
      setIndex(_ => Array.length(parsedWikipediaData)-1)
    };
};


// Main react component
<div>
    <Container component="main" maxWidth="xs">  
    <Button>{React.string("")}</Button> // Temp solution to make UI look better

    <Typography component="h1" variant=Typography.Variant.h6>
    <p>{React.string(wikipediaData.abstractInfo.title)}</p>
    </Typography>
    
    <p>{React.string(wikipediaData.abstractInfo.url)}</p>
    <p>{React.string(wikipediaData.abstractInfo.abstract)}</p>
    </Container>

    <Container component="main" maxWidth="xs">
    <Button variant=Button.Variant.contained onClick = {(_) => {setBack()}}>
         {React.string("Back")} 
    </Button>
    <Button>{React.string("")}</Button> // Temp solution to make UI look better
    <Button variant=Button.Variant.contained onClick = {(_) => {setNext()}}>
           {React.string("Next")} 
    </Button>
    </Container>
    
    <Container component="main" maxWidth="xs">
    <Button>{React.string("")}</Button> // Temp solution to make UI look better
    <List>
    {wikipediaData.sublinks|> 
      Array.map((value: DecodeJson.sublinkInfo) => {
      <ListItem  button=true disablePadding=true divider=true>
        <ListItemText primary={value.anchor}/>
      </ListItem>
    })}
    </List>
    </Container >
  </div>
};
};

ReactDOM.querySelector("#root")
->(
    fun
    | Some(root) => {
      let app = createRoot(root);
      render(app, <App/>);
    }
    | None =>
      Js.Console.error(
        "Failed to start React: couldn't find the #root element",
      )
  );