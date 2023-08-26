// JS binding to read Wikipedia Abstracts output
module ReadFile = {
    [@bs.module "../../../../../../../src/bindings/reader/readFile.js"]
    external readFile: unit => array(string) = "default";
}