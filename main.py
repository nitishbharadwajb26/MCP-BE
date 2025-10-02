from fastapi import FastAPI, UploadFile, File
from typing import List
from models import User, PromptRequest
from storage import load_users, add_user, find_users
from llm_integration import call_mistral
import shutil
import os

app = FastAPI()

@app.post("/create-user")
def create_user(user: User):
    add_user(user)
    return {"message": "User created successfully", "user": user}

@app.get("/list-users", response_model=List[User])
def list_users():
    return load_users()

@app.post("/prompt-resource")
async def prompt_resource(prompt_req: PromptRequest):
    resource_path = None
    # if file:
    #     os.makedirs("resources", exist_ok=True)
    #     resource_path = f"resources/{file.filename}"
    #     with open(resource_path, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)

    result = call_mistral(prompt_req.prompt)
    print('Print of LLM result', result)

    if result.get("create_user"):
        print("User data for creation", result["data"])
        user = add_user(result["data"])
        return {"action": "create_user", "user": user}

    elif result.get("list_user"):
        print("User data for list", result["data"])
        users = find_users(result["data"])
        return {"action": "list_user", "users": users}

    else:
        return {"action": "none", "response": result}
