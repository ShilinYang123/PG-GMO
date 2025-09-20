#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复PMC状态查看器的编码问题
将emoji字符替换为Windows命令行兼容的文本
"""

import re
from pathlib import Path

def fix_pmc_status_viewer():
    """修复pmc_status_viewer.py的编码问题"""
    file_path = Path("s:/PG-PMC/tools/pmc_status_viewer.py")
    
    # emoji替换映射
    emoji_replacements = {
        '🏭': '[工厂]',
        '📋': '[清单]',
        '🖥️': '[系统]',
        '🔄': '[运行]',
        '⏰': '[时间]',
        '📦': '[版本]',
        '🔧': '[模块]',
        '📊': '[数据]',
        '✅': '[正常]',
        '🚨': '[预警]',
        '📏': '[规则]',
        '⏳': '[待处理]',
        '📈': '[仪表板]',
        '👁️': '[监控]',
        '🌅': '[启动]',
        '🔍': '[检查]',
        '🎯': '[重点]',
        '🔥': '[紧急]',
        '📅': '[日常]',
        '💊': '[健康]',
        '🏥': '[整体]',
        '💻': '[CPU]',
        '🧠': '[内存]',
        '💾': '[磁盘]',
        '🌐': '[网络]',
        '❌': '[异常]',
        '⚠️': '[注意]',
        '📁': '[文件]',
        '📍': '[位置]',
        '😴': '[休眠]',
        '🟢': '[在线]',
        '🔴': '[离线]',
        '📡': '[数据源]',
        '👥': '[团队]',
        '👤': '[成员]',
        '🚀': '[启动]',
        '🎉': '[完成]',
        '📖': '[手册]',
        '📚': '[文档]',
        '🔗': '[链接]',
        '💡': '[提示]',
        '🛠️': '[工具]',
        '⚙️': '[设置]',
        '🔒': '[安全]',
        '🔓': '[开放]',
        '📝': '[记录]',
        '📄': '[文档]',
        '📊': '[图表]',
        '📈': '[趋势]',
        '📉': '[下降]',
        '🔔': '[通知]',
        '🔕': '[静音]',
        '⭐': '[重要]',
        '🌟': '[亮点]',
        '💯': '[完美]',
        '🎊': '[庆祝]'
    }
    
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换emoji
        for emoji, replacement in emoji_replacements.items():
            content = content.replace(emoji, replacement)
        
        # 使用正则表达式替换所有剩余的emoji字符
        # 匹配Unicode emoji范围
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F]|'  # 表情符号
            r'[\U0001F300-\U0001F5FF]|'  # 符号和象形文字
            r'[\U0001F680-\U0001F6FF]|'  # 交通和地图符号
            r'[\U0001F1E0-\U0001F1FF]|'  # 国旗
            r'[\U00002600-\U000026FF]|'  # 杂项符号
            r'[\U00002700-\U000027BF]|'  # 装饰符号
            r'[\U0001F900-\U0001F9FF]|'  # 补充符号和象形文字
            r'[\U0001FA70-\U0001FAFF]'   # 扩展A符号和象形文字
        )
        
        def replace_emoji(match):
            return '[符号]'
        
        content = emoji_pattern.sub(replace_emoji, content)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ pmc_status_viewer.py 编码问题已修复")
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 开始修复PMC状态查看器编码问题...")
    
    if fix_pmc_status_viewer():
        print("🎉 编码问题修复完成！")
        print("📋 现在可以正常使用PMC控制面板了")
        return 0
    else:
        print("❌ 修复失败")
        return 1

if __name__ == "__main__":
    exit(main())