import os
import subprocess
import json
import shutil
from build_common import clean_dirs, get_pyinstaller_base_args

def create_portable():
    """创建便携版"""
    print("正在创建便携版...")
    
    args = get_pyinstaller_base_args()
    # 移除 --add-data=qt.conf;. 参数
    args.extend(['--distpath=portable', 'main.py'])
    
    subprocess.run(args, check=True)
    
    # 创建默认配置文件
    default_config = {
        # ... 你的默认配置内容 ...
    }
    
    # 创建配置文件模板
    os.makedirs('portable/VoiceInk', exist_ok=True)
    with open('portable/VoiceInk/config.template.json', 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=4, ensure_ascii=False)
    
    # 创建启动脚本和说明文件
    with open('portable/VoiceInk/启动VoiceInk.bat', 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('cd /d "%~dp0"\n')
        f.write('start VoiceInk.exe\n')
    
    with open('portable/VoiceInk/说明.txt', 'w', encoding='utf-8') as f:
        f.write('VoiceInk - 智能语音输入助手\n\n')
        # ... 其他说明文件内容 ...
    
    # 打包为zip
    shutil.make_archive('VoiceInk_便携版', 'zip', 'portable/VoiceInk')
    print("便携版创建完成：VoiceInk_便携版.zip")

if __name__ == "__main__":
    if not os.environ.get('VIRTUAL_ENV'):
        print("警告：建议在虚拟环境中运行打包脚本")
        input("按Enter继续，或Ctrl+C退出...")
    
    clean_dirs()
    create_portable()
