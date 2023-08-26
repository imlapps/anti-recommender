// JS Binding for Material UI ListItemText
[@react.component] [@bs.module "@mui/material/ListItemText"]
external make: (
    ~id: string=?,
    ~className: string=?,
    ~primary: string=?,
    ~secondary: string=?,
    ~inset: bool=?,
    ~disableTypography: bool=?,
    ~primaryTypographyProps: Js.t<'a>=?,
    ~secondaryTypographyProps: Js.t<'a>=?,
    ~children: React.element=?,
  ) => React.element = "default";
