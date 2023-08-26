// JS Binding for Material UI Box
[@react.component] [@bs.module "@mui/material/Box"]
external make: (
  ~id: string=?,
  ~component: string=?,
  ~bgcolor: string=?,
  ~color: string=?,
  ~p: int=?,
  ~m: int=?,
  ~mt: int=?,
  ~className: string=?,
  ~id: string=?,
  ~children: React.element,
) => React.element = "default"