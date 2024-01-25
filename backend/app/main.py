from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.records import router 
from app.storage.storage import storage as wikipedia_storage

import os

@asynccontextmanager 
async def lifespan(app: FastAPI):

    file_path = os.getcwd()+"\\app\\data\\mini-wikipedia.output.txt"
    
    wikipedia_storage.read_wikipedia_data(file_path)
    wikipedia_storage.set_current_title(first_title = True)
    
    app.state.wikipedia_storage = wikipedia_storage

    yield 

    app.state.wikipedia_storage.reset()

app = FastAPI(lifespan = lifespan)
app.include_router(router)

@app.get("/")
async def root():
    return app.state.wikipedia_storage.get_current_record()



