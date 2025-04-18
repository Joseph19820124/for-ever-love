from pydantic import BaseModel

class MathInput(BaseModel):
    a: int
    b: int
