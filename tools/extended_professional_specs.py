#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扩展专业规格库 - 为所有32个ISO文档定义详细的专业规格
基于真实业务流程，确保每个流程图都具备编程序级别的专业性
"""

def get_extended_professional_specifications():
    """获取扩展的专业规格库"""
    return {
        'HQ-QP-03': {
            'name': '内部审核控制程序',
            'steps': [
                {'text': '制定年度内审计划\\n确定审核频次', 'type': 'start', 'department': '品质部', 'forms': ['年度内审计划', '审核频次表']},
                {'text': '确定审核范围目标\\n制定审核准则', 'type': 'process', 'department': '品质部', 'forms': ['审核范围说明', '审核准则']},
                {'text': '组建内审小组\\n分配审核任务', 'type': 'process', 'department': '品质部', 'forms': ['审核小组名单', '任务分配表']},
                {'text': '制定审核实施方案\\n安排审核时间', 'type': 'process', 'department': '内审员', 'forms': ['审核实施方案', '时间安排表']},
                {'text': '编制审核检查表\\n准备审核工具', 'type': 'process', 'department': '内审员', 'forms': ['审核检查表', '审核工具清单']},
                {'text': '发出审核通知书\\n通报相关部门', 'type': 'process', 'department': '品质部', 'forms': ['审核通知书', '通报记录']},
                {'text': '召开首次会议\\n说明审核目的', 'type': 'process', 'department': '内审员', 'forms': ['首次会议记录', '审核说明']},
                {'text': '实施现场审核\\n执行审核程序', 'type': 'process', 'department': '内审员', 'forms': ['现场审核记录', '证据收集表']},
                {'text': '收集审核证据\\n分析符合性', 'type': 'process', 'department': '内审员', 'forms': ['证据清单', '符合性分析']},
                {'text': '不符合项检查\\n判定严重程度', 'type': 'decision', 'department': '内审员', 'forms': ['不符合项清单', '严重程度评估']},
                {'text': '开具不符合项报告\\n详细描述问题', 'type': 'process', 'department': '内审员', 'forms': ['不符合项报告', '问题描述']},
                {'text': '召开末次会议\\n沟通审核结果', 'type': 'process', 'department': '内审员', 'forms': ['末次会议记录', '结果沟通']},
                {'text': '编制内审报告\\n总结审核发现', 'type': 'process', 'department': '内审员', 'forms': ['内审报告', '审核总结']},
                {'text': '要求整改措施\\n制定整改计划', 'type': 'process', 'department': '被审核部门', 'forms': ['整改措施计划', '整改时间表']},
                {'text': '验证整改效果\\n确认改进结果', 'type': 'process', 'department': '内审员', 'forms': ['验证报告', '改进确认']},
                {'text': '关闭不符合项\\n确认整改完成', 'type': 'process', 'department': '品质部', 'forms': ['关闭确认书', '整改验收']},
                {'text': '审核资料归档\\n建立档案管理', 'type': 'process', 'department': '品质部', 'forms': ['归档清单', '档案目录']},
                {'text': '内审流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        },
        
        'HQ-QP-04': {
            'name': '人力资源控制程序',
            'steps': [
                {'text': '人员需求确定\\n岗位分析评估', 'type': 'start', 'department': '用人部门', 'forms': ['人员需求申请', '岗位分析表']},
                {'text': '制定招聘计划\\n确定招聘策略', 'type': 'process', 'department': '人力资源部', 'forms': ['招聘计划', '招聘策略']},
                {'text': '发布招聘信息\\n渠道推广宣传', 'type': 'process', 'department': '人力资源部', 'forms': ['招聘信息', '渠道记录']},
                {'text': '收集简历筛选\\n初步资格审查', 'type': 'process', 'department': '人力资源部', 'forms': ['简历收集表', '筛选记录']},
                {'text': '初步面试评估\\n基础能力测试', 'type': 'process', 'department': '人力资源部', 'forms': ['面试评估表', '能力测试']},
                {'text': '专业技能测试\\n岗位适配评估', 'type': 'process', 'department': '用人部门', 'forms': ['技能测试表', '适配评估']},
                {'text': '候选人评估\\n综合能力判定', 'type': 'decision', 'department': '用人部门', 'forms': ['评估报告', '能力判定']},
                {'text': '背景调查验证\\n诚信度核实', 'type': 'process', 'department': '人力资源部', 'forms': ['背景调查表', '诚信核实']},
                {'text': '录用决定确认\\n薪酬福利谈判', 'type': 'process', 'department': '管理层', 'forms': ['录用决定书', '薪酬协议']},
                {'text': '签署劳动合同\\n建立雇佣关系', 'type': 'process', 'department': '人力资源部', 'forms': ['劳动合同', '入职协议']},
                {'text': '安排入职培训\\n企业文化宣导', 'type': 'process', 'department': '人力资源部', 'forms': ['培训计划', '文化手册']},
                {'text': '岗位技能培训\\n专业能力提升', 'type': 'process', 'department': '用人部门', 'forms': ['技能培训记录', '能力提升计划']},
                {'text': '试用期考核\\n工作表现评估', 'type': 'process', 'department': '用人部门', 'forms': ['试用期考核表', '表现评估']},
                {'text': '能力持续评估\\n职业发展规划', 'type': 'process', 'department': '用人部门', 'forms': ['能力评估表', '发展规划']},
                {'text': '绩效管理跟踪\\n激励机制实施', 'type': 'process', 'department': '人力资源部', 'forms': ['绩效跟踪表', '激励记录']},
                {'text': '人事档案管理\\n信息维护更新', 'type': 'process', 'department': '人力资源部', 'forms': ['人事档案', '信息更新记录']},
                {'text': '人力资源流程完成', 'type': 'end', 'department': '人力资源部', 'forms': []}
            ]
        },
        
        'HQ-QP-05': {
            'name': '设备、设施管理程序',
            'steps': [
                {'text': '设备需求申请\\n技术规格确定', 'type': 'start', 'department': '使用部门', 'forms': ['设备需求申请', '技术规格书']},
                {'text': '制定设备采购计划\\n预算审批申请', 'type': 'process', 'department': '工程部', 'forms': ['采购计划', '预算申请']},
                {'text': '设备技术规格确定\\n性能参数定义', 'type': 'process', 'department': '工程部', 'forms': ['技术规格', '性能参数']},
                {'text': '供应商选择评估\\n资质能力审查', 'type': 'process', 'department': '采购部', 'forms': ['供应商评估', '资质审查']},
                {'text': '设备采购执行\\n合同谈判签署', 'type': 'process', 'department': '采购部', 'forms': ['采购合同', '谈判记录']},
                {'text': '设备验收检查\\n质量符合性确认', 'type': 'process', 'department': '工程部', 'forms': ['验收检查表', '质量确认']},
                {'text': '设备质量评估\\n性能测试验证', 'type': 'decision', 'department': '品质部', 'forms': ['质量评估报告', '性能测试']},
                {'text': '设备安装调试\\n运行参数设定', 'type': 'process', 'department': '工程部', 'forms': ['安装记录', '参数设定']},
                {'text': '操作培训实施\\n安全规程教育', 'type': 'process', 'department': '工程部', 'forms': ['培训记录', '安全教育']},
                {'text': '设备投入使用\\n运行状态监控', 'type': 'process', 'department': '使用部门', 'forms': ['使用记录', '状态监控']},
                {'text': '日常维护保养\\n预防性维护', 'type': 'process', 'department': '工程部', 'forms': ['保养记录', '维护计划']},
                {'text': '定期检修保养\\n设备健康管理', 'type': 'process', 'department': '工程部', 'forms': ['检修记录', '健康评估']},
                {'text': '设备档案管理\\n履历信息维护', 'type': 'process', 'department': '工程部', 'forms': ['设备档案', '履历记录']},
                {'text': '设备报废处置\\n资产处理程序', 'type': 'process', 'department': '行政部', 'forms': ['报废申请', '处置记录']},
                {'text': '设备管理流程完成', 'type': 'end', 'department': '工程部', 'forms': []}
            ]
        },
        
        'HQ-QP-06': {
            'name': '订单评审控制程序',
            'steps': [
                {'text': '客户订单接收\\n订单信息登记', 'type': 'start', 'department': '业务部', 'forms': ['客户订单', '订单登记表']},
                {'text': '订单信息核对\\n客户需求确认', 'type': 'process', 'department': '业务部', 'forms': ['信息核对表', '需求确认书']},
                {'text': '产品技术要求评估\\n可行性初步分析', 'type': 'process', 'department': '研发部', 'forms': ['技术评估', '可行性分析']},
                {'text': '生产能力评估\\n产能负荷分析', 'type': 'process', 'department': '生产部', 'forms': ['产能评估', '负荷分析']},
                {'text': '交期可行性分析\\n排程计划制定', 'type': 'process', 'department': '生产部', 'forms': ['交期分析', '排程计划']},
                {'text': '成本核算分析\\n利润评估计算', 'type': 'process', 'department': '财务部', 'forms': ['成本核算', '利润分析']},
                {'text': '订单可接受性评估\\n风险综合判定', 'type': 'decision', 'department': '业务部', 'forms': ['可接受性评估', '风险判定']},
                {'text': '订单确认回复\\n接单意向表达', 'type': 'process', 'department': '业务部', 'forms': ['订单确认书', '接单回复']},
                {'text': '合同条款谈判\\n细节条件协商', 'type': 'process', 'department': '业务部', 'forms': ['谈判记录', '条款草案']},
                {'text': '正式合同签署\\n法律关系确立', 'type': 'process', 'department': '管理层', 'forms': ['正式合同', '签署记录']},
                {'text': '生产计划安排\\n资源配置调度', 'type': 'process', 'department': '生产部', 'forms': ['生产计划', '资源配置']},
                {'text': '订单跟踪监控\\n执行进度管理', 'type': 'process', 'department': '业务部', 'forms': ['跟踪记录', '进度报告']},
                {'text': '订单档案管理\\n合同文件归档', 'type': 'process', 'department': '业务部', 'forms': ['档案清单', '归档记录']},
                {'text': '订单评审流程完成', 'type': 'end', 'department': '业务部', 'forms': []}
            ]
        },
        
        'HQ-QP-07': {
            'name': '新产品设计开发控制程序',
            'steps': [
                {'text': '设计开发项目启动\\n立项申请审批', 'type': 'start', 'department': '研发部', 'forms': ['项目立项书', '立项审批']},
                {'text': '市场需求调研\\n用户需求分析', 'type': 'process', 'department': '业务部', 'forms': ['市场调研报告', '用户需求分析']},
                {'text': '设计输入确定\\n技术要求定义', 'type': 'process', 'department': '研发部', 'forms': ['设计输入清单', '技术要求']},
                {'text': '技术可行性分析\\n风险评估识别', 'type': 'process', 'department': '研发部', 'forms': ['可行性分析', '风险评估']},
                {'text': '设计方案制定\\n概念设计开发', 'type': 'process', 'department': '研发部', 'forms': ['设计方案', '概念设计']},
                {'text': '方案评审确认\\n技术路线审查', 'type': 'process', 'department': '管理层', 'forms': ['方案评审', '技术审查']},
                {'text': '设计方案可行性\\n技术实现评估', 'type': 'decision', 'department': '研发部', 'forms': ['方案评估', '实现评估']},
                {'text': '详细设计开发\\n工程图纸绘制', 'type': 'process', 'department': '研发部', 'forms': ['详细设计', '工程图纸']},
                {'text': '样品试制验证\\n原型制作测试', 'type': 'process', 'department': '研发部', 'forms': ['样品制作', '测试报告']},
                {'text': '设计验证测试\\n性能指标验证', 'type': 'process', 'department': '品质部', 'forms': ['验证测试', '性能报告']},
                {'text': '设计确认验收\\n客户需求确认', 'type': 'process', 'department': '业务部', 'forms': ['设计确认', '客户验收']},
                {'text': '工艺文件编制\\n生产指导文件', 'type': 'process', 'department': '工程部', 'forms': ['工艺文件', '生产指导']},
                {'text': '小批量试产\\n工艺验证优化', 'type': 'process', 'department': '生产部', 'forms': ['试产记录', '工艺优化']},
                {'text': '设计输出确认\\n技术文件完善', 'type': 'process', 'department': '研发部', 'forms': ['设计输出', '技术文件']},
                {'text': '设计开发流程完成', 'type': 'end', 'department': '研发部', 'forms': []}
            ]
        },
        
        'HQ-QP-08': {
            'name': '外部提供过程、产品和服务控制程序',
            'steps': [
                {'text': '外部需求确定\\n采购要求识别', 'type': 'start', 'department': '各部门', 'forms': ['需求申请', '采购要求']},
                {'text': '供应商资格评估\\n能力审查认证', 'type': 'process', 'department': '采购部', 'forms': ['资格评估', '能力审查']},
                {'text': '合格供应商选择\\n比较评价筛选', 'type': 'process', 'department': '采购部', 'forms': ['供应商名录', '评价筛选']},
                {'text': '采购合同谈判\\n条款条件协商', 'type': 'process', 'department': '采购部', 'forms': ['谈判记录', '条款草案']},
                {'text': '合同条款审核\\n法务风险评估', 'type': 'process', 'department': '品质部', 'forms': ['条款审核', '风险评估']},
                {'text': '供应商合格性\\n最终资质确认', 'type': 'decision', 'department': '品质部', 'forms': ['合格性评估', '资质确认']},
                {'text': '采购合同签署\\n正式协议生效', 'type': 'process', 'department': '采购部', 'forms': ['采购合同', '协议签署']},
                {'text': '采购执行监控\\n交付进度跟踪', 'type': 'process', 'department': '采购部', 'forms': ['执行监控', '进度跟踪']},
                {'text': '产品服务验收\\n质量符合性检查', 'type': 'process', 'department': '使用部门', 'forms': ['验收记录', '质量检查']},
                {'text': '供应商绩效评价\\n服务质量评估', 'type': 'process', 'department': '采购部', 'forms': ['绩效评价', '质量评估']},
                {'text': '供应商关系维护\\n合作伙伴管理', 'type': 'process', 'department': '采购部', 'forms': ['关系维护', '合作管理']},
                {'text': '采购档案管理\\n合同文件归档', 'type': 'process', 'department': '采购部', 'forms': ['档案管理', '文件归档']},
                {'text': '外部提供流程完成', 'type': 'end', 'department': '采购部', 'forms': []}
            ]
        },
        
        'HQ-QP-09': {
            'name': '生产计划和生产过程控制程序',
            'steps': [
                {'text': '开始', 'type': 'start', 'department': '业务部', 'forms': []},
                {'text': '接收客户订单\n填写销售订单', 'type': 'process', 'department': '业务部', 'forms': ['销售订单', '客户需求确认单']},
                {'text': '订单评审\n技术可行性评估', 'type': 'decision', 'department': 'PMC部', 'forms': ['订单评审表', '技术评估报告']},
                {'text': '制定生产计划\n编制生产任务单', 'type': 'process', 'department': 'PMC部', 'forms': ['生产计划表', '生产任务单', '物料需求计划']},
                {'text': '物料准备\n库存检查', 'type': 'process', 'department': '仓库', 'forms': ['物料清单', '库存报表', '领料单']},
                {'text': '工艺准备\n设备检查', 'type': 'process', 'department': '工程部', 'forms': ['工艺流程图', '作业指导书', '设备点检表']},
                {'text': '生产开始\n首件检验', 'type': 'process', 'department': '生产部', 'forms': ['生产日报表', '首件检验记录']},
                {'text': '生产过程控制\n质量监控', 'type': 'process', 'department': '品质部', 'forms': ['QC巡查报告', '工艺参数记录', '异常报告']},
                {'text': '质量检验', 'type': 'decision', 'department': '品质部', 'forms': ['检验记录表', '不合格品处理单']},
                {'text': '返工/返修', 'type': 'process', 'department': '生产部', 'forms': ['返工单', '返修记录']},
                {'text': '最终检验\n包装入库', 'type': 'process', 'department': '品质部', 'forms': ['最终检验报告', '包装清单']},
                {'text': '发货交付\n客户确认', 'type': 'process', 'department': '仓库', 'forms': ['发货单', '客户签收单']},
                {'text': '结束', 'type': 'end', 'department': '业务部', 'forms': []}
            ]
        },
        
        'HQ-QP-10': {
            'name': '产品标识与可追溯性控制程序',
            'steps': [
                {'text': '标识需求确定\n产品特性分析', 'type': 'start', 'department': '生产部', 'forms': ['标识需求申请', '产品特性分析']},
                {'text': '标识规则制定\n编码体系设计', 'type': 'process', 'department': '品质部', 'forms': ['标识规则', '编码体系']},
                {'text': '标识材料准备\n标签模板设计', 'type': 'process', 'department': '仓储部', 'forms': ['材料清单', '模板设计']},
                {'text': '产品标识实施\n批次信息记录', 'type': 'process', 'department': '生产部', 'forms': ['标识记录', '批次信息']},
                {'text': '标识质量检查\n清晰度验证', 'type': 'process', 'department': '品质部', 'forms': ['质量检查表', '清晰度检查']},
                {'text': '标识是否清晰？\n可识别性评估', 'type': 'decision', 'department': '品质部', 'forms': ['清晰度评估', '可识别性报告']},
                {'text': '标识信息记录\n追溯数据建立', 'type': 'process', 'department': '生产部', 'forms': ['信息记录表', '追溯数据库']},
                {'text': '追溯信息维护\n数据更新管理', 'type': 'process', 'department': '品质部', 'forms': ['信息维护记录', '数据更新日志']},
                {'text': '标识状态监控\n损坏检查管理', 'type': 'process', 'department': '品质部', 'forms': ['状态监控表', '损坏检查记录']},
                {'text': '追溯系统更新\n数据库同步', 'type': 'process', 'department': '品质部', 'forms': ['系统更新日志', '数据同步记录']},
                {'text': '追溯记录归档\n数据备份管理', 'type': 'process', 'department': '品质部', 'forms': ['归档清单', '备份管理记录']},
                {'text': '标识控制流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        },
        
        'HQ-QP-11': {
            'name': '监视和测量资源控制程序',
            'steps': [
                {'text': '测量需求确定\n设备需求分析', 'type': 'start', 'department': '品质部', 'forms': ['测量需求申请', '设备需求分析']},
                {'text': '测量设备选择\n技术规格审查', 'type': 'process', 'department': '品质部', 'forms': ['设备选型表', '技术规格']},
                {'text': '设备采购安装\n环境条件配置', 'type': 'process', 'department': '采购部', 'forms': ['采购合同', '安装记录']},
                {'text': '设备校准检定\n准确度验证', 'type': 'process', 'department': '品质部', 'forms': ['校准记录', '准确度报告']},
                {'text': '校准结果评定\n不确定度分析', 'type': 'process', 'department': '品质部', 'forms': ['校准结果', '不确定度分析']},
                {'text': '设备是否合格？\n性能指标评估', 'type': 'decision', 'department': '品质部', 'forms': ['合格性评估', '性能指标报告']},
                {'text': '设备投入使用\n操作培训实施', 'type': 'process', 'department': '品质部', 'forms': ['使用记录', '培训记录']},
                {'text': '日常维护保养\n使用状态监控', 'type': 'process', 'department': '品质部', 'forms': ['维护记录', '状态监控表']},
                {'text': '定期校准检查\n漂移状态分析', 'type': 'process', 'department': '品质部', 'forms': ['定期校准计划', '漂移分析']},
                {'text': '设备状态监控\n故障预警管理', 'type': 'process', 'department': '品质部', 'forms': ['状态监控记录', '故障预警日志']},
                {'text': '校准记录管理\n证书维护更新', 'type': 'process', 'department': '品质部', 'forms': ['校准记录档案', '证书管理']},
                {'text': '设备档案管理\n历史数据维护', 'type': 'process', 'department': '品质部', 'forms': ['设备档案', '历史数据']},
                {'text': '测量资源流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        },
        
        'HQ-QP-12': {
            'name': '顾客满意控制程序',
            'steps': [
                {'text': '满意度调查计划\n调查方案设计', 'type': 'start', 'department': '业务部', 'forms': ['调查计划', '方案设计']},
                {'text': '调查问卷制作\n评价指标设定', 'type': 'process', 'department': '业务部', 'forms': ['调查问卷', '评价指标']},
                {'text': '调查活动实施\n数据收集执行', 'type': 'process', 'department': '业务部', 'forms': ['调查执行记录', '数据收集表']},
                {'text': '数据收集整理\n样本有效性检查', 'type': 'process', 'department': '业务部', 'forms': ['数据整理表', '样本检查']},
                {'text': '满意度数据分析\n趋势对比研究', 'type': 'process', 'department': '业务部', 'forms': ['数据分析报告', '趋势对比']},
                {'text': '满意度是否达标？\n目标对比评估', 'type': 'decision', 'department': '业务部', 'forms': ['达标评估', '目标对比分析']},
                {'text': '问题原因分析\n根本原因识别', 'type': 'process', 'department': '业务部', 'forms': ['原因分析报告', '根本原因分析']},
                {'text': '改进措施制定\n行动计划编制', 'type': 'process', 'department': '管理层', 'forms': ['改进措施计划', '行动计划']},
                {'text': '改进措施实施\n跨部门协调执行', 'type': 'process', 'department': '各部门', 'forms': ['改进实施记录', '协调执行记录']},
                {'text': '改进效果跟踪\n持续监控评估', 'type': 'process', 'department': '业务部', 'forms': ['效果跟踪表', '监控评估报告']},
                {'text': '满意度记录归档\n持续改进管理', 'type': 'process', 'department': '业务部', 'forms': ['满意度档案', '改进管理记录']},
                {'text': '顾客满意流程完成', 'type': 'end', 'department': '业务部', 'forms': []}
            ]
        },
        
        'HQ-QP-13': {
            'name': '产品放行控制程序',
            'steps': [
                {'text': '产品检验申请\n放行准备检查', 'type': 'start', 'department': '生产部', 'forms': ['检验申请单', '放行准备清单']},
                {'text': '检验计划制定\n检验标准确定', 'type': 'process', 'department': '品质部', 'forms': ['检验计划', '检验标准']},
                {'text': '检验准备工作\n设备工具检查', 'type': 'process', 'department': '品质部', 'forms': ['准备工作清单', '设备检查记录']},
                {'text': '产品检验实施\n全面质量检测', 'type': 'process', 'department': '品质部', 'forms': ['检验记录表', '质量检测报告']},
                {'text': '检验数据分析\n统计过程控制', 'type': 'process', 'department': '品质部', 'forms': ['数据分析报告', '统计控制图']},
                {'text': '检验结果判定\n合格性综合评估', 'type': 'process', 'department': '品质部', 'forms': ['结果判定报告', '合格性评估']},
                {'text': '产品是否合格？\n放行条件检查', 'type': 'decision', 'department': '品质部', 'forms': ['合格性判定', '放行条件检查']},
                {'text': '放行决策确认\n授权签字审批', 'type': 'process', 'department': '品质部', 'forms': ['放行决策记录', '授权签字']},
                {'text': '放行文件签署\n放行证书开具', 'type': 'process', 'department': '品质部', 'forms': ['放行文件', '放行证书']},
                {'text': '产品发货准备\n包装标识检查', 'type': 'process', 'department': '仓储部', 'forms': ['发货准备单', '包装检查记录']},
                {'text': '发货执行监控\n物流跟踪管理', 'type': 'process', 'department': '业务部', 'forms': ['发货执行记录', '物流跟踪']},
                {'text': '放行记录归档\n质量追溯管理', 'type': 'process', 'department': '品质部', 'forms': ['放行记录档案', '追溯管理记录']},
                {'text': '产品放行流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        },
        
        'HQ-QP-14': {
            'name': '不合格品控制程序',
            'steps': [
                {'text': '不合格品发现\n问题识别登记', 'type': 'start', 'department': '各部门', 'forms': ['不合格品报告', '问题识别登记']},
                {'text': '不合格品标识\n状态标识管理', 'type': 'process', 'department': '品质部', 'forms': ['标识标签', '状态记录表']},
                {'text': '不合格品隔离\n防止误用措施', 'type': 'process', 'department': '仓储部', 'forms': ['隔离区域记录', '防误用措施']},
                {'text': '不合格原因分析\n根本原因调查', 'type': 'process', 'department': '品质部', 'forms': ['原因分析报告', '调查记录']},
                {'text': '处置方案确定\n技术可行性评估', 'type': 'process', 'department': '品质部', 'forms': ['处置方案', '可行性评估']},
                {'text': '是否可以返工？\n经济性评估分析', 'type': 'decision', 'department': '品质部', 'forms': ['返工可行性评估', '经济性分析']},
                {'text': '返工处理执行\n返工过程监控', 'type': 'process', 'department': '生产部', 'forms': ['返工指令单', '返工过程记录']},
                {'text': '处置效果验证\n质量再次检验', 'type': 'process', 'department': '品质部', 'forms': ['处置效果验证', '再次检验报告']},
                {'text': '预防措施制定\n系统性改进方案', 'type': 'process', 'department': '品质部', 'forms': ['预防措施计划', '改进方案']},
                {'text': '预防措施实施\n相关部门协调执行', 'type': 'process', 'department': '相关部门', 'forms': ['预防实施记录', '协调执行记录']},
                {'text': '记录整理归档\n经验教训总结', 'type': 'process', 'department': '品质部', 'forms': ['记录归档清单', '经验教训总结']},
                {'text': '不合格品流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        },
        
        'HQ-QP-15': {
            'name': '分析评价及过程监控控制程序',
            'steps': [
                {'text': '数据收集计划制定\n监控指标确定', 'type': 'start', 'department': '品质部', 'forms': ['数据收集计划', '监控指标清单']},
                {'text': '数据收集执行\n多渠道信息获取', 'type': 'process', 'department': '各部门', 'forms': ['数据收集表', '信息来源记录']},
                {'text': '数据整理清洗\n有效性完整性检查', 'type': 'process', 'department': '品质部', 'forms': ['数据整理表', '有效性检查记录']},
                {'text': '统计分析处理\n趋势规律识别', 'type': 'process', 'department': '品质部', 'forms': ['统计分析报告', '趋势分析图表']},
                {'text': '过程能力评价\nCpk能力指数计算', 'type': 'process', 'department': '品质部', 'forms': ['过程能力评价', 'Cpk计算报告']},
                {'text': '性能指标对比\n目标达成情况分析', 'type': 'process', 'department': '品质部', 'forms': ['性能指标对比', '目标达成分析']},
                {'text': '过程是否稳定？\n稳定性评估判定', 'type': 'decision', 'department': '品质郦', 'forms': ['稳定性评估', '判定结果报告']},
                {'text': '问题原因分析\n根本原因清单制定', 'type': 'process', 'department': '品质部', 'forms': ['问题原因分析', '根本原因清单']},
                {'text': '改进措施制定\n统计过程控制计划', 'type': 'process', 'department': '品质部', 'forms': ['改进措施计划', 'SPC控制计划']},
                {'text': '改进措施实施\n过程参数优化', 'type': 'process', 'department': '生产部', 'forms': ['改进实施记录', '参数优化记录']},
                {'text': '效果验证评估\n持续监控机制建立', 'type': 'process', 'department': '品质部', 'forms': ['效果验证报告', '持续监控机制']},
                {'text': '分析评价流程完成', 'type': 'end', 'department': '品质部', 'forms': []}
            ]
        }
    }

if __name__ == "__main__":
    specs = get_extended_professional_specifications()
    print(f"已定义 {len(specs)} 个专业文档规格")
    for doc_code, spec in specs.items():
        print(f"{doc_code}: {spec['name']} - {len(spec['steps'])} 个步骤")