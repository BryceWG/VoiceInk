import json
import os
import time

class ConfigManager:
    def __init__(self):
        self.config_file = "config.json"
        self.history_file = "history.json"
        self.default_config = {
            "general_settings": {
                "insert_method": "clipboard",
                "keyboard_interval": 0.01,
                "enable_logging": False
            },
            "api_settings": {
                # 转录服务设置
                "transcription": {
                    "openai": {
                        "api_key": "",
                        "api_url": "https://api.openai.com/v1",
                        "model": "whisper-1"
                    },
                    "groq": {
                        "api_key": "",
                        "api_url": "https://api.groq.com/openai/v1",  # Groq固定URL
                        "model": "whisper-large-v3"
                    },
                    "custom": {
                        "api_key": "",
                        "api_url": "",
                        "model": ""
                    }
                },
                # 后处理服务设置
                "post_process": {
                    "openai": {
                        "api_key": "",  # 独立的OpenAI后处理API密钥
                        "api_url": "https://api.openai.com/v1",
                        "model": "gpt-3.5-turbo"
                    },
                    "groq": {
                        "model": "mixtral-8x7b-32768"  # 使用transcription.groq的凭据
                    }
                }
            },
            "transcription_settings": {
                "provider": "openai",  # openai, groq, custom
                "post_process": False,
                "post_process_provider": "openai",  # 只保留 openai, groq
                "post_process_prompt": "修正文本中的错误，保持原意",
                "wave_window_position": "right-middle",
                "wave_window_custom_pos": {"x": 0, "y": 0},
                "remove_punctuation": True,
                "punctuation_to_remove": "。，,.?？！!",
                "remove_emoji": True
            },
            "audio_settings": {
                "sample_rate": 44100,
                "channels": 1,
                "trigger_press_time": 0.1,
                "min_press_time": 0.3,
                "max_record_time": 60.0
            },
            "history_settings": {
                "max_days": 30,
                "enabled": True
            }
        }
        self.load_config()
        self.load_history()
        
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                # 合并保存的配置和默认配置，确保新添加的配置项存在
                self.config = self.default_config.copy()
                for section in saved_config:
                    if section in self.config:
                        self.config[section].update(saved_config[section])
        else:
            self.config = self.default_config.copy()
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
            
    def load_history(self):
        """加载历史记录"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        else:
            self.history = {}
            
    def save_history(self):
        """保存历史记录"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)
            
    def add_history(self, text):
        """添加历史记录"""
        if not self.config["history_settings"]["enabled"]:
            return
            
        date = time.strftime("%Y-%m-%d")
        timestamp = time.strftime("%H:%M:%S")
        
        if date not in self.history:
            self.history[date] = []
            
        self.history[date].append({
            "text": text,
            "time": timestamp
        })
        
        # 清理超过最大天数的记录
        dates = sorted(self.history.keys(), reverse=True)
        max_days = self.config["history_settings"]["max_days"]
        if len(dates) > max_days:
            for old_date in dates[max_days:]:
                del self.history[old_date]
                
        self.save_history()
