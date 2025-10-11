from telethon import TelegramClient, errors


class TGClient:
    """Telegram 客户端封装类"""
    
    def __init__(self, session_name, api_id, api_hash, proxy=None):
        """
        初始化 Telegram 客户端
        
        Args:
            session_name: 会话文件名
            api_id: Telegram API ID
            api_hash: Telegram API Hash
            proxy: 代理设置，格式如 (socks.HTTP, "127.0.0.1", 7890)
        """
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.proxy = proxy
        self.client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)

    async def send_login_code(self, phone):
        """
        发送登录验证码
        
        Args:
            phone: 手机号
            
        Returns:
            code_hash: 验证码哈希，如果已登录则返回空字符串
        """
        if await self.is_auth():
            return ""
        
        code_hash = ""
        try:
            res = await self.client.send_code_request(phone)
            code_hash = res.phone_code_hash
        except Exception as e:
            print(f"发送验证码失败: {e}")
        
        await self.client.disconnect()
        return code_hash

    async def send_login(self, phone, pwd, code, code_hash):
        """
        执行登录
        
        Args:
            phone: 手机号
            pwd: 两步验证密码（如果有）
            code: 验证码
            code_hash: 验证码哈希
            
        Returns:
            me: 用户信息，登录失败返回 None
        """
        await self.client.connect()
        
        if await self.client.is_user_authorized():
            return None
        
        me = None
        try:
            await self.client.sign_in(phone, code=code, phone_code_hash=code_hash)
            me = await self.client.get_me()
        except errors.CodeInvalidError:
            print("验证码无效")
        except errors.SessionPasswordNeededError:
            # 需要两步验证密码
            await self.client.sign_in(password=pwd)
            me = await self.client.get_me()
        except Exception as e:
            print(f"登录失败: {e}")
        
        await self.client.disconnect()
        return me

    async def is_auth(self):
        """
        检查是否已授权
        
        Returns:
            bool: 是否已授权
        """
        if self.client.is_connected():
            return await self.client.is_user_authorized()
        else:
            try:
                await self.client.connect()
                return await self.client.is_user_authorized()
            except Exception as e:
                print(f"连接异常: {e}")
                return False

    async def get_me(self):
        """
        获取当前用户信息
        
        Returns:
            用户信息对象
        """
        if not await self.is_auth():
            return None
        return await self.client.get_me()

    async def start(self, phone=None, password=None, bot_token=None):
        """
        启动客户端（支持用户和机器人两种模式）
        
        Args:
            phone: 用户手机号
            password: 两步验证密码
            bot_token: 机器人 token
        """
        if bot_token:
            await self.client.start(bot_token=bot_token)
        else:
            await self.client.start(phone=phone, password=password)

    async def disconnect(self):
        """断开连接"""
        if self.client.is_connected():
            await self.client.disconnect()

    async def send_message(self, entity, message):
        """
        发送消息
        
        Args:
            entity: 目标实体（用户名、ID 或实体对象）
            message: 消息内容
        """
        return await self.client.send_message(entity, message)

    async def log_out(self):
        """登出账号"""
        return await self.client.log_out()

    def on(self, event):
        """
        事件装饰器
        
        Args:
            event: 事件类型
        """
        return self.client.on(event)

    async def run_until_disconnected(self):
        """运行直到断开连接"""
        await self.client.run_until_disconnected()

