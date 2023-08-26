import wikipediaOutput from "./storage/mini_wikipedia.out.jsonl";

// Read and parse the Wikipedia Abstracts output from local Storage
export default function readFile(){
    const wikipediaStream = wikipediaOutput.trim().split("\n");
    let parsedData = [];

    for(var jsonl of wikipediaStream){
        
        const parsedJsonl = JSON.parse(jsonl);
        if(parsedJsonl.type === "RECORD")
        {
            parsedData.push(JSON.stringify(parsedJsonl.record));
        }
    }

    return parsedData;
}