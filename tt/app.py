import asyncio
import signal
from typing import Callable, List
from .log import Logger
from .config import Config


class TelegramApp:
    """Telegram 应用框架类，提供应用生命周期管理和健壮性支持"""
    
    def __init__(self, config_path=None, logger=None):
        """
        初始化应用
        
        Args:
            config_path: 配置文件路径
            logger: 日志记录器，如果为 None 则创建默认记录器
        """
        self.config = Config(config_path) if config_path else Config()
        self.logger = logger or Logger()
        self.loop = None
        self._startup_handlers: List[Callable] = []
        self._shutdown_handlers: List[Callable] = []
        self._running_tasks: List[asyncio.Task] = []
    
    def on_startup(self, handler: Callable):
        """
        注册启动处理器
        
        Args:
            handler: 异步处理函数
            
        Returns:
            原处理函数（用作装饰器）
        """
        self._startup_handlers.append(handler)
        return handler
    
    def on_shutdown(self, handler: Callable):
        """
        注册关闭处理器
        
        Args:
            handler: 异步处理函数
            
        Returns:
            原处理函数（用作装饰器）
        """
        self._shutdown_handlers.append(handler)
        return handler
    
    def create_task(self, coro):
        """
        创建并跟踪任务
        
        Args:
            coro: 协程对象
            
        Returns:
            创建的任务
        """
        task = asyncio.create_task(coro)
        self._running_tasks.append(task)
        return task
    
    async def _run_startup_handlers(self):
        """运行所有启动处理器"""
        for handler in self._startup_handlers:
            try:
                await handler()
            except Exception as e:
                self.logger.exception(f"启动处理器执行失败: {e}")
    
    async def _run_shutdown_handlers(self):
        """运行所有关闭处理器"""
        for handler in self._shutdown_handlers:
            try:
                await handler()
            except Exception as e:
                self.logger.exception(f"关闭处理器执行失败: {e}")
    
    async def shutdown(self, sig=None):
        """
        优雅关闭应用
        
        Args:
            sig: 接收到的信号
        """
        if sig:
            self.logger.info(f"接收到退出信号 {sig.name}...")
        
        # 运行关闭处理器
        await self._run_shutdown_handlers()
        
        # 取消所有正在运行的任务
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        
        for task in tasks:
            task.cancel()
        
        self.logger.info("正在取消任务...")
        await asyncio.gather(*tasks, return_exceptions=True)
        self.logger.info("任务已取消")
        
        if self.loop:
            self.loop.stop()
    
    def _handle_exception(self, loop, context):
        """
        处理未捕获的异常
        
        Args:
            loop: 事件循环
            context: 异常上下文
        """
        msg = context.get("exception", context["message"])
        self.logger.error(f"捕获到异常: {msg}")
        self.logger.info("正在关闭...")
        asyncio.create_task(self.shutdown())
    
    def _setup_signals(self):
        """设置信号处理器"""
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.loop.add_signal_handler(
                sig, lambda s=sig: asyncio.create_task(self.shutdown(s))
            )
    
    def run(self):
        """
        运行应用
        """
        self.loop = asyncio.get_event_loop()
        self.loop.set_exception_handler(self._handle_exception)
        
        # 设置信号处理
        self._setup_signals()
        
        try:
            self.logger.info("应用启动中...")
            self.loop.create_task(self._run_startup_handlers())
            self.loop.run_forever()
        finally:
            self.logger.info("关闭事件循环...")
            self.loop.close()
            self.logger.info("应用已结束")
    
    async def run_async(self):
        """
        异步运行应用（用于在已有事件循环中运行）
        """
        self.logger.info("应用启动中...")
        await self._run_startup_handlers()
        
        # 等待直到收到停止信号
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            self.logger.info("应用被取消")
        finally:
            await self.shutdown()


class TaskManager:
    """任务管理器，用于管理多个长期运行的任务"""
    
    def __init__(self, logger=None):
        """
        初始化任务管理器
        
        Args:
            logger: 日志记录器
        """
        self.logger = logger or Logger()
        self._tasks = {}
    
    def add_task(self, name, coro):
        """
        添加任务
        
        Args:
            name: 任务名称
            coro: 协程对象
            
        Returns:
            创建的任务
        """
        if name in self._tasks:
            self.logger.warning(f"任务 {name} 已存在，将被替换")
        
        task = asyncio.create_task(coro)
        self._tasks[name] = task
        self.logger.info(f"任务 {name} 已添加")
        return task
    
    def remove_task(self, name):
        """
        移除任务
        
        Args:
            name: 任务名称
        """
        if name in self._tasks:
            task = self._tasks[name]
            if not task.done():
                task.cancel()
            del self._tasks[name]
            self.logger.info(f"任务 {name} 已移除")
    
    def get_task(self, name):
        """
        获取任务
        
        Args:
            name: 任务名称
            
        Returns:
            任务对象，不存在返回 None
        """
        return self._tasks.get(name)
    
    async def cancel_all(self):
        """取消所有任务"""
        self.logger.info("正在取消所有任务...")
        for name, task in self._tasks.items():
            if not task.done():
                task.cancel()
                self.logger.info(f"任务 {name} 已取消")
        
        await asyncio.gather(*self._tasks.values(), return_exceptions=True)
        self._tasks.clear()
        self.logger.info("所有任务已取消")
    
    def __len__(self):
        """返回任务数量"""
        return len(self._tasks)
    
    def __contains__(self, name):
        """检查任务是否存在"""
        return name in self._tasks

