class Cake:
    def __init__(self, name):
        self.name = name
    def __del__(self):                       # 对象被回收时，Python 会调用这个方法
        print(f"🗑️ 蛋糕「{self.name}」被回收了")

cake = Cake("草莓")          # 创建蛋糕，贴上标签 cake
print("蛋糕还在")
cake = None                  # 撕掉唯一的标签 → 没人引用了 → 触发回收
print("撕掉标签之后")
print("hellow, world!")
