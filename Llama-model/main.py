from fastapi import FastAPI

from data_classes import Input
from model import Llama3

model_id = "meta-llama/Meta-Llama-3.1-8B"
model = Llama3(model_id)

with open('prompt.txt', 'r') as file:
    prompt = file.read()
app = FastAPI()


@app.post("/infer/normal")
def read_root(user_input: Input):
    try:
        output = model.get_response(user_input.query, user_input.history, prompt=prompt, temperature=0.5,
                                    max_tokens=512, post_process=True)
        response = output[0]
        raw_response = output[1]
        print(raw_response)
    except Exception as e:
        response = f'An error has occurred with the model,{str(e)}'

    return {"response": response}


@app.post("/infer/unhinged")
def read_root(user_input: Input):
    return {"query": "unhinged"}
