from pynput import keyboard
from core.audio_recorder import AudioRecorder
import time
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class KeyboardListener(QObject):
    recording_started = pyqtSignal()  # 录音开始信号
    recording_stopped = pyqtSignal()  # 录音结束信号
    transcribe_requested = pyqtSignal(bytes)  # 转写请求信号
    start_timer_requested = pyqtSignal()  # 新增：请求启动定时器的信号
    stop_timer_requested = pyqtSignal()   # 新增：请求停止定时器的信号
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.recorder = AudioRecorder()
        self.is_recording = False
        self.is_key_pressed = False
        self.press_time = 0  # 记录按键按下的时间
        self.trigger_press_time = self.main_window.config_manager.config["audio_settings"]["trigger_press_time"]
        self.min_press_time = self.main_window.config_manager.config["audio_settings"]["min_press_time"]
        self.max_record_time = self.main_window.config_manager.config["audio_settings"]["max_record_time"]
        
        # 连接信号
        self.recording_started.connect(self.main_window.start_recording)
        self.recording_stopped.connect(self.main_window.stop_recording)
        self.transcribe_requested.connect(self.main_window.transcribe_audio)
        self.start_timer_requested.connect(self.main_window.start_trigger_timer)
        self.stop_timer_requested.connect(self.main_window.stop_trigger_timer)
        
        # 连接主窗口的触发信号
        self.main_window.trigger_timeout.connect(self.start_recording)
        
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        
        self.recorder.set_audio_callback(self.main_window.update_wave_data)
    
    def start_recording(self):
        """实际启动录音的函数"""
        if self.is_key_pressed:  # 确保按键仍然被按住
            try:
                self.is_recording = True
                self.recorder.start_recording()
                self.recording_started.emit()
            except Exception as e:
                print(f"录音启动失败: {str(e)}")
                self.is_recording = False
    
    def on_press(self, key):
        if key == keyboard.Key.ctrl_l and not self.is_key_pressed:
            self.is_key_pressed = True
            self.press_time = time.time()
            # 发送启动定时器的请求
            self.start_timer_requested.emit()
    
    def on_release(self, key):
        if key == keyboard.Key.ctrl_l and self.is_key_pressed:
            self.is_key_pressed = False
            # 发送停止定时器的请求
            self.stop_timer_requested.emit()
            press_duration = time.time() - self.press_time
            
            if self.is_recording:
                self.is_recording = False
                self.recording_stopped.emit()
                
                if press_duration < self.min_press_time:
                    self.recorder.stop_recording()
                    self.main_window.update_status(
                        f"录音时间太短(小于{self.min_press_time}秒)，已取消"
                    )
                    return
                    
                if press_duration > self.max_record_time:
                    self.main_window.update_status(
                        f"录音时间过长(超过{self.max_record_time}秒)，仅保留前{self.max_record_time}秒"
                    )
                
                audio_data = self.recorder.stop_recording()
                if audio_data:
                    self.transcribe_requested.emit(audio_data)
                else:
                    self.main_window.update_status("未检测到录音数据")
            else:
                self.main_window.update_status("按键时间太短，未启动录音")

    def update_settings(self):
        """更新设置"""
        self.trigger_press_time = self.main_window.config_manager.config["audio_settings"]["trigger_press_time"]
        self.min_press_time = self.main_window.config_manager.config["audio_settings"]["min_press_time"]
        self.max_record_time = self.main_window.config_manager.config["audio_settings"]["max_record_time"]
