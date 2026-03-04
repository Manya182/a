from fastapi import FastAPI,Path ,HTTPException,Query
import json
from pydantic import BaseModel,Field,field_validator,model_validator,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal,Optional
app=FastAPI()
# @app.get("/")
class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ENter patient id',examples=['P001'])]
    name:Annotated[str,Field(...,description='Enter your name',examples=['Manya','Buddy'])]
    city:Annotated[str,Field(...,description='ENter City name')]
    age:Annotated[int,Field(...,description=('Enter age'))]
    gender:Annotated[Literal['male','female','others'],Field(...,description='ENter gender',examples=['female','male'])]
    height:Annotated[float,Field(...,description='Enter height in metres')]
    weight:Annotated[float,Field(...,description='Enter weight in kgs')]
    @field_validator('age')
    @classmethod
    def validate_age(cls,ag):
        if ag<=0 or ag>120:
            raise ValueError('Age must be within range 0-120')
        return ag
    @field_validator('height')
    @classmethod
    def validate_height(cls,hg):
        if hg<=0 :
            raise ValueError('Age must be within range 0-120')
        return hg
    @field_validator('weight')
    @classmethod
    def validate_weight(cls,wt):
        if wt<=0 :
            raise ValueError('Age must be within range 0-120')
        return wt
    
    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)
    @computed_field
    @property
    def verdict(self)->str:
        if(self.bmi<=18.5):
            return 'Underweight'
        elif(self.bmi>18.5 and self.bmi<=25):
            return 'Normal'
        elif(self.bmi>25 and self.bmi<30):
            return 'Overweight'
        else:
            return 'Obese'





def load_data():
    with open('patients.json','r') as f:
        print(f)
        data= json.load(f)  #json file ko read krne k lie and use py object conversion
    return data
def save_data(data):
    with open("patients.json",'w') as f:
        json.dump(data,f)
@app.get('/')
def hello():
    return {'message':'Patient Management System API'}

@app.get("/about")
def tell():
    return {'message':'A fully functional API to manage your patient records'}
@app.get('/view')
def view():
    data=load_data()
    return data
@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='ID of patient in db',example='P001',title='jhgjh')):
    data=load_data()
    if(patient_id in data):
        return data[patient_id]
    else:
         raise HTTPException(status_code=404,detail="Patient not found in db")
@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='Sort on the basis of height, bmi, weight'),order:str=Query('asc',description='sort in asc or desc order')):
    valid_fields=['height','bmi','weight']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail='invalid parameter')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='invalid param')
    data=load_data()
    sort_data=sorted(data.values(),key=lambda x: x[sort_by],reverse=True if order=='desc' else False)
    return sort_data

@app.get('/k/{patient_id}')
def querpath(patient_id:str=Path(...,description='this is the patient to be fetched'),filter:str=Query('',description='The specific data you want')):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found in db')
    patdata=data[patient_id]
    if filter=='':
        return patdata
    if filter not in ['age','bmi','weight']:
        raise HTTPException(status_code=400,detail='choose better parameter')

    return {filter: patdata[filter]}

@app.post('/create')
def create_patient(pt:Patient):
    data=load_data()
    if(pt.id in data):
        raise HTTPException(status_code=400,detail='Patient already exists')
    data[pt.id]=pt.model_dump(exclude=['id']) #converts pydantic object to python dictionary
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'Patient created successfully'})
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None,description='Enter your name',examples=['Manya','Buddy'])]
    city:Annotated[Optional[str],Field(default=None,description='ENter City name')]
    age:Annotated[Optional[int],Field(default=None,description=('Enter age'))]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None,description='ENter gender',examples=['female','male'])]
    height:Annotated[Optional[float],Field(default=None,description='Enter height in metres')]
    weight:Annotated[Optional[float],Field(default=None,description='Enter weight in kgs')]
    @field_validator('age')
    @classmethod
    def validate_age(cls,ag):
        if ag<=0 or ag>120:
            raise ValueError('Age must be within range 0-120')
        return ag
    @field_validator('height')
    @classmethod
    def validate_height(cls,hg):
        if hg<=0 :
            raise ValueError('Age must be within range 0-120')
        return hg
    @field_validator('weight')
    @classmethod
    def validate_weight(cls,wt):
        if wt<=0 :
            raise ValueError('Age must be within range 0-120')
        return wt
    
    
         
        
@app.put('/edit/{patient_id}')
def update_details(patient_id:str,patup:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=400,detail='Patient doesnt exist')   
    existing_patient=data[patient_id]
    newdat=patup.model_dump(exclude_unset=True)
    for k in newdat.keys():
        existing_patient[k]=newdat[k]
    #ye krne s pehle we need to update the bmi and verdict as well based on the new values
    #so existing_patient_info->pydantic ob->update bmi->pyd ob->dict
    existing_patient['id']=patient_id
    dt=Patient(**existing_patient) #unpacks the dict , for eg. {name:"many",age:12}-> Patient(name="Many",age=12)
    updt_data=dt.model_dump(exclude='id')

    data[patient_id]=updt_data
    save_data(data)
    return JSONResponse(status_code=203,content='Updated')

@app.delete('/del/{patient_id}')
def del_pat(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=400,detail='Patient doesnt exist') 
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=203,content='Updated')


    

