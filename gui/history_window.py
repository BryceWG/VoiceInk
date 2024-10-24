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
        
        # 文本容
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
        self.setMinimumSize(500, 600)
        self.resize(600, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(10)
        
        # 创建滚动区域容器
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll)
        
        # 初始加载历史记录
        self.refresh_history()
    
    def refresh_history(self):
        """刷新历史记录显示"""
        # 创建新的内容widget
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)
        
        try:
            if not hasattr(self.config, 'history') or not self.config.history:
                empty_label = QLabel("暂无历史记录")
                empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                scroll_layout.addWidget(empty_label)
            else:
                # 按日期分组显示历史记录
                for date in sorted(self.config.history.keys(), reverse=True):
                    date_container = QWidget()
                    date_layout = QVBoxLayout(date_container)
                    date_layout.setContentsMargins(10, 5, 10, 5)
                    
                    # 日期标签
                    date_label = QLabel(date)
                    date_label.setStyleSheet("""
                        QLabel {
                            font-size: 15pt;
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
            
            # 设置新的内容widget
            self.scroll.setWidget(scroll_content)
            
        except Exception as e:
            print(f"显示历史记录时出错: {str(e)}")
    
    def showEvent(self, event):
        """窗口显示时自动刷新"""
        super().showEvent(event)
        self.refresh_history()
