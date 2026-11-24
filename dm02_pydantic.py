# from pydantic import BaseModel
# class Student(BaseModel):
#     name:str
#     age:int
# s=Student(name="小名",age="视为")
# print(s)
# print(s.name)
# print(s.age)
# from pydantic import BaseModel,Field
# class UserProfile(BaseModel):
#     name:str=Field(description="用户姓名")
#     phone:str=Field(default="",description="手机号")
#     age:int=Field(default=18,description="年龄")
#     tags:list=Field(default_factory=list ,description="标签")
# userprofile=UserProfile(name="小名")
# print(userprofile)
# print(userprofile.name)
# print(userprofile.phone)
# print(userprofile.age)
# from pydantic import BaseModel, Field
#
# class EducationItem(BaseModel):
#     school: str = Field(description="学校名称")
#     major:  str = Field(description="专业名称")
#
# class Resume(BaseModel):
#     name:      str                = Field(description="姓名")
#     education: list[EducationItem] = Field(default_factory=list)  # 教育经历列表
#
# # 创建时，嵌套部分可以直接用字典，Pydantic 会自动转成对应的子模型
# resume = Resume(
#     name="小明",
#     education=[
#         {"school": "清华大学", "major": "计算机"},
#         {"school": "北京大学", "major": "软件工程"},
#     ],
# )
#
# print(resume.name)                    # 小明
# print(resume.education[0].school)     # 清华大学  ← 注意：已经是 EducationItem 对象了
# print(type(resume.education[0]))      # <class '__main__.EducationItem'>
# from pydantic import BaseModel, Field
#
# class Student(BaseModel):
#     name: str = Field(description="姓名")
#     age:  int = Field(default=18, description="年龄")
#
# s = Student(name="小明", age=20)
# print(s)
# d=s.model_dump()
# print(d)
# print(type(d))

# from enum import Enum
#
# class InterviewStage(str, Enum):       # 继承 str，取值就是字符串
#     WARMUP    = "warmup"
#     TECH_BASE = "tech_base"
#     PROJECT   = "project"
#     CLOSING   = "closing"
#     FINISHED  = "finished"
#
# print(InterviewStage.WARMUP)           # InterviewStage.WARMUP
# print(InterviewStage.WARMUP.value)     # warmup
# from pydantic_settings import BaseSettings
#
# class Settings(BaseSettings):
#     db_host: str = "localhost"
#     db_port: int = 5433              # 会自动把环境变量里的字符串转成 int
#
# settings = Settings()
# print(settings.db_host, settings.db_port)
