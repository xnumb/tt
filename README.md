# TT - Telegram 自动化工具库

一个基于 Telethon 的 Telegram 自动化开发工具库，提供数据库操作、客户端封装、日志管理、配置管理和应用框架等功能。

## 特性

- 🗄️ **数据库操作**：基于 PyMySQL 的数据库封装，支持增删改查等常规操作
- 📱 **Telegram 客户端**：基于 Telethon 的客户端封装，简化登录和消息发送等操作
- 📝 **日志管理**：自定义日志格式，使用北京时间，并解决 Telethon 日志时间显示问题
- ⚙️ **配置管理**：支持 YAML 配置文件和命令行参数
- 🚀 **应用框架**：提供应用生命周期管理、信号处理和优雅关闭等健壮性支持

## 安装

### 从 GitHub 安装

```bash
pip install git+ssh://git@github.com/yourusername/tt.git
```

### 本地开发安装

```bash
git clone git@github.com:yourusername/tt.git
cd tt
pip install -e .
```

## 快速开始

### 1. 创建配置文件

创建 `config.yaml` 文件：

```yaml
# 代理设置
proxy:
  enabled: true
  type: http  # 支持 http, socks5, socks4
  host: 127.0.0.1
  port: 7890

# 数据库设置
database:
  host: 127.0.0.1
  port: 3306
  user: root
  name: mydb
  password: "123456"

# Telegram 设置
telegram:
  api_id: 12345678
  api_hash: "your_api_hash"

# Bot 设置
bot:
  id: 123456789
  username: "your_bot"
  token: "your_bot_token"
```

### 2. 使用数据库

```python
from tt import DB, Config

config = Config('config.yaml')
db = DB(config.get('database.name'), config.get('database.password'))

# 使用上下文管理器（推荐）
with db:
    # 查询
    rows = db.query('SELECT * FROM users WHERE id = %s', (1,))
    
    # 插入
    last_id = db.insert('INSERT INTO users (name, age) VALUES (%s, %s)', ('张三', 25))
    
    # 更新
    affected = db.update('UPDATE users SET age = %s WHERE id = %s', (26, 1))
    
    # 删除
    affected = db.delete('DELETE FROM users WHERE id = %s', (1,))
```

### 3. 使用 Telegram 客户端

```python
from tt import TGClient, Config

config = Config('config.yaml')
client = TGClient(
    session_name='my_session',
    api_id=config.get('telegram.api_id'),
    api_hash=config.get('telegram.api_hash'),
    proxy=config.proxy
)

# 发送登录验证码
code_hash = await client.send_login_code('+8612345678901')

# 登录
me = await client.send_login('+8612345678901', 'password', '12345', code_hash)

# 检查授权状态
is_auth = await client.is_auth()

# 发送消息
await client.send_message('username', 'Hello!')
```

### 4. 使用应用框架

```python
import asyncio
from tt import TelegramApp, info

# 创建应用实例
app = TelegramApp(config_path='config.yaml')

# 注册启动处理器
@app.on_startup
async def startup():
    info("应用启动")
    # 你的初始化逻辑
    pass

# 注册关闭处理器
@app.on_shutdown
async def shutdown():
    info("应用关闭")
    # 你的清理逻辑
    pass

# 运行应用
app.run()
```

### 5. 使用日志

```python
from tt import info, warn, err, debug, exception

info("这是一条信息")
warn("这是一条警告")
err("这是一条错误")
debug("这是一条调试信息")

try:
    1 / 0
except Exception as e:
    exception("发生异常")  # 会打印堆栈信息
```

### 6. 使用任务管理器

```python
from tt import TaskManager

manager = TaskManager()

# 添加任务
async def my_task():
    while True:
        await asyncio.sleep(1)
        print("任务运行中...")

manager.add_task('task1', my_task())

# 移除任务
manager.remove_task('task1')

# 取消所有任务
await manager.cancel_all()
```

## 完整示例

```python
import asyncio
from tt import TelegramApp, TGClient, DB, info

app = TelegramApp(config_path='config.yaml')

@app.on_startup
async def startup():
    info("启动 Telegram 客户端")
    
    # 创建数据库实例
    db = DB(app.config.get('database.name'), app.config.get('database.password'))
    
    # 创建 Telegram 客户端
    client = TGClient(
        session_name='my_bot',
        api_id=app.config.get('telegram.api_id'),
        api_hash=app.config.get('telegram.api_hash'),
        proxy=app.config.proxy
    )
    
    # 启动客户端
    await client.start(bot_token=app.config.get('bot.token'))
    
    # 发送消息
    await client.send_message('username', 'Bot 已启动！')
    
    # 运行直到断开连接
    app.create_task(client.run_until_disconnected())

@app.on_shutdown
async def shutdown():
    info("关闭应用")

# 运行应用
app.run()
```

## API 文档

### DB 类

数据库操作类，支持上下文管理器。

**方法：**

- `conn()`: 建立数据库连接
- `close()`: 关闭数据库连接
- `query(sql, params)`: 查询数据
- `query_one(sql, params)`: 查询单条数据
- `insert(sql, params)`: 插入数据
- `update(sql, params)`: 更新数据
- `delete(sql, params)`: 删除数据
- `execute(sql, params)`: 执行 SQL
- `execute_many(sql, params_list)`: 批量执行 SQL

### TGClient 类

Telegram 客户端封装类。

**方法：**

- `send_login_code(phone)`: 发送登录验证码
- `send_login(phone, pwd, code, code_hash)`: 执行登录
- `is_auth()`: 检查是否已授权
- `get_me()`: 获取当前用户信息
- `start(phone, password, bot_token)`: 启动客户端
- `disconnect()`: 断开连接
- `send_message(entity, message)`: 发送消息
- `log_out()`: 登出账号
- `on(event)`: 事件装饰器
- `run_until_disconnected()`: 运行直到断开连接

### Config 类

配置管理类，支持 YAML 文件和命令行参数。

**方法：**

- `get(key, default)`: 获取配置项，支持点号分隔的嵌套键（如 'database.name'）
- `set(key, value)`: 设置配置项
- `load(config_path)`: 加载配置文件
- `save(config_path)`: 保存配置文件
- `to_dict()`: 转换为字典

**属性：**

- `proxy`: 代理配置（特殊处理，返回代理元组）

**配置获取示例：**

```python
config = Config('config.yaml')

# 使用 get() 方法获取配置
db_name = config.get('database.name')
db_password = config.get('database.password')
api_id = config.get('telegram.api_id')
api_hash = config.get('telegram.api_hash')
bot_token = config.get('bot.token')

# proxy 使用属性获取（返回特殊格式的元组）
proxy = config.proxy
```

### TelegramApp 类

应用框架类，提供生命周期管理。

**方法：**

- `on_startup(handler)`: 注册启动处理器
- `on_shutdown(handler)`: 注册关闭处理器
- `create_task(coro)`: 创建并跟踪任务
- `run()`: 运行应用
- `run_async()`: 异步运行应用
- `shutdown(sig)`: 优雅关闭应用

### TaskManager 类

任务管理器，用于管理多个长期运行的任务。

**方法：**

- `add_task(name, coro)`: 添加任务
- `remove_task(name)`: 移除任务
- `get_task(name)`: 获取任务
- `cancel_all()`: 取消所有任务

## 配置文件格式

完整的 YAML 配置文件示例：

```yaml
# 代理设置
proxy:
  enabled: true          # 是否启用代理
  type: http            # 代理类型：http, socks5, socks4
  host: 127.0.0.1       # 代理主机
  port: 7890            # 代理端口

# 数据库设置
database:
  host: 127.0.0.1       # 数据库主机
  port: 3306            # 数据库端口
  user: root            # 数据库用户
  name: mydb            # 数据库名称
  password: "123456"    # 数据库密码

# Telegram 设置
telegram:
  api_id: 12345678                              # Telegram API ID
  api_hash: "your_api_hash_here"                # Telegram API Hash

# Bot 设置（可选）
bot:
  id: 123456789                                 # Bot ID
  username: "your_bot"                          # Bot 用户名
  token: "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Bot Token
```

## 命令行参数

使用 `--config` 参数指定配置文件：

```bash
python your_script.py --config /path/to/config.yaml
```

## 注意事项

1. **时区**：所有日志使用北京时间（Asia/Shanghai）
2. **代理**：如果 `proxy.enabled` 为 `false`，则不使用代理
3. **数据库连接**：建议使用 `with` 语句自动管理连接
4. **信号处理**：应用框架会自动处理 SIGINT 和 SIGTERM 信号

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### 0.1.0 (2024-xx-xx)

- 初始版本
- 支持数据库操作
- 支持 Telegram 客户端封装
- 支持日志管理
- 支持配置管理
- 支持应用框架

