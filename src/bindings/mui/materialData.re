/*Access point for Material UI modules */
open Components;

module Button = Button;
module Box = Box;
module Container = Container;
module Typography = Typography;
module List = List;
module ListItem = ListItem;
module ListItemText = ListItemText;


module ThemeProvider = {
  // JS Binding for Material UI ThemeProvider
  [@react.component] [@bs.module "@mui/material/styles"]
  external make: (~theme: Js.Dict.t<string>=?, ~children: React.element) => React.element =
    "ThemeProvider"
};

// JS Binding for Material UI Styles
[@bs.module "@mui/material/styles"]
external createTheme: Js.Dict.t<'a> => Js.Dict.t<string> = "createTheme";


