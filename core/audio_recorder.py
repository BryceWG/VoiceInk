import sounddevice as sd
import numpy as np
import wave
import io
import threading
import time

class AudioRecorder:
    def __init__(self):
        self.sample_rate = 44100
        self.channels = 1
        self.frames = []
        self.recording = False
        self.stream = None
        self._lock = threading.Lock()
        self.audio_callback = None  # 添加回调函数
        
    def set_audio_callback(self, callback):
        """设置音频数据回调"""
        self.audio_callback = callback
        
    def start_recording(self):
        with self._lock:
            self.frames = []
            self.recording = True
            
        def callback(indata, frames, time, status):
            if self.recording:
                with self._lock:
                    # 立即处理音频数据
                    if self.audio_callback:
                        self.audio_callback(indata)
                    self.frames.append(indata.copy())
        
        try:
            # 使用更激进的低延迟设置
            self.stream = sd.InputStream(
                channels=self.channels,
                samplerate=self.sample_rate,
                callback=callback,
                blocksize=256,  # 进一步减小块大小
                latency='low',
                device=None,
                extra_settings=None
            )
            # 预先启动流并等待一小段时间以确保稳定
            self.stream.start()
            time.sleep(0.05)  # 短暂等待以确保流启动
        except Exception as e:
            self.recording = False
            raise Exception(f"录音启动失败: {str(e)}")
    
    def stop_recording(self):
        if not self.stream:
            return None
            
        self.recording = False
        try:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            
            with self._lock:
                if not self.frames:  # 检查是否有录音数据
                    return None
                    
                audio_data = np.concatenate(self.frames, axis=0)
                byte_io = io.BytesIO()
                
                with wave.open(byte_io, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(2)
                    wf.setframerate(self.sample_rate)
                    wf.writeframes((audio_data * 32767).astype(np.int16))
                
                return byte_io.getvalue()
                
        except Exception as e:
            raise Exception(f"录音停止失败: {str(e)}")
        finally:
            self.frames = []
