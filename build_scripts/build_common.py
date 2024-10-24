import os
import shutil
import certifi

def clean_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', 'portable']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def get_pyinstaller_base_args():
    """获取PyInstaller的基础参数"""
    return [
        'pyinstaller',
        '--noconfirm',
        '--noconsole',
        '--name=VoiceInk',
        '--icon=resources/app.ico',
        # 添加证书文件
        f'--add-data={certifi.where()};certifi',
        # 移除 --add-data=qt.conf;. 参数
        '--add-data=resources/app.ico;resources/',
        '--add-data=resources/style.qss;resources/',
        '--add-data=resources/icons/16x16/app.png;resources/icons/16x16/',
        '--add-data=resources/icons/24x24/app.png;resources/icons/24x24/',
        '--add-data=resources/icons/32x32/app.png;resources/icons/32x32/',
        '--add-data=resources/icons/48x48/app.png;resources/icons/48x48/',
        '--add-data=resources/icons/256x256/app.png;resources/icons/256x256/',
        '--add-data=resources;resources',
        # PyQt6 相关配置
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.sip',
        '--collect-submodules=PyQt6',
        '--collect-data=PyQt6',
        # 添加系统托盘相关的依赖
        '--hidden-import=PyQt6.QtWidgets.QSystemTrayIcon',
        '--hidden-import=PyQt6.QtWidgets.QMenu',
        '--hidden-import=PyQt6.QtGui.QIcon',
        # 其他必要的依赖
        '--hidden-import=pynput.keyboard._win32',
        '--hidden-import=sounddevice',
        '--hidden-import=numpy',
        '--hidden-import=openai',
        '--hidden-import=requests',
        '--hidden-import=pyperclip',
        '--hidden-import=pyautogui',
        '--hidden-import=win32com.client',
        '--hidden-import=emoji',
        '--hidden-import=google.generativeai',
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=pandas',
        '--exclude-module=PIL',
        '--exclude-module=cv2',
        '--hidden-import=PyQt6.QtGui.QFontDatabase',
        '--hidden-import=PyQt6.QtGui.QFont',
        '--hidden-import=certifi'
    ]
