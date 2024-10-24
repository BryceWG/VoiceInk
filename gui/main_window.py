from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QStatusBar, QScrollArea,
                           QSystemTrayIcon, QMenu, QStyle, QApplication)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize  # 从 QtCore 导入 QSize
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from .settings_dialog import SettingsDialog
from .wave_visualizer import WaveVisualizerWindow
from core.transcription_manager import TranscriptionManager
import time
import os
from utils.resource_helper import get_resource_path

class MainWindow(QMainWindow):
    trigger_timeout = pyqtSignal()
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.transcription_manager = TranscriptionManager(config_manager)
        self.recording_start_time = 0
        self.history_window = None  # 添加历史记录窗口的引用
        self._quitting = False  # 添加退出标志
        self.wave_window = None
        
        # 修改图标加载
        icon_path = get_resource_path(os.path.join("resources", "app.ico"))
        self.app_icon = QIcon(icon_path)
        self.setWindowIcon(self.app_icon)
        
        # 初始化统托盘
        self.setup_tray()
        
        # 初始化定时器
        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.update_recording_time)
        
        self.trigger_timer = QTimer()
        self.trigger_timer.setSingleShot(True)
        self.trigger_timer.timeout.connect(self.trigger_timeout.emit)
        
        # 加载样式表
        self.load_styles()
        
        self.init_ui()
        
    def load_styles(self):
        """加载样式，移除所有可能导致警告的属性"""
        # 基本样式
        base_style = """
        * {
            font-family: "Microsoft YaHei UI";
            font-size: 10pt;
        }
        
        #titleLabel {
            font-size: 24pt;
            font-weight: bold;
            color: #2c3e50;
        }
        
        #subtitleLabel {
            font-size: 14pt;
            color: #34495e;
        }
        
        #statusContainer {
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        
        #statusLabel {
            color: #2c3e50;
        }
        
        #recordingTimeLabel {
            font-size: 12pt;
            color: #2980b9;
        }
        
        QPushButton {
            padding: 8px 16px;
            border-radius: 4px;
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #2472a4;
        }
        
        QScrollArea {
            border: none;
        }
        
        QMenu {
            background-color: white;
            border: 1px solid #dcdcdc;
            padding: 5px;
        }
        
        QMenu::item {
            padding: 5px 25px 5px 30px;
            border: 1px solid transparent;
        }
        
        QMenu::item:selected {
            background-color: #3498db;
            color: white;
        }
        """
        
        # 直接设置样式，不从文件加载
        self.setStyleSheet(base_style)
        
        # 设置基本字体
        font = QFont("Microsoft YaHei UI", 10)
        self.setFont(font)
        
    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        
        # 修改多尺寸图标加载
        icon = QIcon()
        icon_sizes = [16, 24, 32, 48, 256]
        for size in icon_sizes:
            icon_path = get_resource_path(os.path.join(
                "resources", "icons", f"{size}x{size}", "app.png"
            ))
            if os.path.exists(icon_path):
                icon.addFile(icon_path, QSize(size, size))
        
        # 修改后备图标加载
        if icon.isNull():
            ico_path = get_resource_path(os.path.join("resources", "app.ico"))
            if os.path.exists(ico_path):
                icon = QIcon(ico_path)
        
        if not icon.isNull():
            self.app_icon = icon
            self.tray_icon.setIcon(self.app_icon)
            self.setWindowIcon(self.app_icon)
        
        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = tray_menu.addAction(self.app_icon, "显示主界面")
        show_action.triggered.connect(self.show_and_activate)
        
        history_action = tray_menu.addAction(self.app_icon, "历史记录")
        history_action.triggered.connect(self.show_history)
        
        settings_action = tray_menu.addAction(self.app_icon, "设置")
        settings_action.triggered.connect(self.show_settings)
        
        tray_menu.addSeparator()
        quit_action = tray_menu.addAction(self.app_icon, "退出")
        quit_action.triggered.connect(self.quit_application)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # 托盘图标单击和双击事件
        self.tray_icon.activated.connect(self.tray_icon_activated)
    
    def tray_icon_activated(self, reason):
        # 单击或双击都显示主窗口
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, 
                     QSystemTrayIcon.ActivationReason.DoubleClick):
            self.show_and_activate()
            
    def show_and_activate(self):
        """显示并激活窗口"""
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized)  # 取消最小化
        self.activateWindow()  # 激活窗口
    
    def closeEvent(self, event):
        if self.tray_icon.isVisible() and not self._quitting:
            self.hide()
            self.tray_icon.showMessage(
                "VoiceInk",  # 修改通知标题
                "程序已最小化到系统托盘，双击图标可以重打开窗口。",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
            event.ignore()
        else:
            event.accept()
            
    def init_ui(self):
        self.setWindowTitle('VoiceInk')  # 修改窗口标题
        self.setMinimumSize(400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("VoiceInk")  # 修改主标题
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 副标题
        subtitle_label = QLabel("声音化墨 - 智能语音输入助手")  # 添加中文副标题
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # 说明标签
        instructions = QLabel(
            "🎤 按住 Ctrl 键开始录音\n"
            "🔄 松开 Ctrl 键结束录音并转写\n"
            "📝 转写文本将自动插入到当前焦点位置"
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)
        
        # 添加按钮局
        buttons_layout = QHBoxLayout()
        
        # 设置按钮
        settings_btn = QPushButton("⚙️ 设置")
        settings_btn.clicked.connect(self.show_settings)
        buttons_layout.addWidget(settings_btn)
        
        # 历史记录按钮
        history_btn = QPushButton("📋 历史记录")
        history_btn.clicked.connect(self.show_history)
        buttons_layout.addWidget(history_btn)
        
        layout.addLayout(buttons_layout)
        
        # 录音时长标签
        self.recording_time_label = QLabel("录音时长: 0.0秒")
        self.recording_time_label.setObjectName("recordingTimeLabel")
        self.recording_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.recording_time_label)
        
        layout.addStretch()
        
        # 创建一个固定高度的状态显示区域
        status_container = QWidget()
        status_container.setFixedHeight(100)
        status_container.setObjectName("statusContainer")  # 添加对象名以便应用样式
        status_layout = QVBoxLayout(status_container)
        status_layout.setContentsMargins(10, 10, 10, 10)  # 添加内边距
        
        self.status_label = QLabel()
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        
        layout.addWidget(status_container)
        
        # 移除状态栏
        # self.status_bar = QStatusBar()
        # self.setStatusBar(self.status_bar)
    
    def show_settings(self):
        dialog = SettingsDialog(self.config_manager)
        dialog.exec()
    
    def update_status(self, message):
        """更新状态信息"""
        self.status_label.setText(message)
        # 移除对 status_bar 的引用，因为我在使用固定高度的状态容器
    
    def transcribe_audio(self, audio_data):
        """音频转写的槽函数"""
        if not audio_data:
            self.update_status("错误: 未获取到录音数据")
            return
            
        self.update_status("正在转写...")
        try:
            text = self.transcription_manager.transcribe(audio_data)
            self.transcription_manager.insert_text(text)
            # 显示转录文本
            self.update_status(f"转写完成\n转录文本：{text}")
        except Exception as e:
            error_msg = f"错误: {str(e)}\n请查看logs文件夹中的日志文件获取详细信息"
            print(error_msg)
            self.update_status(error_msg)
    
    def start_recording(self):
        """录音开始的槽函数"""
        self.recording_start_time = time.time()
        self.recording_timer.start(100)
        self.update_status("正在录音...")
        
        # 显示波形窗口
        if not self.wave_window:
            self.wave_window = WaveVisualizerWindow(self.config_manager)
        self.wave_window.show()
        
    def stop_recording(self):
        """录音结束的槽函数"""
        self.recording_timer.stop()
        self.recording_time_label.setText("录音时长: 0.0秒")
        
        # 隐藏波形窗口
        if self.wave_window:
            self.wave_window.hide()
            
    def update_recording_time(self):
        """更新录音时长显示"""
        duration = time.time() - self.recording_start_time
        self.recording_time_label.setText(f"录音时长: {duration:.1f}秒")
    
    def start_trigger_timer(self):
        """启动录音触发定时器"""
        trigger_time = int(self.config_manager.config["audio_settings"]["trigger_press_time"] * 1000)
        self.trigger_timer.start(trigger_time)
    
    def stop_trigger_timer(self):
        """停止录音触发定时器"""
        self.trigger_timer.stop()

    def show_history(self):
        """显示历史记录窗口"""
        from .history_window import HistoryWindow
        if not self.history_window:
            self.history_window = HistoryWindow(self.config_manager)
        self.history_window.show()
        self.history_window.activateWindow()  # 激活窗口

    def quit_application(self):
        """完全退出应用程序"""
        self.tray_icon.hide()  # 隐藏托盘图标
        QApplication.quit()  # 退出应用

    def update_wave_data(self, data):
        """更新波形显示"""
        if self.wave_window:
            self.wave_window.update_wave_data(data)

    def config_updated(self):
        """配置更新后的处理"""
        if hasattr(self, 'keyboard_listener'):
            self.keyboard_listener.update_settings()
        
        # 更新波形窗口位置
        if self.wave_window:
            self.wave_window.update_position()
