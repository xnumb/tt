import yaml
import argparse
import socks
from pathlib import Path


class Config:
    """配置管理类"""
    
    def __init__(self, config_path=None):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径，如果为 None 则从命令行参数读取
        """
        self._config_data = {}
        
        if config_path is None:
            config_path = self._parse_args()
        
        if config_path:
            self.load(config_path)
    
    def _parse_args(self):
        """从命令行参数解析配置文件路径"""
        parser = argparse.ArgumentParser(description='Telegram 自动化程序')
        parser.add_argument('--config', type=str, help='配置文件路径')
        args, _ = parser.parse_known_args()
        return args.config
    
    def load(self, config_path):
        """
        从 YAML 文件加载配置
        
        Args:
            config_path: 配置文件路径
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            self._config_data = yaml.safe_load(f) or {}
    
    def get(self, key, default=None):
        """
        获取配置项
        
        Args:
            key: 配置键，支持点号分隔的嵌套键，如 'database.name'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config_data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """
        设置配置项
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
        """
        keys = key.split('.')
        data = self._config_data
        
        for k in keys[:-1]:
            if k not in data or not isinstance(data[k], dict):
                data[k] = {}
            data = data[k]
        
        data[keys[-1]] = value
    
    @property
    def proxy(self):
        """
        获取代理配置
        
        Returns:
            代理元组 (socks.HTTP, host, port) 或 None
        """
        use_proxy = self.get('proxy.enabled', False)
        if not use_proxy:
            return None
        
        proxy_type = self.get('proxy.type', 'http').lower()
        host = self.get('proxy.host', '127.0.0.1')
        port = self.get('proxy.port', 7890)
        
        # 映射代理类型
        proxy_type_map = {
            'http': socks.HTTP,
            'socks5': socks.SOCKS5,
            'socks4': socks.SOCKS4,
        }
        
        proxy_type_enum = proxy_type_map.get(proxy_type, socks.HTTP)
        return (proxy_type_enum, host, port)
    
    def to_dict(self):
        """
        将配置转换为字典
        
        Returns:
            配置字典
        """
        return self._config_data.copy()
    
    def save(self, config_path):
        """
        保存配置到 YAML 文件
        
        Args:
            config_path: 配置文件路径
        """
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self._config_data, f, allow_unicode=True, default_flow_style=False)

