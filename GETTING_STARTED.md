# 快速开始指南

本指南将帮助你快速上手 TT 库。

## 发布到 GitHub

### 1. 初始化 Git 仓库

```bash
cd ttlib
git init
git add .
git commit -m "Initial commit: TT library v0.1.0"
```

### 2. 创建 GitHub 仓库

1. 登录 GitHub
2. 创建新仓库，例如命名为 `tt`
3. 不要初始化 README、.gitignore 或 LICENSE（我们已经有了）

### 3. 推送到 GitHub

```bash
git remote add origin git@github.com:yourusername/tt.git
git branch -M main
git push -u origin main
```

## 在新项目中使用

### 方法 1: 从 GitHub 直接安装（推荐）

```bash
# SSH 方式
pip install git+ssh://git@github.com/yourusername/tt.git

# HTTPS 方式
pip install git+https://github.com/yourusername/tt.git

# 安装特定版本
pip install git+ssh://git@github.com/yourusername/tt.git@v0.1.0
```

### 方法 2: 从本地安装（开发模式）

```bash
# 克隆仓库
git clone git@github.com:yourusername/tt.git
cd tt

# 开发模式安装（修改会立即生效）
pip install -e .

# 或者正常安装
pip install .
```

### 方法 3: 添加到 requirements.txt

在你的项目 `requirements.txt` 中添加：

```text
# 从 GitHub 安装
git+ssh://git@github.com/yourusername/tt.git

# 或指定版本
git+ssh://git@github.com/yourusername/tt.git@v0.1.0
```

然后运行：

```bash
pip install -r requirements.txt
```

## 基本使用

### 1. 创建配置文件

在你的项目根目录创建 `config.yaml`：

```yaml
proxy:
  enabled: true
  type: http
  host: 127.0.0.1
  port: 7890

database:
  name: mydb
  password: "123456"

telegram:
  api_id: 12345678
  api_hash: "your_api_hash"

bot:
  id: 123456789
  username: "your_bot"
  token: "your_bot_token"
```

### 2. 编写你的程序

创建 `main.py`：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tt import TelegramApp, info

app = TelegramApp()

@app.on_startup
async def startup():
    info("程序启动")
    # 你的初始化逻辑

@app.on_shutdown
async def shutdown():
    info("程序关闭")
    # 你的清理逻辑

if __name__ == '__main__':
    app.run()
```

### 3. 运行程序

```bash
# 使用默认配置文件（会从命令行参数读取）
python main.py --config config.yaml

# 或者在代码中指定
# app = TelegramApp(config_path='config.yaml')
```

## 更新库版本

当库有新版本时：

```bash
# 更新到最新版本
pip install --upgrade git+ssh://git@github.com/yourusername/tt.git

# 或者先卸载再安装
pip uninstall tt
pip install git+ssh://git@github.com/yourusername/tt.git
```

## 开发建议

### 1. 使用虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装库
pip install git+ssh://git@github.com/yourusername/tt.git
```

### 2. 项目结构建议

```
your_project/
├── config.yaml         # 配置文件
├── main.py            # 主程序
├── requirements.txt   # 依赖列表
├── sessions/          # Telegram 会话文件夹
│   └── .gitkeep
└── venv/              # 虚拟环境（添加到 .gitignore）
```

### 3. .gitignore 建议

```
# Python
__pycache__/
*.py[cod]
venv/

# 配置和会话
config.yaml
sessions/*.session
sessions/*.session-journal

# 日志
*.log
```

## 常见问题

### Q: 如何获取 Telegram API ID 和 API Hash？

A: 访问 https://my.telegram.org，登录后在 "API development tools" 创建应用。

### Q: 如何创建 Telegram Bot？

A: 在 Telegram 中找到 @BotFather，发送 `/newbot` 命令创建。

### Q: 代理设置不生效？

A: 确保 `proxy.enabled` 设置为 `true`，并检查代理服务器是否正常运行。

### Q: 数据库连接失败？

A: 检查数据库服务是否启动，用户名密码是否正确，数据库是否存在。

### Q: 如何调试？

A: 使用 `debug()` 函数打印调试信息，或者设置日志级别：

```python
from tt import Logger
import logging

logger = Logger(level=logging.DEBUG)
```

## 更多示例

查看 `example.py` 文件获取更多使用示例。

## 获取帮助

- 查看 [README.md](README.md) 获取详细文档
- 提交 Issue: https://github.com/yourusername/tt/issues
- 查看示例代码: `example.py`

## 版本发布

当你要发布新版本时：

```bash
# 更新版本号（在 setup.py 和 pyproject.toml 中）
# 提交更改
git add .
git commit -m "Release v0.2.0"

# 打标签
git tag -a v0.2.0 -m "Version 0.2.0"

# 推送
git push origin main --tags
```

