from fastapi import FastAPI, Request
from database import supabase

# import AI dependencies
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_predict
import json

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

@app.post("/get_AI_rating")
async def get_AI_rating(request: Request):
    data = await request.json()
    startupList = data.get('startupList')
    print(startupList)
    model = pickle.load(open('./assets/RFClassifier.pkl', 'rb'))
    # X = pd.read_csv('./assets/mock_csv.csv')
    # 34 features
    dfs = []
    for startup in startupList:
        df = pd.DataFrame(startup)
        dfs.append(df)
    X = pd.concat(dfs, axis=0)

    prediction = model.predict(X)
    return {'prediction':np.array(prediction).tolist()}