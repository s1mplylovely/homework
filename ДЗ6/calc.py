import uvicorn
from typing import Dict
from pydantic import BaseModel
from fastapi import FastAPI


app = FastAPI()


class Nums(BaseModel):
    nums: Dict[str, int] = {
        'a': 0,
        'b': 0,
        'c': 0,
        'd': 0,
        'e': 0,
        'f': 0,
        'g': 0
    }


@app.get("/add")
async def add(a: int | float, b: int | float):
    return {"res": a+b}


@app.get("/subtract")
async def subtract(a: int | float, b: int | float):
    return {"res": a-b}


@app.get("/multiply")
async def multiply(a: int | float, b: int | float):
    return {"res": a*b}


@app.get("/divide")
async def divide(a: int | float, b: int | float):
    return {"res": a/b}


@app.post("/calculate")
async def calculate(model: Nums, op: str):
    allowed_chars = set(
        'abcdefghijklmnopqrstuvwxyz0123456789+-*/().^ ')
    if not all(x in allowed_chars for x in op):
        return {"res": "Выражение содержит запрещенные символы"}
    op = op.replace('^', '**')
    for k in model.nums.keys():
        op = op.replace(k, str(model.nums[k]))
    return {"res": eval(op)}

if __name__ == "__main__":
    uvicorn.run("calc:app", reload=True)
