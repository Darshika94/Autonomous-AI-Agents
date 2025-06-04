from fastapi import FastAPI, Request
from agent_logic import process_transaction
from storage_sqlite import init_db
from access_control import verify_token  # 🔐 Import JWT checker

app = FastAPI()
init_db()

@app.get("/")
def welcome():
    return {"msg": "Compliance Agent is Running"}

@app.post("/check")
async def check(request: Request):
    data = await request.json()
    token = data.get("token")

    # ✅ Extract role from JWT token
    role = verify_token(token)
    if not role:
        return {"result": "Access Denied: Invalid or Expired Token"}

    # 🚀 Pass role into agent logic (if needed)
    result = process_transaction(data["txn"], token)
    return {"result": result}
