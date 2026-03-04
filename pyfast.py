from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    id:str
    name:str

app=FastAPI()
@app.get('/',response_model=User)
def home():
    return User(id='12s',name='Manya')

if(__name__=="__main__"):
    import uvicorn
    uvicorn.run("pyfast:app",port=4000,reload=True)
