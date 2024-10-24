from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import (Qt, QTimer, QPropertyAnimation, QEasingCurve, 
                         pyqtProperty, QRectF)  # 从 QtCore 导入 QRectF
from PyQt6.QtGui import QPainter, QColor, QLinearGradient
import numpy as np

class WaveVisualizerWindow(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.dragging = False
        self.drag_position = None
        
        # 初始化动画相关的属性
        self._ripple_size = 0
        self._ripple_opacity = 0.0
        self.size_anim = None
        self.opacity_anim = None
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |  # 无边框
            Qt.WindowType.WindowStaysOnTopHint | # 置顶
            Qt.WindowType.Tool  # 不在任务栏显示
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明背景
        
        # 波形数据
        self.wave_data = np.zeros(50)
        self.max_amplitude = 0.1
        
        # 设置窗口位置
        self.update_position()
        
        # 更新定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(50)  # 20fps
        
        # 样式设置
        self.bar_color = QColor(52, 152, 219)  # 基础蓝色
        self.background_color = QColor(255, 255, 255, 230)  # 浅色半透明背景
        self.ripple_color = QColor(52, 152, 219, 100)  # 涟漪颜色
        
    # 使用 pyqtProperty 定义属性
    @pyqtProperty(float)
    def ripple_size(self):
        return self._ripple_size
    
    @ripple_size.setter
    def ripple_size(self, value):
        self._ripple_size = value
        self.update()
    
    @pyqtProperty(float)
    def ripple_opacity(self):
        return self._ripple_opacity
    
    @ripple_opacity.setter
    def ripple_opacity(self, value):
        self._ripple_opacity = value
        self.update()
        
    def reset_wave_data(self):
        """重置波形数据"""
        self.wave_data = np.zeros(50)
        self.max_amplitude = 0.1
        self.update()  # 立即更新显示
        
    def showEvent(self, event):
        """窗口显示时播放涟漪动画"""
        super().showEvent(event)
        self.reset_wave_data()
        QTimer.singleShot(100, self.play_ripple_animation)  # 延迟一小段时间再播放动画
        
    def play_ripple_animation(self):
        """播放涟漪动画"""
        if not self.isVisible():
            return
            
        # 停止现有动画
        if self.size_anim and self.size_anim.state() == QPropertyAnimation.State.Running:
            self.size_anim.stop()
        if self.opacity_anim and self.opacity_anim.state() == QPropertyAnimation.State.Running:
            self.opacity_anim.stop()
        
        # 重置动画状态
        self._ripple_opacity = 1.0
        self._ripple_size = 0
        
        # 创建大小动画
        self.size_anim = QPropertyAnimation(self, b"ripple_size")
        self.size_anim.setStartValue(0.0)
        self.size_anim.setEndValue(float(max(self.width(), self.height())))
        self.size_anim.setDuration(1000)  # 1秒
        self.size_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # 创建透明度动画
        self.opacity_anim = QPropertyAnimation(self, b"ripple_opacity")
        self.opacity_anim.setStartValue(1.0)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.setDuration(1000)  # 1秒
        self.opacity_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # 启动动画
        self.size_anim.start()
        self.opacity_anim.start()
    
    def update_wave_data(self, data):
        """更新波形数据"""
        if len(data) > 0:
            # 计算音频块的RMS值
            rms = np.sqrt(np.mean(np.square(data)))
            # 更新最大振幅（添加衰减以使显示更动态）
            self.max_amplitude = max(rms, self.max_amplitude * 0.95)
            # 归一化并添加到波形数据
            normalized = rms / (self.max_amplitude if self.max_amplitude > 0.1 else 0.1)
            normalized = min(normalized, 1.0)  # 限制最大值
            self.wave_data = np.roll(self.wave_data, -1)
            self.wave_data[-1] = normalized
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_y = height / 2
        
        # 绘制背景
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.background_color)
        painter.drawRoundedRect(self.rect(), 10, 10)
        
        # 绘制涟漪效果
        if self._ripple_opacity > 0:
            ripple_color = QColor(self.ripple_color)
            ripple_color.setAlpha(int(255 * self._ripple_opacity))
            painter.setBrush(ripple_color)
            
            # 使用 QRectF 绘制椭圆
            center_x = width / 2
            center_y = height / 2
            radius = self._ripple_size / 2
            rect = QRectF(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2
            )
            painter.drawEllipse(rect)
        
        # 绘制波形
        bar_width = int(width / (len(self.wave_data) * 1.5))
        spacing = int(width / len(self.wave_data))
        
        for i, value in enumerate(self.wave_data):
            bar_height = int(value * (height * 0.8))
            
            bar_gradient = QLinearGradient(0, center_y - bar_height/2, 0, center_y + bar_height/2)
            alpha = int(180 + value * 75)
            
            bar_gradient.setColorAt(0, QColor(100, 181, 246, alpha))
            bar_gradient.setColorAt(0.5, QColor(30, 136, 229, alpha))
            bar_gradient.setColorAt(1, QColor(100, 181, 246, alpha))
            
            x = i * spacing
            y = int(center_y - bar_height/2)
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(bar_gradient)
            painter.drawRoundedRect(
                x, y, 
                bar_width, bar_height,
                2, 2
            )
    
    def update_position(self):
        """根据配置更新窗口位置"""
        screen = QApplication.primaryScreen().geometry()
        width = 300
        height = 100
        position = self.config.config["transcription_settings"]["wave_window_position"]
        
        if position == "custom":
            custom_pos = self.config.config["transcription_settings"]["wave_window_custom_pos"]
            x = custom_pos["x"]
            y = custom_pos["y"]
        else:
            # 根据预设位置计算坐标
            if position == "left-top":
                x = 20
                y = 20
            elif position == "right-top":
                x = screen.width() - width - 20
                y = 20
            elif position == "left-bottom":
                x = 20
                y = screen.height() - height - 20
            elif position == "right-bottom":
                x = screen.width() - width - 20
                y = screen.height() - height - 20
            elif position == "right-middle":
                x = screen.width() - width - 20
                y = screen.height() // 2 - height // 2
                
        self.setGeometry(x, y, width, height)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.dragging:
            self.dragging = False
            # 保存新位置
            pos = self.pos()
            self.config.config["transcription_settings"]["wave_window_position"] = "custom"
            self.config.config["transcription_settings"]["wave_window_custom_pos"] = {
                "x": pos.x(),
                "y": pos.y()
            }
            self.config.save_config()
