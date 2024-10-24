from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                           QLabel, QLineEdit, QComboBox, QCheckBox, 
                           QPushButton, QGroupBox, QWidget, QMessageBox, QScrollArea)
from PyQt6.QtGui import QDoubleValidator

class SettingsDialog(QDialog):
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                font-size: 13pt;
            }
            QGroupBox {
                font-size: 14pt;
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                margin-top: 15px;
                padding-top: 12px;
            }
        """)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("设置")
        self.setMinimumSize(500, 400)  # 改为最小尺寸而不是固定尺寸
        self.resize(600, 500)  # 设置默认尺寸
        
        layout = QVBoxLayout()
        
        # 创建标签页
        tabs = QTabWidget()
        tabs.addTab(self.create_api_tab(), "API设置")
        tabs.addTab(self.create_transcription_tab(), "转写设置")
        tabs.addTab(self.create_audio_tab(), "录音设置")
        tabs.addTab(self.create_general_tab(), "文本插入设置")
        layout.addWidget(tabs)
        
        # 按钮
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        cancel_btn = QPushButton("取消")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addStretch()  # 添加弹性空间
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
    def create_api_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 转录服务设置
        trans_group = QGroupBox("转录服务设置")
        trans_layout = QVBoxLayout()
        
        # OpenAI转录设置
        trans_layout.addWidget(QLabel("OpenAI转录设置:"))
        self.trans_openai_key = QLineEdit()
        self.trans_openai_key.setText(self.config.config["api_settings"]["transcription"]["openai"]["api_key"])
        trans_layout.addWidget(QLabel("API密钥:"))
        trans_layout.addWidget(self.trans_openai_key)
        
        self.trans_openai_url = QLineEdit()
        self.trans_openai_url.setText(self.config.config["api_settings"]["transcription"]["openai"]["api_url"])
        trans_layout.addWidget(QLabel("API地址:"))
        trans_layout.addWidget(self.trans_openai_url)
        
        self.trans_openai_model = QLineEdit()
        self.trans_openai_model.setText(self.config.config["api_settings"]["transcription"]["openai"]["model"])
        trans_layout.addWidget(QLabel("模型名称:"))
        trans_layout.addWidget(self.trans_openai_model)
        
        trans_layout.addWidget(QLabel("\nGroq转录设置:"))
        self.trans_groq_key = QLineEdit()
        self.trans_groq_key.setText(self.config.config["api_settings"]["transcription"]["groq"]["api_key"])
        trans_layout.addWidget(QLabel("API密钥:"))
        trans_layout.addWidget(self.trans_groq_key)
        
        self.trans_groq_model = QLineEdit()
        self.trans_groq_model.setText(self.config.config["api_settings"]["transcription"]["groq"]["model"])
        trans_layout.addWidget(QLabel("模型名称:"))
        trans_layout.addWidget(self.trans_groq_model)
        
        trans_layout.addWidget(QLabel("\n自定义转录服务设置:"))
        self.trans_custom_key = QLineEdit()
        self.trans_custom_key.setText(self.config.config["api_settings"]["transcription"]["custom"]["api_key"])
        trans_layout.addWidget(QLabel("API密钥:"))
        trans_layout.addWidget(self.trans_custom_key)
        
        self.trans_custom_url = QLineEdit()
        self.trans_custom_url.setText(self.config.config["api_settings"]["transcription"]["custom"]["api_url"])
        trans_layout.addWidget(QLabel("API地址:"))
        trans_layout.addWidget(self.trans_custom_url)
        
        self.trans_custom_model = QLineEdit()
        self.trans_custom_model.setText(self.config.config["api_settings"]["transcription"]["custom"]["model"])
        trans_layout.addWidget(QLabel("模型名称:"))
        trans_layout.addWidget(self.trans_custom_model)
        
        trans_group.setLayout(trans_layout)
        layout.addWidget(trans_group)
        
        # 后处理服务设置
        post_group = QGroupBox("后处理服务设置")
        post_layout = QVBoxLayout()
        
        post_layout.addWidget(QLabel("OpenAI后处理设置:"))
        self.post_openai_key = QLineEdit()
        self.post_openai_key.setText(self.config.config["api_settings"]["post_process"]["openai"]["api_key"])
        post_layout.addWidget(QLabel("API密钥:"))
        post_layout.addWidget(self.post_openai_key)
        
        self.post_openai_url = QLineEdit()
        self.post_openai_url.setText(self.config.config["api_settings"]["post_process"]["openai"]["api_url"])
        post_layout.addWidget(QLabel("API地址:"))
        post_layout.addWidget(self.post_openai_url)
        
        self.post_openai_model = QLineEdit()
        self.post_openai_model.setText(self.config.config["api_settings"]["post_process"]["openai"]["model"])
        post_layout.addWidget(QLabel("模型名称:"))
        post_layout.addWidget(self.post_openai_model)
        
        post_layout.addWidget(QLabel("\nGroq后处理设置:"))
        self.post_groq_model = QLineEdit()
        self.post_groq_model.setText(self.config.config["api_settings"]["post_process"]["groq"]["model"])
        post_layout.addWidget(QLabel("模型名称:"))
        post_layout.addWidget(self.post_groq_model)
        
        post_group.setLayout(post_layout)
        layout.addWidget(post_group)
        
        # 添加滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        
        widget.setLayout(main_layout)
        return widget
        
    def create_transcription_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 转写设置
        trans_group = QGroupBox("转写设置")
        trans_layout = QVBoxLayout()
        
        self.provider = QComboBox()
        self.provider.addItems(["openai", "groq", "custom"])
        self.provider.setCurrentText(self.config.config["transcription_settings"]["provider"])
        trans_layout.addWidget(QLabel("转写提供商:"))
        trans_layout.addWidget(self.provider)
        
        trans_group.setLayout(trans_layout)
        layout.addWidget(trans_group)  # 添加转写设置组到主布局
        
        # 后处理设置
        post_group = QGroupBox("后处理设置")
        post_layout = QVBoxLayout()
        
        self.post_process = QCheckBox("启用后处理")
        self.post_process.setChecked(self.config.config["transcription_settings"]["post_process"])
        post_layout.addWidget(self.post_process)
        
        self.post_provider = QComboBox()
        self.post_provider.addItems(["openai", "groq"])  # 只保留 openai 和 groq
        self.post_provider.setCurrentText(self.config.config["transcription_settings"]["post_process_provider"])
        post_layout.addWidget(QLabel("后处理提供商:"))
        post_layout.addWidget(self.post_provider)
        
        self.post_prompt = QLineEdit()
        self.post_prompt.setText(self.config.config["transcription_settings"]["post_process_prompt"])
        post_layout.addWidget(QLabel("后处理提示词:"))
        post_layout.addWidget(self.post_prompt)
        
        post_group.setLayout(post_layout)
        layout.addWidget(post_group)
        
        # 标点符和表情符号处理设置
        punct_group = QGroupBox("文本清理设置")
        punct_layout = QVBoxLayout()
        
        # 标点符号设置
        self.remove_punctuation = QCheckBox("移除句尾标点符号")
        self.remove_punctuation.setChecked(
            self.config.config["transcription_settings"]["remove_punctuation"]
        )
        punct_layout.addWidget(self.remove_punctuation)
        
        punct_layout.addWidget(QLabel("要移除的标点符号:"))
        self.punctuation_to_remove = QLineEdit()
        self.punctuation_to_remove.setText(
            self.config.config["transcription_settings"]["punctuation_to_remove"]
        )
        self.punctuation_to_remove.setPlaceholderText("例如: 。，,.?？！!")
        punct_layout.addWidget(self.punctuation_to_remove)
        
        # 表情符号设置
        self.remove_emoji = QCheckBox("移除表情符号")
        self.remove_emoji.setChecked(
            self.config.config["transcription_settings"]["remove_emoji"]
        )
        punct_layout.addWidget(self.remove_emoji)
        
        # 添加说明文本
        help_text = QLabel(
            "提示：\n"
            "- 标点符号：只会移除文本末尾的指定标点符号\n"
            "- 表情符号：会移除文本中所有的emoji和Unicode表情符号"
        )
        help_text.setWordWrap(True)
        punct_layout.addWidget(help_text)
        
        punct_group.setLayout(punct_layout)
        layout.addWidget(punct_group)
        
        # 波形窗口位置设置
        wave_group = QGroupBox("波形显示设置")
        wave_layout = QVBoxLayout()
        
        self.wave_position = QComboBox()
        positions = [
            ("right-middle", "屏幕右侧中间"),
            ("left-top", "屏幕左上角"),
            ("right-top", "屏幕右上角"),
            ("left-bottom", "屏幕左下角"),
            ("right-bottom", "屏幕右下角"),
            ("custom", "自定义位置")
        ]
        for value, text in positions:
            self.wave_position.addItem(text, value)  # 使用 addItem 添加显示文本和数据
            
        # 设置当前值
        current_pos = self.config.config["transcription_settings"]["wave_window_position"]
        index = self.wave_position.findData(current_pos)  # 根据数据查找索引
        if index >= 0:
            self.wave_position.setCurrentIndex(index)
            
        wave_layout.addWidget(QLabel("波形窗口位置:"))
        wave_layout.addWidget(self.wave_position)
        
        # 添加说明文本
        help_text = QLabel(
            "提示：\n"
            "- 选择'自定义位置'后，可以拖动波形窗口到任意位置\n"
            "- 窗口位置会被记住，下次显示时会在相同位置"
        )
        help_text.setWordWrap(True)
        wave_layout.addWidget(help_text)
        
        wave_group.setLayout(wave_layout)
        layout.addWidget(wave_group)
        
        # 添加弹性空间
        layout.addStretch()
        
        # 设置滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        
        # 创建最外层布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        
        widget.setLayout(main_layout)
        return widget
        
    def update_post_model(self, provider):
        """更新后处理模型输入框的默认值"""
        default_models = {
            "openai": "gpt-3.5-turbo",
            "groq": "mixtral-8x7b-32768",
            "gemini": "gemini-pro"
        }
        current_model = self.config.config["transcription_settings"]["post_process_models"][provider]
        self.post_model.setText(current_model or default_models.get(provider, ""))
        
    def create_audio_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 录音设置组
        audio_group = QGroupBox("录音设置")
        audio_layout = QVBoxLayout()
        
        # 最小按压时间设置
        press_time_layout = QHBoxLayout()
        press_time_layout.addWidget(QLabel("最小按压时间(秒):"))
        self.min_press_time = QLineEdit()
        self.min_press_time.setText(str(self.config.config["audio_settings"]["min_press_time"]))
        self.min_press_time.setPlaceholderText("默认: 0.3")
        # 限制输入为数字
        self.min_press_time.setValidator(QDoubleValidator(0.1, 5.0, 1))
        press_time_layout.addWidget(self.min_press_time)
        audio_layout.addLayout(press_time_layout)
        
        # 最大录音时间设置
        max_time_layout = QHBoxLayout()
        max_time_layout.addWidget(QLabel("最大录音时间(秒):"))
        self.max_record_time = QLineEdit()
        self.max_record_time.setText(str(self.config.config["audio_settings"]["max_record_time"]))
        self.max_record_time.setPlaceholderText("默认: 60")
        self.max_record_time.setValidator(QDoubleValidator(1.0, 300.0, 1))
        max_time_layout.addWidget(self.max_record_time)
        audio_layout.addLayout(max_time_layout)
        
        # 添加录音触发时间设置
        trigger_time_layout = QHBoxLayout()
        trigger_time_layout.addWidget(QLabel("录音触发时间(秒):"))
        self.trigger_press_time = QLineEdit()
        self.trigger_press_time.setText(str(self.config.config["audio_settings"]["trigger_press_time"]))
        self.trigger_press_time.setPlaceholderText("默认: 0.1")
        self.trigger_press_time.setValidator(QDoubleValidator(0.05, 0.5, 2))
        trigger_time_layout.addWidget(self.trigger_press_time)
        audio_layout.addLayout(trigger_time_layout)
        
        # 更新帮助文本
        help_text = QLabel(
            "提示：\n"
            "- 录音触发时间：按住Ctrl键超过此时间才会开始录音\n"
            "- 最小按压时间：按住Ctrl键少于此时��将不会触发转写\n"
            "- 最大录音时间：超过此时间将自动停止录音\n"
            "- 建议录音触发时间设置在0.05-0.2秒之间\n"
            "- 建议最小按压时间设置在0.3-1.0秒之间"
        )
        help_text.setWordWrap(True)
        audio_layout.addWidget(help_text)
        
        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
        
    def create_general_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 文本插入设置
        insert_group = QGroupBox("文本插入设置")
        insert_layout = QVBoxLayout()
        
        self.insert_method = QComboBox()
        self.insert_method.addItems(["clipboard", "keyboard"])
        self.insert_method.setCurrentText(
            self.config.config["general_settings"]["insert_method"]
        )
        insert_layout.addWidget(QLabel("插入方式:"))
        insert_layout.addWidget(self.insert_method)
        
        # 添加说明文本
        help_text = QLabel(
            "插入方式说明：\n"
            "- clipboard: 使用剪贴板（推荐，支持所有字符）\n"
            "- keyboard: 模拟键盘输入（仅支持英文字符）"
        )
        help_text.setWordWrap(True)
        insert_layout.addWidget(help_text)
        
        insert_group.setLayout(insert_layout)
        layout.addWidget(insert_group)
        
        # 日志设置
        log_group = QGroupBox("日志设置")
        log_layout = QVBoxLayout()
        
        self.enable_logging = QCheckBox("启用日志记录")
        self.enable_logging.setChecked(
            self.config.config["general_settings"]["enable_logging"]
        )
        log_layout.addWidget(self.enable_logging)
        
        log_help = QLabel(
            "启用后将在logs文件夹中保存��序运行日志\n"
            "仅保留最新的日志文件"
        )
        log_help.setWordWrap(True)
        log_layout.addWidget(log_help)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def save_settings(self):
        try:
            # 保存转录服务设置
            self.config.config["api_settings"]["transcription"]["openai"]["api_key"] = self.trans_openai_key.text()
            self.config.config["api_settings"]["transcription"]["openai"]["api_url"] = self.trans_openai_url.text()
            self.config.config["api_settings"]["transcription"]["openai"]["model"] = self.trans_openai_model.text()
            
            self.config.config["api_settings"]["transcription"]["groq"]["api_key"] = self.trans_groq_key.text()
            self.config.config["api_settings"]["transcription"]["groq"]["model"] = self.trans_groq_model.text()
            
            self.config.config["api_settings"]["transcription"]["custom"]["api_key"] = self.trans_custom_key.text()
            self.config.config["api_settings"]["transcription"]["custom"]["api_url"] = self.trans_custom_url.text()
            self.config.config["api_settings"]["transcription"]["custom"]["model"] = self.trans_custom_model.text()
            
            # 保存后处理服务设置
            self.config.config["api_settings"]["post_process"]["openai"]["api_key"] = self.post_openai_key.text()
            self.config.config["api_settings"]["post_process"]["openai"]["api_url"] = self.post_openai_url.text()
            self.config.config["api_settings"]["post_process"]["openai"]["model"] = self.post_openai_model.text()
            
            self.config.config["api_settings"]["post_process"]["groq"]["model"] = self.post_groq_model.text()
            
            # 保存转写设置
            self.config.config["transcription_settings"]["provider"] = self.provider.currentText()
            self.config.config["transcription_settings"]["post_process"] = self.post_process.isChecked()
            self.config.config["transcription_settings"]["post_process_provider"] = self.post_provider.currentText()
            self.config.config["transcription_settings"]["post_process_prompt"] = self.post_prompt.text()
            
            # 保存文本清理设置
            self.config.config["transcription_settings"]["remove_punctuation"] = self.remove_punctuation.isChecked()
            self.config.config["transcription_settings"]["punctuation_to_remove"] = self.punctuation_to_remove.text()
            self.config.config["transcription_settings"]["remove_emoji"] = self.remove_emoji.isChecked()
            
            # 保存录音设置
            try:
                trigger_press_time = float(self.trigger_press_time.text())
                min_press_time = float(self.min_press_time.text())
                max_record_time = float(self.max_record_time.text())
                
                if trigger_press_time < 0.05 or trigger_press_time > 0.5:
                    QMessageBox.warning(self, "警告", "录音触发时间应在0.05-0.5秒之间")
                    return
                    
                if min_press_time <= trigger_press_time:
                    QMessageBox.warning(self, "警告", "最小按压时间必须大于录音触发时间")
                    return
                
                if min_press_time < 0.1 or min_press_time > 5.0:
                    QMessageBox.warning(self, "警告", "最小按压时间应在0.1-5.0秒之间")
                    return
                    
                if max_record_time < 1.0 or max_record_time > 300.0:
                    QMessageBox.warning(self, "警告", "最大录音时间应在1-300秒之间")
                    return
                    
                self.config.config["audio_settings"]["trigger_press_time"] = trigger_press_time
                self.config.config["audio_settings"]["min_press_time"] = min_press_time
                self.config.config["audio_settings"]["max_record_time"] = max_record_time
                
            except ValueError:
                QMessageBox.warning(self, "警告", "请输入有效的数字")
                return
            
            # 保存波形窗口位置设置
            selected_pos = self.wave_position.currentData()
            self.config.config["transcription_settings"]["wave_window_position"] = selected_pos
            
            # 保存文本插入设置
            self.config.config["general_settings"]["insert_method"] = self.insert_method.currentText()
            
            # 保存日志设置
            self.config.config["general_settings"]["enable_logging"] = self.enable_logging.isChecked()
            
            self.config.save_config()
            
            # 发送设置更新信号（修改这部分）
            if hasattr(self.parent(), 'config_updated'):
                self.parent().config_updated()
                
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置时发生错误：{str(e)}")



















