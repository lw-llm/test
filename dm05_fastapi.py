# from fastapi import FastAPI
# app=FastAPI(title="EduAgent Demo")
# @app.get("/health")
# async def health_check():
#     return {"state":"ok"}
#
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app,host='127.0.0.1',port=8000)
import asyncio

from fastapi import FastAPI,Depends
from pydantic import BaseModel,Field
app=FastAPI()
# 1. 请求体模型：前端要发来的数据
class LoginRequest(BaseModel):
    username:str=Field(...,description="用户名或邮箱")
    password:str=Field(...,description="密码")
# 2. 响应 模型：我们要返回的数据样式
class TokenResponse(BaseModel):
    access_token:str
    token_type:str="bearer"
    role:str
@app.post("/login",response_model=TokenResponse)
async def login(req:LoginRequest):
    # req 已经是解析并校验好的对象，直接用req.username / req.password
    if req.username=="student01" and req.password=="1234567890":
        return TokenResponse(access_token="hhhh-gggg-kkk",role="student")
    return {"access_token":"","token_type":"bearer","role":"guest"}

@app.get("/reviews/{review_id}")
async def get_review(review_id: str):
    return {"review_id": review_id, "content": "This is a sample review."}

@app.get("/reviews")
async def list_reviews(page: int = 1, page_size: int = 10):
    return {"page": page, "page_size": page_size, "reviews": []}

# 这里我们使用文档中的 get_current_user 模拟版本。
async def get_db():
    return {"db": "fake_session"}

# 模拟的当前用户（不校验 Token，直接返回）
async def get_current_user():
    return {"user_id": "test_user", "role": "student"}

@app.get("/my-reviews")
async def my_reviews(
    db = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # return {"user": current_user["user_id"], "data": "这是受保护的数据"}
    return {"db":db["db"], "user": current_user["user_id"], "data": "这是受保护的数据"}
from fastapi import FastAPI,File,UploadFile
@app.post("/upload",status_code=202)
async def upload(file:UploadFile=File(...)):
    content=await file.read()
    return {"file_name": file.filename, "size":len(content)}
import json
from sse_starlette.sse import EventSourceResponse
app=FastAPI()
@app.post("/chat/stream")
async def chat_steam():
    async def event_generator():
        answer="装饰器是一种包装函数的语法"
        for char in answer:
            await asyncio.sleep(0.1)
            yield {"data":json.dumps({"type":"token","content":char},ensure_ascii=False)}
        yield {"data":json.dumps({"type":"done"})}
    return EventSourceResponse(event_generator())
def find_review(review_id):
    print('你好')
from fastapi import HTTPException
@app.get("/reviews/{review_id}")
async def get_review(review_id: str):
    review=find_review(review_id)
    if review is None:
        raise HTTPException(status_code=404,detail="审查记录不存在")
    return review

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8000)