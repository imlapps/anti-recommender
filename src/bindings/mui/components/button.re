open Datatypes.MaterialUIDataType;

module Variant: {
  type t
  let text: t
  let outlined: t
  let contained: t
} = {
  type t = string
  let text = "text"
  let outlined = "outlined"
  let contained = "contained"
};

// JS Binding for Material UI Button
[@react.component] [@bs.module "@mui/material/Button"]
external make: (
  ~id: string=?,
  ~children: React.element=?,
  ~className: string=?,
  ~color: NoTransparentColor.t=?,
  ~component: string=?,
  ~disabled: bool=?,
  ~disableElevation: bool=?,
  ~disableFocusRipple: bool=?,
  ~disableRipple: bool=?,
  ~endIcon: React.element=?,
  ~fullWidth: bool=?,
  ~href: string=?,
  ~size: Size.t=?,
  ~startIcon: React.element=?,
  ~variant: Variant.t=?,
  ~onClick: ReactEvent.Synthetic.t => unit=?,
  ~_type: string=?,
  ~ref: 'a=?,
) => React.element = "default";
