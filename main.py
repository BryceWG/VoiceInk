import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow
from core.keyboard_listener import KeyboardListener
from core.config_manager import ConfigManager
from core.logger import Logger
import os
import certifi
from utils.resource_helper import get_resource_path, check_resources

# 设置证书路径
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# DPI设置需要在创建QApplication之前完成
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"

def main():
    try:
        # 检查资源文件
        check_resources()
        
        config = ConfigManager()
        logger = Logger(config)
        
        try:
            # 创建应用实例
            app = QApplication(sys.argv)
            # 使用新的DPI缩放设置方法
            QApplication.setHighDpiScaleFactorRoundingPolicy(
                Qt.HighDpiScaleFactorRoundingPolicy.Floor)
            
            # 修改图标加载方式
            icon_path = get_resource_path(os.path.join("resources", "app.ico"))
            if os.path.exists(icon_path):
                app_icon = QIcon(icon_path)
                app.setWindowIcon(app_icon)
                # 设置任务栏图标
                try:
                    import ctypes
                    myappid = 'VoiceInk'
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                except:
                    pass
            else:
                logger.warning(f"图标文件未找到: {icon_path}")
            
            # 在创建QApplication之后,设置全局字体
            font = app.font()
            font.setPointSize(11)  # 将默认字体从9调整到11
            app.setFont(font)
            
            window = MainWindow(config)
            keyboard_listener = KeyboardListener(window)
            
            window.show()
            ret = app.exec()
            # 在退出前确保清理资源
            window = None
            keyboard_listener = None
            app = None
            sys.exit(ret)
        except Exception as e:
            logger.error(f"程序发生致命错误: {str(e)}")
            raise
    except FileNotFoundError as e:
        print(f"错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"程序发生致命错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
