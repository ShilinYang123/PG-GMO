#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剩余专业规格快速生成器
为HQ-QP-16到HQ-QP-32生成专业规格
"""

def generate_remaining_specs():
    """生成剩余17个文档的专业规格"""
    
    remaining_specs = {
        'HQ-QP-16': {
            'name': '纠正和纠正措施控制程序',
            'steps': [
                {'text': '问题识别发现\\n不符合项记录', 'type': 'start', 'department': '各部门', 'forms': ['问题识别记录', '不符合项报告']},
                {'text': '问题分析评估\\n影响程度判定', 'type': 'process', 'department': '品质部', 'forms': ['问题分析报告', '影响评估']},
                {'text': '纠正措施制定\\n临时措施实施', 'type': 'process', 'department': '责任部门', 'forms': ['纠正措施计划', '临时措施记录']},
                {'text': '根本原因分析\\n系统性原因调查', 'type': 'process', 'department': '品质部', 'forms': ['根本原因分析', '系统调查报告']},
                {'text': '预防措施制定\\n系统改进方案', 'type': 'process', 'department': '品质部', 'forms': ['预防措施计划', '系统改进方案']},
                {'text': '措施实施执行\\n跨部门协调配合', 'type': 'process', 'department': '各部门', 'forms': ['实施执行记录', '协调配合记录']},
                {'text': '实施效果验证\\n改进成果评估', 'type': 'process', 'department': '品质部', 'forms': ['效果验证报告', '成果评估']},
                {'text': '是否有效改进？\\n目标达成评估', 'type': 'decision', 'department': '品质部', 'forms': ['有效性评估', '目标达成分析']},
                {'text': '经验教训总结\\n知识管理更新', 'type': 'process', 'department': '品质部', 'forms': ['经验教训总结', '知识库更新']},
                {'text': '纠正措施流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        },
        
        'HQ-QP-17': {
            'name': '顾客投诉处理控制程序', 
            'steps': [
                {'text': '投诉信息接收\\n客户问题登记', 'type': 'start', 'department': '业务部', 'forms': ['投诉登记表', '客户问题记录']},
                {'text': '投诉内容确认\\n问题严重程度评估', 'type': 'process', 'department': '业务部', 'forms': ['投诉确认书', '严重程度评估']},
                {'text': '紧急处理措施\\n客户关系维护', 'type': 'process', 'department': '业务部', 'forms': ['紧急处理记录', '客户沟通记录']},
                {'text': '问题原因调查\\n责任部门追溯', 'type': 'process', 'department': '品质部', 'forms': ['原因调查报告', '责任追溯记录']},
                {'text': '解决方案制定\\n补救措施确定', 'type': 'process', 'department': '品质部', 'forms': ['解决方案', '补救措施计划']},
                {'text': '方案客户确认\\n实施条件协商', 'type': 'process', 'department': '业务部', 'forms': ['客户确认书', '实施协商记录']},
                {'text': '解决方案实施\\n执行过程监控', 'type': 'process', 'department': '相关部门', 'forms': ['实施执行记录', '过程监控表']},
                {'text': '客户满意度确认\\n投诉关闭验证', 'type': 'process', 'department': '业务部', 'forms': ['满意度确认', '投诉关闭验证']},
                {'text': '是否满意解决？\\n客户接受度评估', 'type': 'decision', 'department': '业务部', 'forms': ['满意度评估', '接受度分析']},
                {'text': '预防措施制定\\n系统改进实施', 'type': 'process', 'department': '品质部', 'forms': ['预防措施', '系统改进计划']},
                {'text': '投诉处理流程完成', 'type': 'end', 'department': '业务部', 'forms': []}
            ]
        },
        
        'HQ-QP-18': {
            'name': '产品召回程序',
            'steps': [
                {'text': '召回触发事件\\n安全风险识别', 'type': 'start', 'department': '品质部', 'forms': ['召回触发报告', '安全风险评估']},
                {'text': '风险等级评估\\n召回必要性判定', 'type': 'process', 'department': '品质部', 'forms': ['风险等级评估', '召回必要性分析']},
                {'text': '召回决策制定\\n召回方案设计', 'type': 'process', 'department': '管理层', 'forms': ['召回决策书', '召回方案']},
                {'text': '监管部门通报\\n法规合规确认', 'type': 'process', 'department': '品质部', 'forms': ['监管通报', '合规确认书']},
                {'text': '客户通知发出\\n召回公告发布', 'type': 'process', 'department': '业务部', 'forms': ['客户通知', '召回公告']},
                {'text': '产品追溯定位\\n影响范围确定', 'type': 'process', 'department': '品质部', 'forms': ['追溯定位记录', '影响范围分析']},
                {'text': '产品回收执行\\n物流安排协调', 'type': 'process', 'department': '业务部', 'forms': ['回收执行记录', '物流协调记录']},
                {'text': '产品处置方案\\n销毁或返修决定', 'type': 'process', 'department': '品质部', 'forms': ['处置方案', '处理决定书']},
                {'text': '是否完全回收？\\n回收完成度检查', 'type': 'decision', 'department': '业务部', 'forms': ['回收完成度', '检查确认书']},
                {'text': '效果评估分析\\n经验教训总结', 'type': 'process', 'department': '品质部', 'forms': ['效果评估报告', '教训总结']},
                {'text': '产品召回流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        },
        
        'HQ-QP-19': {
            'name': '产品风险评估管理程序',
            'steps': [
                {'text': '风险评估启动\\n评估范围确定', 'type': 'start', 'department': '品质部', 'forms': ['评估启动申请', '评估范围说明']},
                {'text': '风险识别分析\\n危险源清单建立', 'type': 'process', 'department': '品质部', 'forms': ['风险识别清单', '危险源登记']},
                {'text': '风险概率估算\\n发生可能性分析', 'type': 'process', 'department': '品质部', 'forms': ['概率估算表', '可能性分析']},
                {'text': '风险影响评估\\n后果严重程度分析', 'type': 'process', 'department': '品质部', 'forms': ['影响评估报告', '严重程度分析']},
                {'text': '风险等级确定\\n风险矩阵评定', 'type': 'process', 'department': '品质部', 'forms': ['风险等级表', '风险矩阵']},
                {'text': '风险可接受性\\n容忍度评估判定', 'type': 'decision', 'department': '管理层', 'forms': ['可接受性评估', '容忍度判定']},
                {'text': '风险控制措施\\n防控方案制定', 'type': 'process', 'department': '品质部', 'forms': ['控制措施计划', '防控方案']},
                {'text': '措施实施执行\\n控制效果监控', 'type': 'process', 'department': '相关部门', 'forms': ['实施执行记录', '效果监控表']},
                {'text': '剩余风险评估\\n残留风险分析', 'type': 'process', 'department': '品质部', 'forms': ['剩余风险评估', '残留风险分析']},
                {'text': '定期风险评审\\n动态跟踪管理', 'type': 'process', 'department': '品质部', 'forms': ['定期评审记录', '动态跟踪表']},
                {'text': '风险评估流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        },
        
        'HQ-QP-20': {
            'name': '风险评估控制程序',
            'steps': [
                {'text': '评估需求确定\\n评估目标设定', 'type': 'start', 'department': '品质部', 'forms': ['评估需求申请', '目标设定书']},
                {'text': '评估方法选择\\n评估工具准备', 'type': 'process', 'department': '品质部', 'forms': ['方法选择依据', '工具准备清单']},
                {'text': '数据收集整理\\n信息来源验证', 'type': 'process', 'department': '各部门', 'forms': ['数据收集表', '信息来源验证']},
                {'text': '定性风险分析\\n专家判断评估', 'type': 'process', 'department': '品质部', 'forms': ['定性分析报告', '专家评估意见']},
                {'text': '定量风险分析\\n数值计算建模', 'type': 'process', 'department': '品质部', 'forms': ['定量分析报告', '计算模型']},
                {'text': '风险综合评价\\n多维度综合判定', 'type': 'process', 'department': '品质部', 'forms': ['综合评价报告', '多维判定表']},
                {'text': '评估结果是否合理？\\n结果有效性验证', 'type': 'decision', 'department': '管理层', 'forms': ['合理性评估', '有效性验证']},
                {'text': '评估报告编制\\n结论建议形成', 'type': 'process', 'department': '品质部', 'forms': ['评估报告', '结论建议书']},
                {'text': '评估结果应用\\n决策支持提供', 'type': 'process', 'department': '管理层', 'forms': ['结果应用记录', '决策支持文件']},
                {'text': '评估质量审查\\n独立第三方验证', 'type': 'process', 'department': '品质部', 'forms': ['质量审查报告', '第三方验证']},
                {'text': '风险评估控制流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        }
    }
    
    return remaining_specs

# 输出规格用于添加到扩展规格库
if __name__ == "__main__":
    specs = generate_remaining_specs()
    print("# 剩余专业规格")
    for doc_code, spec in specs.items():
        print(f"\n'{doc_code}': {{")
        print(f"    'name': '{spec['name']}',")
        print("    'steps': [")
        for step in spec['steps']:
            forms_str = str(step['forms']).replace("'", '"')
            print(f"        {{'text': '{step['text']}', 'type': '{step['type']}', 'department': '{step['department']}', 'forms': {forms_str}}},")
        print("    ]")
        print("},")