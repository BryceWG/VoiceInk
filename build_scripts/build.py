import os
import shutil
import subprocess
import json
from build_common import clean_dirs, get_pyinstaller_base_args, get_output_filename

def create_portable():
    """创建便携版"""
    print("正在创建便携版...")
    
    args = get_pyinstaller_base_args()
    args.extend(['--distpath=portable', 'main.py'])
    subprocess.run(args, check=True)
    
    # 创建默认配置文件
    default_config = {
        "general_settings": {
            "insert_method": "clipboard",
            "keyboard_interval": 0.01,
            "enable_logging": False
        },
        "api_settings": {
            "transcription": {
                "openai": {
                    "api_key": "",
                    "api_url": "https://api.openai.com/v1",
                    "model": "whisper-1"
                },
                "groq": {
                    "api_key": "",
                    "api_url": "https://api.groq.com/openai/v1",
                    "model": "whisper-large-v3"
                },
                "custom": {
                    "api_key": "",
                    "api_url": "https://api.siliconflow.cn/v1/audio/transcriptions",
                    "model": "FunAudioLLM/SenseVoiceSmall"
                }
            },
            "post_process": {
                "openai": {
                    "api_key": "",
                    "api_url": "https://api.openai.com/v1",
                    "model": "gpt-4o-mini"
                },
                "groq": {
                    "model": "mixtral-8x7b-32768"
                }
            }
        },
        "transcription_settings": {
            "provider": "openai",
            "post_process": False,
            "post_process_provider": "openai",
            "post_process_prompt": "更正文本中错误，保持原意",
            "wave_window_position": "right-middle",
            "wave_window_custom_pos": {"x": 0, "y": 0},
            "remove_punctuation": True,
            "punctuation_to_remove": "。，,.?？！!",
            "remove_emoji": True
        },
        "audio_settings": {
            "sample_rate": 44100,
            "channels": 1,
            "trigger_press_time": 0.2,
            "min_press_time": 0.5,
            "max_record_time": 60.0
        },
        "history_settings": {
            "max_days": 30,
            "enabled": True
        }
    }
    
    # 创建配置文件模板
    os.makedirs('portable/VoiceInk', exist_ok=True)
    with open('portable/VoiceInk/config.template.json', 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=4, ensure_ascii=False)
    
    # 创建启动脚本
    with open('portable/VoiceInk/启动VoiceInk.bat', 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('cd /d "%~dp0"\n')  # 切换到脚本所在目录
        f.write('start VoiceInk.exe\n')
    
    # 创建说明文件
    with open('portable/VoiceInk/说明.txt', 'w', encoding='utf-8') as f:
        f.write('VoiceInk - 智能语音输入助手\n\n')
        f.write('使用说明：\n')
        f.write('1. 双击"启动VoiceInk.bat"运行程序\n')
        f.write('2. 按住Ctrl键开始录音\n')
        f.write('3. 松开Ctrl键结束录音并转写\n')
        f.write('4. 转写文本将自动插入到当前焦点位置\n\n')
        f.write('注意事项：\n')
        f.write('- 首次运行请在设置中配置API密钥\n')
        f.write('- 所有配置和历史记录都保存在程序目录下\n')
        f.write('- 如需迁移程序，复制整个文件夹即可\n')
    
    # 使用版本号命名
    output_name = get_output_filename(is_portable=True)
    shutil.make_archive(output_name, 'zip', 'portable/VoiceInk')
    print(f"便携版创建完成：{output_name}.zip")

def create_single_exe():
    """创建单文件版本"""
    print("正在创建单文件版本...")
    
    args = get_pyinstaller_base_args()
    args.extend(['--onefile', 'main.py'])
    subprocess.run(args, check=True)
    
    # 重命名输出文件以包含版本号
    output_name = get_output_filename(is_portable=False)
    os.rename('dist/VoiceInk.exe', f'dist/{output_name}.exe')
    print(f"单文件版本创建完成：dist/{output_name}.exe")

def main():
    # 检查是否在虚拟环境中
    if not os.environ.get('VIRTUAL_ENV'):
        print("警告：建议在虚拟环境中运行打包脚本")
        input("按Enter继续，或Ctrl+C退出...")
    
    # 清理旧的构建文件
    clean_dirs()
    
    # 创建便携版
    create_portable()
    
    # 创建单文件版本
    create_single_exe()
    
    print("\n打包完成！")
    print("- 便携版: VoiceInk_便携版.zip")
    print("- 单文件版: dist/VoiceInk.exe")

if __name__ == "__main__":
    main()
