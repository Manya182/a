from pydantic import BaseModel,Field

class Employee(BaseModel):
    id:int=Field(...,description='Enter id',gt=0)
    name:str
    department:str
    age:int

