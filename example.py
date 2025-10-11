#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TT 库使用示例
"""

import asyncio
from tt import TelegramApp, TGClient, DB, info, err


# 方式 1: 使用应用框架（推荐）
def example_with_app():
    """使用应用框架的示例"""
    
    # 创建应用实例，会自动从命令行参数读取 --config
    app = TelegramApp()
    
    # 注册启动处理器
    @app.on_startup
    async def startup():
        info("应用启动中...")
        
        # 创建数据库实例
        db = DB(app.config.get('database.name'), app.config.get('database.password'))
        
        # 使用数据库
        with db:
            rows = db.query('SELECT * FROM users LIMIT 10')
            info(f"查询到 {len(rows)} 条记录")
        
        # 创建 Telegram 客户端
        client = TGClient(
            session_name='sessions/my_bot',
            api_id=app.config.get('telegram.api_id'),
            api_hash=app.config.get('telegram.api_hash'),
            proxy=app.config.proxy
        )
        
        # 启动客户端（Bot 模式）
        await client.start(bot_token=app.config.get('bot.token'))
        info("Telegram 客户端已启动")
        
        # 发送消息
        try:
            await client.send_message(app.config.get('bot.username'), 'Bot 已启动！')
        except Exception as e:
            err(f"发送消息失败: {e}")
        
        # 创建任务让客户端持续运行
        app.create_task(client.run_until_disconnected())
    
    # 注册关闭处理器
    @app.on_shutdown
    async def shutdown():
        info("应用关闭中...")
        # 在这里做清理工作
    
    # 运行应用
    app.run()


# 方式 2: 直接使用各个组件
async def example_direct():
    """直接使用各个组件的示例"""
    
    from tt import Config
    
    # 加载配置
    config = Config('config.yaml')
    
    # 使用数据库
    db = DB(config.get('database.name'), config.get('database.password'))
    
    with db:
        # 查询
        rows = db.query('SELECT * FROM users WHERE id = %s', (1,))
        print(rows)
        
        # 插入
        last_id = db.insert(
            'INSERT INTO users (name, age) VALUES (%s, %s)',
            ('张三', 25)
        )
        print(f"插入成功，ID: {last_id}")
        
        # 更新
        affected = db.update(
            'UPDATE users SET age = %s WHERE id = %s',
            (26, last_id)
        )
        print(f"更新了 {affected} 行")
    
    # 使用 Telegram 客户端
    client = TGClient(
        session_name='my_session',
        api_id=config.get('telegram.api_id'),
        api_hash=config.get('telegram.api_hash'),
        proxy=config.proxy
    )
    
    # 检查是否已登录
    if await client.is_auth():
        info("已登录")
        me = await client.get_me()
        info(f"当前用户: {me.first_name}")
    else:
        info("未登录，需要登录")
        # 发送验证码
        phone = '+8612345678901'
        code_hash = await client.send_login_code(phone)
        
        if code_hash:
            # 这里应该从用户获取验证码
            code = input("请输入验证码: ")
            password = input("如果有两步验证，请输入密码（没有按回车）: ")
            
            # 登录
            me = await client.send_login(phone, password, code, code_hash)
            if me:
                info(f"登录成功: {me.first_name}")
            else:
                err("登录失败")
    
    # 发送消息
    await client.send_message('username', 'Hello from TT!')
    
    # 断开连接
    await client.disconnect()


# 方式 3: 使用任务管理器
async def example_with_task_manager():
    """使用任务管理器的示例"""
    
    from tt import TaskManager
    
    manager = TaskManager()
    
    # 定义一些任务
    async def task1():
        while True:
            info("任务 1 运行中...")
            await asyncio.sleep(5)
    
    async def task2():
        while True:
            info("任务 2 运行中...")
            await asyncio.sleep(10)
    
    # 添加任务
    manager.add_task('task1', task1())
    manager.add_task('task2', task2())
    
    # 等待一段时间
    await asyncio.sleep(30)
    
    # 取消所有任务
    await manager.cancel_all()


if __name__ == '__main__':
    # 使用方式 1（推荐）
    example_with_app()
    
    # 或者使用方式 2
    # asyncio.run(example_direct())
    
    # 或者使用方式 3
    # asyncio.run(example_with_task_manager())

