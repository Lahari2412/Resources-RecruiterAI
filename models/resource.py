from pydantic import BaseModel

class Resource(BaseModel):
    #id: int 
    job_id: int
    job_description: str
    skills:str
    qualification:str
    experience: str
    resources:str




