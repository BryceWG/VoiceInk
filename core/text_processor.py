import openai
import requests

class TextProcessor:
    def __init__(self, config_manager):
        self.config = config_manager
        
    def process(self, text):
        provider = self.config.config["transcription_settings"]["post_process_provider"]
        prompt = self.config.config["transcription_settings"]["post_process_prompt"]
        
        if provider == "openai":
            return self._process_openai(text, prompt)
        elif provider == "groq":
            return self._process_groq(text, prompt)
            
    def _process_openai(self, text, prompt):
        """使用OpenAI进行后处理"""
        settings = self.config.config["api_settings"]["post_process"]["openai"]
        api_key = settings["api_key"]
        api_url = settings["api_url"]
        model = settings["model"]
        
        if not api_key:
            raise Exception("请先配置OpenAI后处理API密钥")
            
        client = openai.OpenAI(
            api_key=api_key,
            base_url=api_url
        )
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI后处理失败: {str(e)}")
            
    def _process_groq(self, text, prompt):
        """使用Groq进行后处理"""
        # 使用转录服务的Groq凭据
        settings = self.config.config["api_settings"]["transcription"]["groq"]
        api_key = settings["api_key"]
        api_url = settings["api_url"]
        model = self.config.config["api_settings"]["post_process"]["groq"]["model"]
        
        if not api_key:
            raise Exception("请先配置Groq API密钥")
            
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        json_data = {
            "model": model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        }
        
        response = requests.post(
            f"{api_url}/chat/completions",
            headers=headers,
            json=json_data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Groq后处理失败: {response.text}")
