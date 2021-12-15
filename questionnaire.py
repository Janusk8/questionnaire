from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
import csv
from random import choices

df = pd.read_csv('/home/ubuntu/FastAPI/exercice/questions.csv' , sep = ',', header = 0)

users = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}

class Question(BaseModel):
    libelle: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: Optional[str]
    responseD: Optional[str]
    remark: Optional[str]

class Questionnaire(BaseModel):
    use: str
    subject: List[str]
    nb_questions: int

api = FastAPI(
    title="Questionnaires API",
    description="API de creation de QCMs de 5, 10 ou 20 questions",
    version="1.0.1",
    openapi_tags=[
    {
        'name': 'Home',
        'description': 'Default functions'
    },
    {
        'name': 'Questions',
        'description': 'Functions that are used to deal with questions'
    }
    ]
)

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    for key, value in users.items():
        if credentials.username==key and credentials.password==value:
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )

def get_admin_username(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username=='admin' and credentials.password=='4dm1N':
        return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    
@api.get('/status', name='Get API status', tags=['Home'])
def get_status(username: str = Depends(get_current_username)):
    """Cette fonction renvoie 1 si l'API fonctionne.
    """
    return 1

@api.post('/questions', name='Post questions', tags=['Questions'])
def post_questions(questionnaire: Questionnaire, username: str = Depends(get_current_username)):
    """Cette fonction renvoie une série de questions.\n
        USE : Test de positionnement / Test de validation / Total Bootcamp\n
        SUBJECT : Automation / BDD / Classification / Data Science / Docker / Machine Learning / Streaming de données / Systèmes distribués\n
        NB_QUESTIONS : 5, 10 ou 20
    """
    try:
        data=df[(df['use'] == questionnaire.use)]
        data=data[data['subject'].isin(questionnaire.subject)]
        data=data.sample(questionnaire.nb_questions)
        data_jason=data.to_json(orient='records')
        return data_jason
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )

@api.post('/question', name='Post new question', tags=['Questions'])
def post_question(question: Question, username: str = Depends(get_admin_username)):
    """Cette fonction permet a un utilisateur admin de créer une nouvelle question
    """
    global df
    try:
        new_question = {
            'libelle': question.libelle,
            'subject': question.subject,
            'use': question.use,
            'correct': question.correct,
            'responseA': question.responseA,
            'responseB': question.responseB,
            'responseC': question.responseC,
            'responseD': question.responseD,
            'remark': question.remark
        }
        df=df.append(new_question,ignore_index=True)
        return new_question

    except IndexError:
        return {}

