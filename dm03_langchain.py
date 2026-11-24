import asyncio
from pydantic import BaseModel,Field
from langchain.chat_models import init_chat_model
import os
from langchain_core.messages import SystemMessage, HumanMessage
api_key=os.getenv("DEEPSEEK_API_KEY")
llm=init_chat_model(
    model="deepseek-chat",
    model_provider="openai",
    api_key="sk-c5ba9086ce6545238610749dfd22718a",
    base_url="https://api.deepseek.com/v1",
    temperature=0
)
class PersonInfo(BaseModel):
    name:str=Field(description="姓名")
    age:int=Field(description="年龄")
    city:str=Field(description="城市")
structure_llm=llm.with_structured_output(PersonInfo,method="function_calling")

async def main():
    messages=[
        SystemMessage(content="你负责从文本中抽取人物信息。"),
        HumanMessage(content="我叫小明，今年 25 岁，住在上海。"),
    ]
    response=await structure_llm.ainvoke(messages)
    print(response.name)
    print(response.model_dump())
asyncio.run(main())
