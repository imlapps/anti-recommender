// JS Binding for Material UI Container
[@react.component] [@bs.module "@mui/material/Container"]
external make: (
  ~id: string=?,
  ~maxWidth: 'a=?,
  ~component: string=?,
  ~className: string=?,
  ~children: React.element,
) => React.element = "default"