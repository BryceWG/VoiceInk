import os
import subprocess
from build_common import clean_dirs, get_pyinstaller_base_args

def create_single_exe():
    """创建单文件版本"""
    print("正在创建单文件版本...")
    
    args = get_pyinstaller_base_args()
    args.extend(['--onefile', 'main.py'])
    
    subprocess.run(args, check=True)
    print("单文件版本创建完成：dist/VoiceInk.exe")

if __name__ == "__main__":
    if not os.environ.get('VIRTUAL_ENV'):
        print("警告：建议在虚拟环境中运行打包脚本")
        input("按Enter继续，或Ctrl+C退出...")
    
    clean_dirs()
    create_single_exe()
