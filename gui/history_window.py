from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QScrollArea, QFrame)
from PyQt6.QtCore import Qt
import pyperclip

class HistoryCard(QFrame):
    def __init__(self, text, time):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            HistoryCard {
                background-color: white;
                border-radius: 8px;
                margin: 5px;
                padding: 15px;
            }
            QLabel {
                font-size: 13pt;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        layout = QVBoxLayout()  # 改为垂直布局
        layout.setSpacing(8)
        
        # 文本内容
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("font-size: 13pt;")  # 增大字体
        layout.addWidget(text_label)
        
        # 底部信息栏
        bottom_container = QWidget()
        bottom_layout = QHBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 8, 0, 0)
        
        time_label = QLabel(time)
        time_label.setStyleSheet("color: #666; font-size: 11pt;")  # 调整时间字体
        bottom_layout.addWidget(time_label)
        
        bottom_layout.addStretch()
        
        copy_btn = QPushButton("复制")
        copy_btn.setFixedWidth(70)  # 稍微加宽按钮
        copy_btn.clicked.connect(lambda: pyperclip.copy(text))
        bottom_layout.addWidget(copy_btn)
        
        layout.addWidget(bottom_container)
        self.setLayout(layout)

class HistoryWindow(QMainWindow):
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("历史记录")
        self.setMinimumSize(500, 600)  # 改为竖直的长条形
        self.resize(600, 800)  # 设置默认尺寸
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)
        
        # 按日期分组显示历史记录
        for date in sorted(self.config.history.keys(), reverse=True):
            date_container = QWidget()
            date_layout = QVBoxLayout(date_container)
            date_layout.setContentsMargins(10, 5, 10, 5)
            
            # 日期标签
            date_label = QLabel(date)
            date_label.setStyleSheet("""
                QLabel {
                    font-size: 15pt;  /* 增大日期字体 */
                    font-weight: bold;
                    color: #2c3e50;
                    padding: 8px;
                    background-color: #ecf0f1;
                    border-radius: 4px;
                }
            """)
            date_layout.addWidget(date_label)
            
            # 当天的记录卡片
            daily_records = self.config.history[date]
            for record in reversed(daily_records):
                card = HistoryCard(record["text"], record["time"])
                date_layout.addWidget(card)
            
            scroll_layout.addWidget(date_container)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
