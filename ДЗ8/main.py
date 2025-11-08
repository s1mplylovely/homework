import uvicorn
import re
import json
from pydantic import BaseModel, model_validator
from fastapi import FastAPI, Response
from datetime import date, datetime
from typing import List

app = FastAPI()


class User(BaseModel):
    surname: str
    name: str
    birthday: date = 'YYYY-mm-dd'
    phone_number: str
    email: str = 'user@example.com'
    reason: List[str] = [
        "Нет доступа к сети",
        "Не работает телефон",
        "Не приходят письма",
    ]
    date: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @model_validator(mode="after")
    def validate_surname(self):
        if not self.surname[0].isupper():
            raise ValueError("Surname error: low first letter")
        valid = re.match(r"[А-ЯЁа-яё]+$", self.surname)
        if not valid:
            raise ValueError("Surname error: must by cyrillic")
        return self

    @model_validator(mode="after")
    def validate_name(self):
        if not self.name[0].isupper():
            raise ValueError("Name error: low first letter")
        valid = re.match(r"[А-ЯЁа-яё]+$", self.name)
        if not valid:
            raise ValueError("Name error: must by cyrillic")
        return self

    @model_validator(mode="after")
    def validate_email(self):
        valid = re.match(
            r"(^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email)
        if valid:
            return self
        else:
            raise ValueError("Email error")


@app.post("/appeals")
async def post_appeal(model: User):
    to_file(dict(model))
    return model.model_dump()


def to_file(data: dict):
    id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name = f"appeal_{id}.json"
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, default=str)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
