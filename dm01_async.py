# import time
#
# def fetch(name, seconds):
#     print(f"开始 {name}")
#     time.sleep(seconds)          # 模拟一次耗时的网络请求
#     print(f"完成 {name}")
#
# start = time.time()
# fetch("请求A", 2)
# fetch("请求B", 2)
# fetch("请求C", 2)
# print(f"总耗时：{time.time() - start:.1f} 秒")
# import asyncio
# async def say_hello():
#     print("hello")
#     await asyncio.sleep(1)
#     print("Async")
#     return "完成"
# async def main():
#     result=await say_hello()
#     print("拿到结果：",result)
# asyncio.run(main())
# import asyncio
# import time
# async def fetch(name,seconds):
#     print(f"开始{name}")
#     await asyncio.sleep(seconds)
#     print(f'完成{name}')
#     return f"{name}的结果"
# async def main():
#     start=time.time()
#     results=await asyncio.gather(
#         fetch("请求A",2),
#         fetch("请求B",2),
#         fetch("请求C",5))
#     print("所有结果：",results)
#     print(f'总耗时：{time.time()-start:.1f}秒')
#
# asyncio.run(main())
# import asyncio
# import time
# def heavy_sync_work(n):
#     print("同步重活开始...")
#     time.sleep(2)
#     print("同步重活结束")
#     return n*n
# async def main():
#     loop=asyncio.get_running_loop()
#     result=await loop.run_in_executor(None,heavy_sync_work,10)
#     print("结果：",result)
# asyncio.run(main())
# import asyncio
# _background_tasks:set[asyncio.Task]=set()
# async def grade_exam(exam_id):
#     print(f'开始批改试卷{exam_id}...')
#     await asyncio.sleep(2)
#     print(f'试卷{exam_id}批改完成')
# async def submit():
#     task=asyncio.create_task(grade_exam("EX-001"))
#     # print(task,type(task))
#     _background_tasks.add(task)
#     task.add_done_callback(_background_tasks.discard)
#     print("接口立即返回：已收到，正在后台批改")
# async def main():
#     await submit()
#     await asyncio.sleep(3)
#     print("当前后台任务数：",len(_background_tasks))
# asyncio.run(main())
# import asyncio
# from contextlib import asynccontextmanager
# @asynccontextmanager
# async def lifespan():
#     print("启动/加载 模型")
#     yield
#     print("关闭/释放 资源")
# async def main():
#     async with lifespan():
#         print("应用运行中，处理请求...")
# asyncio.run(main())
import asyncio


async def get_value():
    return 42

# 错误：result 是一个 <coroutine object>，不是 42
# result = get_value()
# print("结果：",result)

# 正确：必须 await
async def main():
    result = await get_value()
    print("结果：",result)
# 42
asyncio.run(main())