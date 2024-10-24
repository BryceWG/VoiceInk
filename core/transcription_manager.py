import openai
import google.generativeai as genai
import requests
import pyautogui
import pyperclip
from .text_processor import TextProcessor
from .logger import Logger
import time
import win32com.client
import pythoncom
import re
import emoji

class TranscriptionManager:
    def __init__(self, config_manager):
        self.config = config_manager
        self.text_processor = TextProcessor(config_manager)
        self.logger = Logger(config_manager)  # 传入 config_manager
        # 设置pyautogui的安全设置
        pyautogui.PAUSE = 0.01  # 设置操作间隔时间
        pyautogui.FAILSAFE = True  # 启用故障保护
        # 初始化 shell 对象
        try:
            pythoncom.CoInitialize()  # 初始化COM
            self.shell = win32com.client.Dispatch("WScript.Shell")
        except Exception as e:
            self.logger.error(f"COM初始化失败: {str(e)}")
            self.shell = None
            
    def transcribe(self, audio_data):
        provider = self.config.config["transcription_settings"]["provider"]
        self.logger.info(f"使用 {provider} 进行转写")
        
        text = None
        if provider == "openai":
            text = self._transcribe_openai(audio_data)
        elif provider == "groq":
            text = self._transcribe_groq(audio_data)
        elif provider == "custom":
            text = self._transcribe_custom(audio_data)
            
        # 添加到历史记录
        if text:
            self.config.add_history(text)
            
        return text
    
    def _process_text(self, text):
        """处理转写后的文本"""
        # 移除表情符号
        if self.config.config["transcription_settings"]["remove_emoji"]:
            text = emoji.replace_emoji(text, '')
            # 移除其他 Unicode 表情符号和特殊字符
            text = re.sub(r'[\U0001F300-\U0001F9FF]', '', text)
            text = re.sub(r'[\u2600-\u26FF\u2700-\u27BF]', '', text)
        
        # 移除句尾标点符号
        if self.config.config["transcription_settings"]["remove_punctuation"]:
            punctuation = self.config.config["transcription_settings"]["punctuation_to_remove"]
            while text and text[-1] in punctuation:
                text = text[:-1]
        
        # 后处理
        if self.config.config["transcription_settings"]["post_process"]:
            self.logger.info("开始后处理")
            text = self.text_processor.process(text)
            self.logger.debug(f"后处理结果: {text}")
        
        return text.strip()
    
    def _transcribe_openai(self, audio_data):
        """使用OpenAI进行转写"""
        settings = self.config.config["api_settings"]["transcription"]["openai"]
        api_key = settings["api_key"]
        api_url = settings["api_url"]
        model = settings["model"]
        
        if not api_key:
            self.logger.error("OpenAI API密钥未配置")
            raise Exception("请先在设置中配置OpenAI API密钥")
            
        client = openai.OpenAI(
            api_key=api_key,
            base_url=api_url
        )
        
        self.logger.debug(f"使用OpenAI API: {api_url}")
        self.logger.debug(f"使用模型: {model}")
        
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data)
            
        try:
            with open("temp_audio.wav", "rb") as f:
                response = client.audio.transcriptions.create(
                    model=model,
                    file=f,
                    language="zh"
                )
                text = response.text
                self.logger.info("转写成功")
                self.logger.debug(f"原始转写结果: {text}")
                
                # 处理文本
                text = self._process_text(text)
                self.logger.debug(f"处理后的结果: {text}")
                
                return text
        except Exception as e:
            self.logger.error(f"OpenAI转写失败: {str(e)}")
            raise Exception(f"OpenAI转写失败: {str(e)}")
        finally:
            import os
            if os.path.exists("temp_audio.wav"):
                os.remove("temp_audio.wav")
                
    def _transcribe_groq(self, audio_data):
        """使用Groq进行转写"""
        settings = self.config.config["api_settings"]["transcription"]["groq"]
        api_key = settings["api_key"]
        api_url = settings["api_url"]  # Groq的API URL是固定的
        model = settings["model"]
        
        if not api_key:
            self.logger.error("Groq API密钥未配置")
            raise Exception("请先在设置中配置Groq API密钥")
            
        self.logger.debug(f"使用Groq API: {api_url}")
        self.logger.debug(f"使用模型: {model}")
        
        # 保存临时音频文件
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data)
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            
            with open("temp_audio.wav", "rb") as f:
                files = {
                    'file': ('audio.wav', f, 'audio/wav')
                }
                data = {
                    'model': model,
                    'language': 'zh'
                }
                
                response = requests.post(
                    f"{api_url}/audio/transcriptions",
                    headers=headers,
                    files=files,
                    data=data
                )
                
                if response.status_code == 200:
                    text = response.json()["text"]
                    self.logger.info("转写成功")
                    self.logger.debug(f"原始转写结果: {text}")
                    
                    # 处理文本
                    text = self._process_text(text)
                    self.logger.debug(f"处理后的结果: {text}")
                    
                    return text
                else:
                    error_msg = f"Groq API错误: {response.text}"
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"Groq��写失败: {str(e)}")
            raise Exception(f"Groq转写失败: {str(e)}")
        finally:
            import os
            if os.path.exists("temp_audio.wav"):
                os.remove("temp_audio.wav")
                
    def _transcribe_custom(self, audio_data):
        """使用自定义服务进行转写（使用自定义格式）"""
        settings = self.config.config["api_settings"]["transcription"]["custom"]
        api_key = settings["api_key"]
        api_url = settings["api_url"]
        model = settings["model"]
        
        if not api_url:
            self.logger.error("自定义API URL未配置")
            raise Exception("请先在设置中配置自定义API URL")
            
        if not api_key:
            self.logger.error("自定义API密钥未配置")
            raise Exception("请先在设置中配置自定义API密钥")
            
        self.logger.debug(f"使用自定义API: {api_url}")
        self.logger.debug(f"使用模型: {model}")
        
        try:
            # 使用自定义格式构建请求
            files = {
                'file': ('audio.wav', audio_data, 'audio/wav'),
                'model': (None, model)
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            
            self.logger.info("开始调用自定义API")
            response = requests.post(api_url, files=files, headers=headers)
            
            if response.status_code == 200:
                try:
                    text = response.json()["text"]
                    self.logger.info("转写成功")
                    self.logger.debug(f"原始转写结果: {text}")
                    
                    # 处理文本
                    text = self._process_text(text)
                    self.logger.debug(f"处理后的结果: {text}")
                    
                    return text
                except KeyError:
                    error_msg = f"API响应格式错误: {response.text}"
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
            else:
                error_msg = f"API请求失败 (状态码: {response.status_code}): {response.text}"
                self.logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(f"自定义API转写失败: {str(e)}")
            raise Exception(f"自定义API转写失败: {str(e)}")
            
    def _escape_for_sendkeys(self, text):
        """转义文本以适应SendKeys方法"""
        result = ''
        for char in text:
            # 如果是ASCII字符，处理特殊字符
            if ord(char) < 128:
                if char in '~!@#$%^&*()_+{}[]|\\;:\'",./<>?`=':
                    result += '{' + char + '}'
                else:
                    result += char
            # 对于中文字符，直接使用
            else:
                result += char
        return result

    def insert_text(self, text):
        """插入文本到当前焦点位置"""
        method = self.config.config.get("general_settings", {}).get("insert_method", "clipboard")
        
        try:
            # 给应用一点时间切换焦点
            time.sleep(0.1)
            
            if method == "keyboard" and self._is_ascii_only(text):
                # ASCII文本使用pyautogui
                pyautogui.write(text, interval=0.01)
            else:
                # 默认使用剪贴板方法
                self._insert_by_clipboard(text)
                
        except Exception as e:
            self.logger.error(f"文本插入失败: {str(e)}")
            raise Exception(f"文本插入失败: {str(e)}")
            
    def _insert_by_clipboard(self, text):
        """使用剪贴板方法插入文本"""
        try:
            original = pyperclip.paste()
            pyperclip.copy(text)
            time.sleep(0.1)  # 给剪贴板操作一点时间
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)  # 给粘贴操作一点时间
            pyperclip.copy(original)  # 恢复原始剪贴板内容
        except Exception as e:
            self.logger.error(f"剪贴板操作失败: {str(e)}")
            raise Exception(f"剪贴板操作失败: {str(e)}")
    
    def _is_ascii_only(self, text):
        """检查文本是否只包含ASCII字符"""
        return all(ord(c) < 128 for c in text)

