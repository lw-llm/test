# from typing import TypedDict
# class HelperState(TypedDict):
#     question:str
#     category:str
#     answer:str
# def classify_node(state:HelperState)->dict:
#     q=state["question"]
#     if "代码" in q or "报错" in q or "bug" in q:
#         return {"category": "code"}
#     elif "什么是" in q or "概念" in q or "原理" in q:
#         return {"category": "concept"}
#     else:
#         return {"category": "chat"}
# def answer_concept_node(state:HelperState)->dict:
#     return {"answer": f"【概念解答】关于「{state['question']}」，它的核心思想是……"}
# def answer_code_node(state:HelperState)->dict:
#     return {"answer": f"【代码助手】针对「{state['question']}」，我们一步步排查……"}
# def answer_chat_node(state:HelperState)->dict:
#     return {"answer": "【闲聊】哈哈，没问题，我们继续聊～"}
# from langgraph.graph import StateGraph,START,END
# todo 1.直线型graph
# # 1. 用state类型创建图构建器
# builder=StateGraph(HelperState)
# # 2. 注册节点（名字，函数）
# builder.add_node("classify",classify_node)
# builder.add_node("answer",answer_concept_node)
# # 3. 连边
# builder.add_edge(START,"classify")
# builder.add_edge("classify","answer")
# builder.add_edge("answer",END)
# # 4. 编译可执行图
# graph= builder.compile()
# result=graph.invoke({"question":"什么是python"})
# print(result)
# # todo 2.带分支的graph
# def route_by_category(state:HelperState)-> str:
#     """
#     路由函数：返回一个字符串路标，决定去那个节点
#     """
#     return state["category"]
# builder=StateGraph(HelperState)
#
# builder.add_node("classify",classify_node)
# builder.add_node("concept",answer_concept_node)
# builder.add_node("code",answer_code_node)
# builder.add_node("chat",answer_chat_node)
#
# builder.add_edge(START,"classify")
# # 添加条件边
# builder.add_conditional_edges(
#     "classify",
#     route_by_category,
#     {"concept":"concept","code":"code","chat":"chat"}
# )
# builder.add_edge("concept",END)
#
# builder.add_edge("code",END)
# builder.add_edge("chat",END)
# graph= builder.compile()
#
# for q in ["什么是python","如何debug代码","python why"]:
#     result=graph.invoke({"question":q})
#     print(result)

# todo 3. 加记忆
from typing import Annotated,TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage,AIMessage
class ChatState(TypedDict):
    messages:Annotated[list,add_messages]
def reply_node(state:ChatState) -> dict:
    last_user_msg=state["messages"][-1].content
    history_count=len(state["messages"])
    relpy=f'我收到了{last_user_msg},(当前历史消息共{history_count}条)'
    return {"messages":[AIMessage(content=relpy)]}
builder=StateGraph(ChatState)
builder.add_node("reply",reply_node)
builder.add_edge(START,"reply")
builder.add_edge("reply",END)
graph= builder.compile(checkpointer=MemorySaver())
config={"configurable":{"thread_id":"user-1"}}
graph.invoke({"messages":[HumanMessage(content="你好")]},config)
result=graph.invoke({"messages":[HumanMessage(content="还记得我刚说的什么吗")]},config)
for m in result["messages"]:
    print(type(m).__name__, m.content)

