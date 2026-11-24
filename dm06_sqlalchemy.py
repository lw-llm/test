import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

engine=create_async_engine("sqlite+aiosqlite:///demo.db")
AsyncSessionLocal=async_sessionmaker(engine,expire_on_commit=False)

async def main():
    async with AsyncSessionLocal() as session:
        # 1. 建表
        await session.execute(text("drop table if exists users"))
        await session.execute(text("""
        create table users(
        id      integer primary key autoincrement,
        username    text,
        role        text,
        is_active   boolean
        )
        """))
        # 2. insert
        await session.execute(
            text("insert into users(username,role,is_active)values(:u,:r,:a)"),
            [{"u":"student01","r":"student","a":True},{"u":"student02","r":"student","a":True}]
        )


        await session.execute(
            text("INSERT INTO users (username, role, is_active) VALUES (:u, :r, :a)"),
            {"u": "teacher01", "r": "teacher", "a": True},
        )
        # 3. select
        result = await session.execute(
            text("SELECT id, username, role, is_active FROM users WHERE role = :r"),
            {"r": "student"},
        )
        row = result.fetchone()
        row = result.fetchone()
        print(f'row: {row}')
        print("查到学生：", row.id, row.username, row.role)
        print("查到学生：", row[0], row[1], row[2])
        print("*" * 80)
        # 4. update
        await session.execute(
            text("UPDATE users SET is_active = :a WHERE username = :u"),
            {"a": False, "u": "student01"},
        )
        # result = await session.execute(
        #     text("SELECT id, username, role, is_active FROM users WHERE role = :r"),
        #     {"r": "student"},
        # )
        # row = result.fetchone()
        # print(f'row: {row}')
        # print("查到学生1：", row.id, row.username, row.role)
        # print("查到学生1：", row[0], row[1], row[2])

        # 5. 删（DELETE）
        await session.execute(
            text("delete from users where username=:u"),
            {"u":"teacher01"},
        )
        # 6. 提交事务
        await session.commit()
        # # 验证：看看现在表里剩什么
        all_rows = (await session.execute(text("SELECT username, is_active FROM users")))
        print(f'all_rows={type(all_rows)}')
        print(all_rows.fetchall())
        print("*"*80)
        all_rows = (await session.execute(text("SELECT username, is_active FROM users"))).mappings().all()
        print(f'all_rows={type(all_rows)}')
        print(f'all_rows={all_rows}')
        print("最终数据：", [dict(r) for r in all_rows])
asyncio.run(main())

