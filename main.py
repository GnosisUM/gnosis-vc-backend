from fastapi import FastAPI
from database import supabase
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/gnosis")
async def root():
    return {"message": "Hello Gnosis"}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/read_connection")
async def read_connection():
    data = supabase.table("startup_scrap").select("*").execute()
    return data