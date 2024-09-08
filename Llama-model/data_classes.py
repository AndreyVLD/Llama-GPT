from pydantic import BaseModel


class Message(BaseModel):
    content: str
    sender: str

    def __str__(self):
        return f'- {self.sender}: {self.content}\n'


class Input(BaseModel):
    query: str
    history: list[Message] = []
