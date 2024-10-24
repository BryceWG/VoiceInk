import logging
import os
from datetime import datetime
import glob

class Logger:
    def __init__(self, config_manager=None):
        self.config = config_manager
        if config_manager is None:
            self.enabled = False
        else:
            self.enabled = config_manager.config["general_settings"]["enable_logging"]
        
        # 创建一个空的logger
        self.logger = logging.getLogger(__name__)
        self.logger.handlers = []  # 清除所有已存在的handlers
        
        if not self.enabled:
            self.logger.addHandler(logging.NullHandler())
            return
            
        # 创建logs目录
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # 清理旧的日志文件
        self._cleanup_old_logs()
            
        # 设置日志文件名
        log_file = 'logs/app.log'
        
        # 配置日志格式
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 设置日志级别
        self.logger.setLevel(logging.DEBUG)
    
    def _cleanup_old_logs(self):
        """清理旧的日志文件"""
        try:
            files = glob.glob('logs/*.log')
            for f in files:
                try:
                    os.remove(f)
                except:
                    pass
        except:
            pass
    
    def debug(self, message):
        if self.enabled:
            self.logger.debug(message)
    
    def info(self, message):
        if self.enabled:
            self.logger.info(message)
    
    def warning(self, message):
        if self.enabled:
            self.logger.warning(message)
    
    def error(self, message):
        if self.enabled:
            self.logger.error(message)
