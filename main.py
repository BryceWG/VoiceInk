import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow
from core.keyboard_listener import KeyboardListener
from core.config_manager import ConfigManager
from core.logger import Logger
import os
from utils.resource_helper import get_resource_path, check_resources

def main():
    try:
        # 检查资源文件
        check_resources()
        
        config = ConfigManager()
        logger = Logger(config)
        
        try:
            # 创建应用实例
            app = QApplication(sys.argv)
            
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
            
            window = MainWindow(config)
            keyboard_listener = KeyboardListener(window)
            
            window.show()
            sys.exit(app.exec())
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
