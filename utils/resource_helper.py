import os
import sys
import logging

def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    
    full_path = os.path.join(base_path, relative_path)
    if not os.path.exists(full_path):
        logging.warning(f"资源文件未找到: {full_path}")
    return full_path

def check_resources():
    """检查必要的资源文件是否存在"""
    required_resources = [
        "resources/app.ico",
        "resources/style.qss",
        "resources/icons/16x16/app.png",
        "resources/icons/24x24/app.png",
        "resources/icons/32x32/app.png",
        "resources/icons/48x48/app.png",
        "resources/icons/256x256/app.png"
    ]
    
    missing_resources = []
    for resource in required_resources:
        if not os.path.exists(get_resource_path(resource)):
            missing_resources.append(resource)
    
    if missing_resources:
        raise FileNotFoundError(
            f"缺少以下资源文件:\n" + "\n".join(missing_resources)
        )
