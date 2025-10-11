# 迁移指南

本指南说明如何将现有项目迁移到使用 TT 库。

## 迁移步骤

### 1. 安装 TT 库

```bash
pip install git+ssh://git@github.com/yourusername/tt.git
```

### 2. 创建配置文件

将原来的 `conf.py` 转换为 `config.yaml`：

**原 conf.py:**
```python
import socks

PROXY = (socks.HTTP, "127.0.0.1", 7890)
DB_PWD = "123456aA"
DB_NAME = "pc28sender"
API_ID = 11649161
API_HASH = "7bb42992b8a3f05dec91be50390398fc"
BOT_ID = 6524718932
BOT_USERNAME = "vshentest_bot"
BOT_TOKEN = "6524718932:AAG1E6zRmA43pTcXcajBJcQhRUlwK48vF14"
```

**新 config.yaml:**
```yaml
proxy:
  enabled: true
  type: http
  host: 127.0.0.1
  port: 7890

database:
  name: pc28sender
  password: "123456aA"

telegram:
  api_id: 11649161
  api_hash: "7bb42992b8a3f05dec91be50390398fc"

bot:
  id: 6524718932
  username: "vshentest_bot"
  token: "6524718932:AAG1E6zRmA43pTcXcajBJcQhRUlwK48vF14"
```

### 3. 更新代码

#### 3.1 导入语句

**之前:**
```python
from tt import acc, log, db
```

**之后:**
```python
from tt import TGClient, info, err, warn, DB, Config
```

#### 3.2 数据库使用

**之前:**
```python
from tt import db
import conf

d = db.DB(conf.DB_NAME, conf.DB_PWD)

def get_senders():
    d.conn()
    rows = d.query('select * from `sender` where login_state = %s', (2,))
    d.close()
    return rows
```

**之后:**
```python
from tt import DB, Config

config = Config('config.yaml')
db = DB(config.get('database.name'), config.get('database.password'))

def get_senders():
    with db:
        rows = db.query('select * from `sender` where login_state = %s', (2,))
        return rows
```

#### 3.3 日志使用

**之前:**
```python
from tt import log

log.info("消息")
log.err("错误")
log.warn("警告")
```

**之后:**
```python
from tt import info, err, warn

info("消息")
err("错误")
warn("警告")
```

#### 3.4 Telegram 客户端

**之前:**
```python
from tt import acc
import conf

class Sender(acc.Acc):
    def __init__(self, id):
        self.id = id
        super().__init__("sessions/" + str(id), conf.API_ID, conf.API_HASH, conf.PROXY)
```

**之后:**
```python
from tt import TGClient, Config

config = Config('config.yaml')

class Sender(TGClient):
    def __init__(self, id):
        self.id = id
        super().__init__(
            session_name="sessions/" + str(id),
            api_id=config.get('telegram.api_id'),
            api_hash=config.get('telegram.api_hash'),
            proxy=config.proxy
        )
```

#### 3.5 主程序

**之前 (main_pc28sender.py):**
```python
import asyncio
import signal
import account
import mod
from tt import log

async def main():
    asyncio.create_task(account.start_bot())
    rs = mod.get_senders()
    for r in rs:
        try:
            log.info("Start Sender:" + str(r["id"]))
            sender_instance = account.Sender(r["id"])
            asyncio.create_task(sender_instance.start())
        except Exception as e:
            log.warn(e)

# ... 信号处理和事件循环代码
loop = asyncio.get_event_loop()
# ...
```

**之后:**
```python
from tt import TelegramApp, info, warn
import account
import mod

app = TelegramApp(config_path='config.yaml')
senders = []

@app.on_startup
async def startup():
    info("应用启动")
    
    # 启动 bot
    app.create_task(account.start_bot())
    
    # 启动 senders
    rs = mod.get_senders()
    for r in rs:
        try:
            info("Start Sender:" + str(r["id"]))
            sender_instance = account.Sender(r["id"])
            senders.append(sender_instance)
            app.create_task(sender_instance.start())
        except Exception as e:
            warn(str(e))

@app.on_shutdown
async def shutdown():
    info("应用关闭")

if __name__ == '__main__':
    app.run()
```

### 4. 更新 requirements.txt

**之前:**
```text
telethon
PyMySQL
pytz
PySocks
```

**之后:**
```text
# TT 库（已包含上述所有依赖）
git+ssh://git@github.com/yourusername/tt.git
```

### 5. 清理旧代码

迁移完成后，可以删除或备份以下文件：
- `tt/` 目录（旧的本地库）
- `conf.py`（已替换为 config.yaml）

## 完整示例对比

### 迁移前

**文件结构:**
```
project/
├── conf.py
├── main_pc28sender.py
├── account.py
├── mod.py
├── tt/
│   ├── acc.py
│   ├── db.py
│   └── log.py
└── sessions/
```

**main_pc28sender.py:**
```python
import asyncio
import signal
import account
import mod
from tt import log

senders = []

async def main():
    asyncio.create_task(account.start_bot())
    rs = mod.get_senders()
    for r in rs:
        try:
            log.info("Start Sender:" + str(r["id"]))
            sender_instance = account.Sender(r["id"])
            senders.append(sender_instance)
            asyncio.create_task(sender_instance.start())
        except Exception as e:
            log.warn(e)

async def shutdown(loop, sig=None):
    if sig:
        log.info(f"Received exit signal {sig.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    log.info("Cancelling tasks...")
    await asyncio.gather(*tasks, return_exceptions=True)
    log.info("Tasks cancelled.")
    loop.stop()

def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    log.err(f"Caught exception: {msg}")
    log.info("Shutting down...")
    asyncio.create_task(shutdown(loop))

loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)

for sig in (signal.SIGINT, signal.SIGTERM):
    loop.add_signal_handler(
        sig, lambda s=sig: asyncio.create_task(shutdown(loop, s))
    )

try:
    log.info("Application starting...")
    loop.create_task(main())
    loop.run_forever()
finally:
    log.info("Closing loop...")
    loop.close()
    log.info("Application finished.")
```

### 迁移后

**文件结构:**
```
project/
├── config.yaml        # 新增
├── main.py           # 简化后的主程序
├── account.py        # 修改导入
├── mod.py            # 修改导入
└── sessions/
```

**main.py:**
```python
from tt import TelegramApp, info, warn
import account
import mod

app = TelegramApp(config_path='config.yaml')
senders = []

@app.on_startup
async def startup():
    info("应用启动")
    app.create_task(account.start_bot())
    
    rs = mod.get_senders()
    for r in rs:
        try:
            info("Start Sender:" + str(r["id"]))
            sender_instance = account.Sender(r["id"])
            senders.append(sender_instance)
            app.create_task(sender_instance.start())
        except Exception as e:
            warn(str(e))

@app.on_shutdown
async def shutdown():
    info("应用关闭")

if __name__ == '__main__':
    app.run()
```

**mod.py:**
```python
from tt import DB, Config

config = Config('config.yaml')
db = DB(config.get('database.name'), config.get('database.password'))

def get_senders():
    with db:
        return db.query('select * from `sender` where login_state = %s', (2,))

def get_sender(id):
    with db:
        return db.query_one('select * from `sender` where id = %s', (id,))

def update_sender(id, tid, username, name):
    with db:
        db.update(
            'update `sender` set tid = %s, username = %s, name = %s, login_state = %s where id = %s',
            (tid, username, name, 2, id)
        )

# ... 其他函数类似
```

**account.py:**
```python
from telethon import TelegramClient, events
import asyncio
from tt import TGClient, info, Config
import mod

config = Config('config.yaml')

LISTENER_CODE_MSG = "请输入您收到的验证码"
LISTENER_LOGIN_MSG = "正在登录中, 如果您提供的内容正确, 账号将在1分钟之内完成登录, 请稍后查看"

bot = TelegramClient(
    "sessions/bot",
    config.get('telegram.api_id'),
    config.get('telegram.api_hash'),
    proxy=config.proxy
).start(bot_token=config.get('bot.token'))

async def start_bot():
    # ... 保持不变
    pass

class Sender(TGClient):
    def __init__(self, id):
        self.id = id
        self.tid = 0
        super().__init__(
            session_name="sessions/" + str(id),
            api_id=config.get('telegram.api_id'),
            api_hash=config.get('telegram.api_hash'),
            proxy=config.proxy
        )
    
    # ... 其他方法保持不变
```

## 优势对比

### 迁移前
- ❌ 每个项目都需要复制 `tt/` 目录
- ❌ 配置是 Python 代码，不易修改
- ❌ 需要手写信号处理和优雅关闭代码
- ❌ 数据库需要手动 conn() 和 close()

### 迁移后
- ✅ 通过 pip 安装，易于更新
- ✅ YAML 配置，易于修改
- ✅ 应用框架自动处理信号和关闭
- ✅ 数据库使用 with 语句自动管理连接
- ✅ Telethon 日志自动带时间
- ✅ 代码更简洁，关注业务逻辑

## 注意事项

1. **配置文件位置**: 确保 `config.yaml` 在正确的位置，或通过 `--config` 参数指定
2. **会话文件**: Telegram 会话文件保持不变，无需重新登录
3. **数据库**: 数据库结构和数据保持不变
4. **兼容性**: TT 库保持了原有功能的兼容性，只是接口更简洁

## 逐步迁移策略

如果项目较大，可以逐步迁移：

1. **第一步**: 只迁移日志
   ```python
   # 将 from tt import log 改为
   from tt import info, err, warn
   ```

2. **第二步**: 迁移数据库
   ```python
   # 使用 with 语句管理连接
   with db:
       db.query(...)
   ```

3. **第三步**: 迁移配置
   ```python
   # 创建 config.yaml，使用 Config 类
   from tt import Config
   config = Config('config.yaml')
   ```

4. **第四步**: 迁移主程序
   ```python
   # 使用 TelegramApp 框架
   app = TelegramApp()
   ```

每一步都可以单独测试，确保功能正常后再进行下一步。

