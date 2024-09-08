from fastapi import FastAPI
from pydantic import BaseModel

from model import Llama3

model_id = "meta-llama/Meta-Llama-3.1-8B"
model = Llama3(model_id)


class Query(BaseModel):
    query: str


app = FastAPI()


@app.post("/infer/normal")
def read_root(query: Query):
    try:
        output = model.get_response(query.query, temperature=0.5, post_process=True)
        response = output[0]
        raw_response = output[1]
        print(raw_response)
    except Exception as e:
        response = f'An error has occurred with the model,{str(e)}'

    return {"response": response}


@app.post("/infer/unhinged")
def read_root(query: Query):
    return {"query": "unhinged"}
