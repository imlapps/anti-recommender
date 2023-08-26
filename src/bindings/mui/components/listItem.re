// JS Binding for Material UI ListItem
[@react.component] [@bs.module "@mui/material/ListItem"]
external make: (
  ~id: string=?,
  ~href: string=?,
  ~button: bool=?,
  ~selected: bool=?,
  ~dense: bool=?,
  ~disableGutters: bool=?,
  ~disablePadding: bool=?,
  ~divider: bool=?,
  ~onClick: unit => unit=?,
  ~component: 'b=?,
  ~className: string=?,
  ~children: React.element=?,
) => React.element = "default";
