from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str

class PromptRequest(BaseModel):
    prompt: Optional[str]
    resource_file: Optional[str] = None
