import asyncio
import json
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

app = FastAPI(title="EduAgent Demo")

# ---------- 2.5.2 健康检查 ----------
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# ---------- 2.5.3 登录（请求体 + 响应模型） ----------
class LoginRequest(BaseModel):
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

@app.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    if req.username == "student01" and req.password == "Student@123456":
        return TokenResponse(access_token="fake-token-abc", role="student")
    # 为了演示，错误的也返回 guest
    return TokenResponse(access_token="", token_type="bearer", role="guest")

# ---------- 2.5.4 路径参数与查询参数 ----------
@app.get("/reviews/{review_id}")
async def get_review(review_id: str):
    return {"review_id": review_id, "status": "completed"}

@app.get("/reviews")
async def list_reviews(page: int = 1, size: int = 10):
    return {"page": page, "size": size}

# ---------- 2.5.5 依赖注入（模拟数据库 + 模拟鉴权） ----------
# 为了让你在 Postman 里能直接测通，这里不强制要求传 Token，而是直接返回模拟用户。
# 但为了演示真实鉴权流程，我加一个可选的 Bearer Token 校验（非必须，以便测试）。
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
    return {"user": current_user["user_id"], "data": "这是受保护的数据"}

# 如果你想知道带上真实 Authorization 头怎么测，这里额外写一个真实的 Bearer 校验示例（选看）
# 为了简化，依然不验签，只从Header取token展示
bearer_scheme = HTTPBearer(auto_error=False)  # auto_error=False 允许不带Token

@app.get("/secure-endpoint")
async def secure_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="请提供 Token")
    token = credentials.credentials
    return {"message": f"收到您的 Token: {token[:10]}..."}

# ---------- 2.5.6 文件上传 ----------
@app.post("/upload", status_code=202)
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}

# ---------- 2.5.7 SSE 流式响应 ----------
@app.post("/chat/stream")
async def chat_stream():
    async def event_generator():
        answer = "装饰器是一种包装函数的语法。"
        for char in answer:
            await asyncio.sleep(0.1)  # 模拟逐字生成
            yield {"data": json.dumps({"type": "token", "content": char})}
        yield {"data": json.dumps({"type": "done"})}
    return EventSourceResponse(event_generator())

# ---------- 2.5.8 错误处理 ----------
def find_review(review_id: str):
    return None  # 模拟查不到

@app.get("/reviews-with-error/{review_id}")
async def get_review_with_error(review_id: str):
    review = find_review(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="审查记录不存在")
    return review
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8000)