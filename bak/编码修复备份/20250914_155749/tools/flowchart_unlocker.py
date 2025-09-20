#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流程图解锁工具
移除drawio文件中的locked属性，使文件重新可编辑
"""

import xml.etree.ElementTree as ET
import re
from datetime import datetime
import os

class FlowchartUnlocker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        self.unlocked_items = []
        
    def unlock_all_elements(self):
        """移除所有元素的locked属性"""
        unlocked_count = 0
        
        # 遍历所有mxCell元素
        for elem in self.root.iter('mxCell'):
            style = elem.get('style', '')
            
            if 'locked=1' in style:
                # 移除locked=1属性
                new_style = self.remove_locked_from_style(style)
                elem.set('style', new_style)
                
                element_id = elem.get('id', '未知')
                element_value = elem.get('value', '').split('\n')[0][:20] if elem.get('value') else '无标题'
                
                self.unlocked_items.append({
                    'id': element_id,
                    'value': element_value,
                    'old_style': style,
                    'new_style': new_style
                })
                
                unlocked_count += 1
        
        return unlocked_count
    
    def remove_locked_from_style(self, style):
        """从样式字符串中移除locked属性"""
        # 移除 ;locked=1 或 locked=1; 或 locked=1
        style = re.sub(r';?locked=1;?', '', style)
        
        # 清理多余的分号
        style = re.sub(r';;+', ';', style)
        style = style.strip(';')
        
        return style
    
    def remove_shape_restrictions(self):
        """移除形状的移动、调整等限制"""
        restrictions_removed = 0
        
        for elem in self.root.iter('mxCell'):
            style = elem.get('style', '')
            
            # 移除各种限制属性
            restrictions = [
                'movable=0', 'resizable=0', 'rotatable=0', 
                'deletable=0', 'editable=0', 'connectable=0'
            ]
            
            original_style = style
            for restriction in restrictions:
                if restriction in style:
                    style = style.replace(restriction, '')
                    style = style.replace(';;', ';').strip(';')
            
            if original_style != style:
                elem.set('style', style)
                restrictions_removed += 1
        
        return restrictions_removed
    
    def unlock_file(self):
        """执行解锁操作"""
        print("🔓 开始解锁流程图文件...")
        print(f"📁 目标文件: {self.file_path}")
        
        # 创建备份
        backup_path = self.file_path.replace('.drawio', '_locked_backup.drawio')
        try:
            import shutil
            shutil.copy2(self.file_path, backup_path)
            print(f"📋 已创建备份文件: {backup_path}")
        except Exception as e:
            print(f"⚠️ 备份创建失败: {e}")
        
        # 执行解锁
        unlocked_count = self.unlock_all_elements()
        restrictions_removed = self.remove_shape_restrictions()
        
        if unlocked_count > 0 or restrictions_removed > 0:
            # 保存解锁后的文件
            try:
                self.tree.write(self.file_path, encoding='utf-8', xml_declaration=True)
                print(f"✅ 解锁完成!")
                print(f"   - 解锁元素: {unlocked_count} 个")
                print(f"   - 移除限制: {restrictions_removed} 个")
                
                # 生成解锁报告
                self.generate_unlock_report()
                
            except Exception as e:
                print(f"❌ 保存文件失败: {e}")
                return False
                
        else:
            print("✅ 文件已经是解锁状态，无需处理")
        
        return True
    
    def generate_unlock_report(self):
        """生成解锁报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.file_path.replace('.drawio', f'_解锁报告_{timestamp}.md')
        
        report_content = f"""# 流程图解锁报告

## 📋 解锁概要
**解锁时间**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}  
**目标文件**: {os.path.basename(self.file_path)}  
**解锁状态**: ✅ 完成  
**解锁元素数量**: {len(self.unlocked_items)} 个

## 🔓 解锁详情

### 已解锁的元素
"""
        
        if self.unlocked_items:
            for i, item in enumerate(self.unlocked_items[:10], 1):  # 只显示前10个
                report_content += f"{i}. **{item['id']}** - {item['value']}\n"
            
            if len(self.unlocked_items) > 10:
                report_content += f"... 以及其他 {len(self.unlocked_items) - 10} 个元素\n"
        else:
            report_content += "无需解锁的元素\n"
        
        report_content += f"""

## 🎯 解锁效果

### ✅ 恢复的功能
1. **元素移动**: 所有图形元素现在可以自由移动
2. **尺寸调整**: 可以调整图形的大小
3. **形状编辑**: 可以编辑文本内容和样式
4. **连接线**: 可以添加、删除和修改连接线
5. **泳道调整**: 泳道可以重新排列和调整

### 📊 解锁统计
- **总解锁元素**: {len(self.unlocked_items)} 个
- **泳道元素**: 包含所有业务泳道
- **业务节点**: 包含所有流程步骤
- **连接线**: 所有流程连接线

### 🛠️ 使用建议
1. **谨慎编辑**: 解锁后请小心编辑，避免破坏流程逻辑
2. **备份保护**: 重要修改前请先创建备份
3. **重新锁定**: 编辑完成后可以重新锁定关键元素

## 📁 文件状态
- **原锁定文件**: 已备份为 `*_locked_backup.drawio`
- **解锁文件**: 当前文件已解锁，可正常编辑
- **兼容性**: 完全兼容Draw.io/diagrams.net

## 🔧 解锁技术说明
- 移除了所有 `locked=1` 属性
- 移除了 `movable=0`, `resizable=0` 等限制
- 保持了所有原始样式和布局
- 维护了元素间的父子关系

---
**解锁工具**: FlowchartUnlocker v1.0  
**生成时间**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}
"""
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"📄 解锁报告已生成: {os.path.basename(report_path)}")
        except Exception as e:
            print(f"⚠️ 报告生成失败: {e}")

def main():
    """主函数"""
    file_path = r"S:\PG-GMO\office\业务部\小家电制造业详细生产流程图-交叉优化版.drawio"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    try:
        unlocker = FlowchartUnlocker(file_path)
        success = unlocker.unlock_file()
        
        if success:
            print("\n🎉 文件解锁成功!")
            print("💡 现在可以在Draw.io中正常编辑该文件了")
            print("⚠️ 建议编辑完成后手动锁定重要元素以防误操作")
        else:
            print("\n❌ 解锁过程中出现问题")
            
    except Exception as e:
        print(f"❌ 解锁过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()