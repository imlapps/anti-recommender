// JS Binding for Material UI List
[@react.component] [@bs.module "@mui/material/List"]
external make: (
    ~id: string=?,
    ~className: string=?,
    ~children: array(React.element)=?,
    ~classes: string=?,
    ~component: string=?,
    ~dense: bool=?,
    ~disablePadding: bool=?,
    ~subheader: React.element=?,
  ) => React.element = "default";