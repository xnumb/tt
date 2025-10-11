from datetime import datetime
import pytz
import logging


def get_now():
    """获取北京时间"""
    now = datetime.now(pytz.utc)
    return now.astimezone(pytz.timezone('Asia/Shanghai'))


class BeijingTimeFormatter(logging.Formatter):
    """使用北京时间的日志格式化器"""
    
    def formatTime(self, record, datefmt=None):
        """格式化时间为北京时间"""
        t = get_now()
        if datefmt:
            s = t.strftime(datefmt)
        else:
            s = t.strftime("%Y-%m-%d %H:%M:%S")
        return s


class Logger:
    """日志封装类"""
    
    def __init__(self, name='TTLogger', level=logging.DEBUG):
        """
        初始化日志记录器
        
        Args:
            name: 日志记录器名称
            level: 日志级别
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 创建控制台处理器
            ch = logging.StreamHandler()
            ch.setLevel(level)
            
            # 设置自定义的日志格式化器
            formatter = BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            
            # 添加处理器到日志记录器
            self.logger.addHandler(ch)
    
    def error(self, msg, *args, **kwargs):
        """记录错误日志"""
        self.logger.error(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        """记录信息日志"""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        """记录警告日志"""
        self.logger.warning(msg, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        """记录调试日志"""
        self.logger.debug(msg, *args, **kwargs)
    
    def exception(self, msg, *args, **kwargs):
        """记录异常日志（包含堆栈信息）"""
        self.logger.exception(msg, *args, **kwargs)


def setup_telethon_logger():
    """
    配置 telethon 库的日志，使其使用北京时间
    """
    # 获取 telethon 的日志记录器
    telethon_logger = logging.getLogger('telethon')
    
    # 清除现有处理器
    telethon_logger.handlers.clear()
    
    # 创建新的处理器
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # 使用北京时间格式化器
    formatter = BeijingTimeFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    # 添加处理器
    telethon_logger.addHandler(ch)
    telethon_logger.setLevel(logging.INFO)


# 创建默认日志实例
_default_logger = Logger()


# 提供简便的函数接口
def err(msg, *args, **kwargs):
    """记录错误日志"""
    _default_logger.error(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """记录信息日志"""
    _default_logger.info(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    """记录警告日志"""
    _default_logger.warning(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """记录调试日志"""
    _default_logger.debug(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    """记录异常日志（包含堆栈信息）"""
    _default_logger.exception(msg, *args, **kwargs)


# 自动配置 telethon 日志
setup_telethon_logger()

