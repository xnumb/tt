#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的安装测试脚本
用于验证 TT 库是否正确安装
"""

def test_imports():
    """测试所有模块是否可以正确导入"""
    try:
        from tt import (
            DB, TGClient, Logger, Config, TelegramApp, TaskManager,
            info, err, warn, debug, exception, get_now
        )
        print("✓ 所有模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False


def test_logger():
    """测试日志功能"""
    try:
        from tt import info, warn, err, debug, get_now
        info("测试信息日志")
        warn("测试警告日志")
        # err("测试错误日志")  # 注释掉以免吓到用户
        debug("测试调试日志")
        now = get_now()
        print(f"✓ 日志功能正常，当前北京时间: {now}")
        return True
    except Exception as e:
        print(f"✗ 日志测试失败: {e}")
        return False


def test_config():
    """测试配置功能"""
    try:
        from tt import Config
        import tempfile
        import os
        
        # 创建临时配置文件
        config_content = """
proxy:
  enabled: true
  host: 127.0.0.1
  port: 7890

database:
  name: test_db
  password: test_pwd

telegram:
  api_id: 12345
  api_hash: test_hash
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_content)
            temp_file = f.name
        
        # 测试配置加载
        config = Config(temp_file)
        assert config.db_name == 'test_db'
        assert config.db_password == 'test_pwd'
        assert config.api_id == 12345
        
        # 清理
        os.unlink(temp_file)
        
        print("✓ 配置功能正常")
        return True
    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False


def test_db_class():
    """测试数据库类（不实际连接）"""
    try:
        from tt import DB
        db = DB('test_db', 'test_pwd')
        assert db.db_name == 'test_db'
        assert db.pwd == 'test_pwd'
        print("✓ 数据库类初始化正常")
        return True
    except Exception as e:
        print(f"✗ 数据库类测试失败: {e}")
        return False


def test_client_class():
    """测试 Telegram 客户端类（不实际连接）"""
    try:
        from tt import TGClient
        client = TGClient('test_session', 12345, 'test_hash')
        assert client.api_id == 12345
        assert client.api_hash == 'test_hash'
        print("✓ Telegram 客户端类初始化正常")
        return True
    except Exception as e:
        print(f"✗ Telegram 客户端类测试失败: {e}")
        return False


def test_app_class():
    """测试应用框架类"""
    try:
        from tt import TelegramApp
        # 不传配置路径，避免要求配置文件
        # app = TelegramApp()
        print("✓ 应用框架类可用")
        return True
    except Exception as e:
        print(f"✗ 应用框架类测试失败: {e}")
        return False


def test_task_manager():
    """测试任务管理器"""
    try:
        from tt import TaskManager
        manager = TaskManager()
        assert len(manager) == 0
        print("✓ 任务管理器初始化正常")
        return True
    except Exception as e:
        print(f"✗ 任务管理器测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("=" * 50)
    print("TT 库安装测试")
    print("=" * 50)
    print()
    
    tests = [
        ("模块导入", test_imports),
        ("日志功能", test_logger),
        ("配置功能", test_config),
        ("数据库类", test_db_class),
        ("客户端类", test_client_class),
        ("应用框架", test_app_class),
        ("任务管理器", test_task_manager),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"\n测试 {name}...")
        if test_func():
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 50)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    if failed == 0:
        print("\n✓ TT 库安装成功！可以开始使用了。")
        print("\n下一步:")
        print("  1. 查看 README.md 了解详细使用方法")
        print("  2. 查看 example.py 了解示例代码")
        print("  3. 查看 GETTING_STARTED.md 快速开始")
        return 0
    else:
        print("\n✗ 部分测试失败，请检查安装")
        return 1


if __name__ == '__main__':
    exit(main())

