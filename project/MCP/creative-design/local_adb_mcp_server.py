#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地ADB MCP服务器
提供Android设备控制和自动化功能接口
"""

import json
import logging
import subprocess
import time
from pathlib import Path
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalADBMCPServer:
    def __init__(self):
        self.server_name = "Local ADB MCP Server"
        self.version = "1.0.0"
        self.base_dir = Path(__file__).parent
        self.screenshots_dir = self.base_dir / "adb-screenshots"
        self.logs_dir = self.base_dir / "adb-logs"
        self.scripts_dir = self.base_dir / "adb-scripts"
        
        # 创建必要目录
        self.screenshots_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.scripts_dir.mkdir(exist_ok=True)
        
        # ADB可执行文件路径
        self.adb_path = self._find_adb_path()
        
        logger.info(f"启动 {self.server_name} v{self.version}")
        if self.adb_path:
            logger.info(f"ADB路径: {self.adb_path}")
        else:
            logger.warning("未找到ADB安装路径，请安装Android SDK Platform Tools")
    
    def _find_adb_path(self):
        """查找ADB安装路径"""
        possible_paths = [
            "adb",  # 如果在PATH中
            "C:\\Android\\Sdk\\platform-tools\\adb.exe",
            "C:\\Users\\%USERNAME%\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe",
            "D:\\Android\\Sdk\\platform-tools\\adb.exe"
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run(
                    [path, "version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        return None
    
    def list_available_functions(self):
        """列出可用功能"""
        functions = [
            "list_devices - 列出连接的设备",
            "device_info - 获取设备信息",
            "take_screenshot - 截取屏幕",
            "tap_screen - 点击屏幕",
            "swipe_screen - 滑动屏幕",
            "input_text - 输入文本",
            "press_key - 按键操作",
            "install_app - 安装应用",
            "uninstall_app - 卸载应用",
            "list_apps - 列出已安装应用",
            "start_app - 启动应用",
            "stop_app - 停止应用",
            "get_logs - 获取系统日志",
            "push_file - 推送文件到设备",
            "pull_file - 从设备拉取文件"
        ]
        
        logger.info("支持的功能:")
        for func in functions:
            logger.info(f"  - {func}")
        
        return functions
    
    def execute_adb_command(self, command, device_id=None):
        """执行ADB命令"""
        if not self.adb_path:
            return "错误: 未找到ADB安装路径"
        
        try:
            cmd = [self.adb_path]
            if device_id:
                cmd.extend(["-s", device_id])
            cmd.extend(command.split())
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"错误: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return "错误: 命令执行超时"
        except Exception as e:
            return f"错误: {str(e)}"
    
    def list_devices(self):
        """列出连接的设备"""
        result = self.execute_adb_command("devices")
        if "错误" in result:
            return result
        
        devices = []
        lines = result.split('\n')[1:]  # 跳过标题行
        for line in lines:
            if line.strip() and '\t' in line:
                device_id, status = line.strip().split('\t')
                devices.append({"id": device_id, "status": status})
        
        logger.info(f"找到 {len(devices)} 个设备")
        return devices
    
    def device_info(self, device_id=None):
        """获取设备信息"""
        info = {}
        
        # 获取设备型号
        model = self.execute_adb_command("shell getprop ro.product.model", device_id)
        info["model"] = model
        
        # 获取Android版本
        version = self.execute_adb_command("shell getprop ro.build.version.release", device_id)
        info["android_version"] = version
        
        # 获取屏幕分辨率
        resolution = self.execute_adb_command("shell wm size", device_id)
        info["resolution"] = resolution
        
        # 获取电池信息
        battery = self.execute_adb_command("shell dumpsys battery | grep level", device_id)
        info["battery"] = battery
        
        logger.info(f"设备信息: {info}")
        return info
    
    def take_screenshot(self, device_id=None, filename=None):
        """截取屏幕"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_path = self.screenshots_dir / filename
        
        # 在设备上截图
        result = self.execute_adb_command("shell screencap -p /sdcard/screenshot.png", device_id)
        if "错误" in result:
            return result
        
        # 拉取截图到本地
        result = self.execute_adb_command(f"pull /sdcard/screenshot.png {screenshot_path}", device_id)
        if "错误" in result:
            return result
        
        # 删除设备上的临时文件
        self.execute_adb_command("shell rm /sdcard/screenshot.png", device_id)
        
        logger.info(f"截图保存到: {screenshot_path}")
        return f"截图已保存: {screenshot_path}"
    
    def tap_screen(self, x, y, device_id=None):
        """点击屏幕"""
        result = self.execute_adb_command(f"shell input tap {x} {y}", device_id)
        logger.info(f"点击屏幕坐标: ({x}, {y})")
        return result if "错误" in result else f"已点击坐标 ({x}, {y})"
    
    def swipe_screen(self, x1, y1, x2, y2, duration=300, device_id=None):
        """滑动屏幕"""
        result = self.execute_adb_command(f"shell input swipe {x1} {y1} {x2} {y2} {duration}", device_id)
        logger.info(f"滑动屏幕: ({x1}, {y1}) -> ({x2}, {y2})")
        return result if "错误" in result else f"已滑动: ({x1}, {y1}) -> ({x2}, {y2})"
    
    def input_text(self, text, device_id=None):
        """输入文本"""
        # 转义特殊字符
        escaped_text = text.replace(' ', '%s').replace('&', '\\&')
        result = self.execute_adb_command(f"shell input text '{escaped_text}'", device_id)
        logger.info(f"输入文本: {text}")
        return result if "错误" in result else f"已输入文本: {text}"
    
    def press_key(self, keycode, device_id=None):
        """按键操作"""
        # 常用按键映射
        key_mapping = {
            "home": "KEYCODE_HOME",
            "back": "KEYCODE_BACK",
            "menu": "KEYCODE_MENU",
            "power": "KEYCODE_POWER",
            "volume_up": "KEYCODE_VOLUME_UP",
            "volume_down": "KEYCODE_VOLUME_DOWN",
            "enter": "KEYCODE_ENTER",
            "space": "KEYCODE_SPACE",
            "delete": "KEYCODE_DEL"
        }
        
        key = key_mapping.get(keycode.lower(), keycode)
        result = self.execute_adb_command(f"shell input keyevent {key}", device_id)
        logger.info(f"按键: {keycode}")
        return result if "错误" in result else f"已按键: {keycode}"
    
    def list_apps(self, device_id=None):
        """列出已安装应用"""
        result = self.execute_adb_command("shell pm list packages", device_id)
        if "错误" in result:
            return result
        
        apps = []
        for line in result.split('\n'):
            if line.startswith('package:'):
                package_name = line.replace('package:', '').strip()
                apps.append(package_name)
        
        logger.info(f"找到 {len(apps)} 个应用")
        return apps
    
    def start_app(self, package_name, device_id=None):
        """启动应用"""
        result = self.execute_adb_command(f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1", device_id)
        logger.info(f"启动应用: {package_name}")
        return result if "错误" in result else f"已启动应用: {package_name}"
    
    def install_app(self, apk_path, device_id=None):
        """安装应用"""
        result = self.execute_adb_command(f"install {apk_path}", device_id)
        logger.info(f"安装应用: {apk_path}")
        return result
    
    def create_automation_script(self, script_name, actions):
        """创建自动化脚本"""
        script_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化脚本: {script_name}
生成时间: {datetime.now().isoformat()}
"""

import time
from local_adb_mcp_server import LocalADBMCPServer

def main():
    server = LocalADBMCPServer()
    
    # 检查设备连接
    devices = server.list_devices()
    if not devices:
        print("未找到连接的设备")
        return
    
    device_id = devices[0]["id"] if len(devices) == 1 else None
    print(f"使用设备: {{device_id or '默认设备'}}")
    
    # 执行自动化操作
'''
        
        for i, action in enumerate(actions):
            script_content += f"    # 步骤 {i+1}: {action.get('description', '')}\n"
            
            if action["type"] == "tap":
                script_content += f"    server.tap_screen({action['x']}, {action['y']}, device_id)\n"
            elif action["type"] == "swipe":
                script_content += f"    server.swipe_screen({action['x1']}, {action['y1']}, {action['x2']}, {action['y2']}, device_id=device_id)\n"
            elif action["type"] == "input":
                script_content += f"    server.input_text('{action['text']}', device_id)\n"
            elif action["type"] == "key":
                script_content += f"    server.press_key('{action['key']}', device_id)\n"
            elif action["type"] == "wait":
                script_content += f"    time.sleep({action['seconds']})\n"
            elif action["type"] == "screenshot":
                script_content += f"    server.take_screenshot(device_id, '{action.get('filename', '')}')\n"
            
            script_content += "\n"
        
        script_content += '''    print("自动化脚本执行完成")

if __name__ == "__main__":
    main()
'''
        
        script_file = self.scripts_dir / f"{script_name}.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        logger.info(f"创建自动化脚本: {script_name}")
        return f"脚本已创建: {script_file}"
    
    def run_demo(self):
        """运行演示"""
        logger.info("=== ADB MCP服务器演示 ===")
        
        # 列出功能
        self.list_available_functions()
        
        # 检查设备连接
        devices = self.list_devices()
        if isinstance(devices, list) and devices:
            logger.info(f"连接的设备: {devices}")
            
            # 获取第一个设备的信息
            if len(devices) > 0 and isinstance(devices[0], dict) and devices[0]["status"] == "device":
                device_id = devices[0]["id"]
                info = self.device_info(device_id)
                logger.info(f"设备详细信息: {info}")
        else:
            logger.info(f"设备连接状态: {devices}")
        
        # 创建示例自动化脚本
        sample_actions = [
            {"type": "screenshot", "description": "截取初始屏幕", "filename": "initial.png"},
            {"type": "tap", "description": "点击屏幕中心", "x": 540, "y": 960},
            {"type": "wait", "description": "等待2秒", "seconds": 2},
            {"type": "swipe", "description": "向上滑动", "x1": 540, "y1": 1500, "x2": 540, "y2": 500},
            {"type": "key", "description": "按返回键", "key": "back"},
            {"type": "screenshot", "description": "截取最终屏幕", "filename": "final.png"}
        ]
        
        self.create_automation_script("示例自动化", sample_actions)
        
        logger.info("演示完成！")
        
        if not self.adb_path:
            logger.info("请安装Android SDK Platform Tools以使用完整功能")
            logger.info("下载地址: https://developer.android.com/studio/releases/platform-tools")

def main():
    """主函数"""
    server = LocalADBMCPServer()
    server.run_demo()

if __name__ == "__main__":
    main()