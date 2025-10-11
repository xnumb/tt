# 更新日志

本文档记录 TT 库的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

## [0.1.0] - 2024-10-11

### 新增
- 数据库操作类 `DB`
  - 支持增删改查等基本操作
  - 支持上下文管理器（`with` 语句）
  - 自动连接管理，无需手动 `conn()` 和 `close()`
  - 新增 `query_one()` 方法用于查询单条记录
  - 新增 `execute()` 和 `execute_many()` 方法

- Telegram 客户端类 `TGClient`
  - 封装 Telethon 客户端
  - 简化登录流程
  - 支持发送验证码、登录、检查授权状态
  - 支持发送消息、登出等常用操作
  - 支持代理配置

- 日志管理类 `Logger`
  - 自定义时间格式，固定使用北京时间
  - 封装常用日志方法（`err`, `info`, `warn`, `debug`, `exception`）
  - 自动配置 Telethon 库的日志，使其显示时间

- 配置管理类 `Config`
  - 支持 YAML 配置文件
  - 支持命令行参数 `--config` 指定配置文件
  - 支持点号分隔的嵌套键访问（如 `config.get('database.name')`）
  - 提供便捷属性访问配置项

- 应用框架类 `TelegramApp`
  - 提供应用生命周期管理
  - 支持启动和关闭处理器注册
  - 自动处理 SIGINT 和 SIGTERM 信号
  - 优雅关闭机制，自动取消所有任务
  - 全局异常处理

- 任务管理器 `TaskManager`
  - 管理多个长期运行的任务
  - 支持添加、移除、获取任务
  - 支持取消所有任务

### 文档
- README.md - 完整的使用文档和 API 文档
- GETTING_STARTED.md - 快速开始指南
- MIGRATION_GUIDE.md - 从旧项目迁移指南
- example.py - 完整的使用示例
- config.example.yaml - 配置文件示例

### 工具
- setup.py - 传统 setuptools 配置
- pyproject.toml - 现代 Python 项目配置
- requirements.txt - 依赖列表
- MANIFEST.in - 打包文件清单
- .gitignore - Git 忽略配置

## [计划中]

### v0.2.0
- [ ] 添加异步数据库支持
- [ ] 添加数据库连接池
- [ ] 添加更多 Telegram 客户端方法封装
- [ ] 支持更多配置文件格式（JSON, TOML）
- [ ] 添加单元测试
- [ ] 添加类型提示（Type Hints）

### v0.3.0
- [ ] 添加消息队列支持
- [ ] 添加定时任务支持
- [ ] 添加插件系统
- [ ] 性能优化

## 贡献指南

发现问题或有建议？欢迎：
- 提交 Issue: https://github.com/yourusername/tt/issues
- 提交 Pull Request: https://github.com/yourusername/tt/pulls

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

