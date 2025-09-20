# AI生成流程图规范

## 📋 基于实际修复经验的完整规范

**文档版本**: v1.0  
**制定时间**: 2025年08月29日  
**基于案例**: 小家电制造业详细生产流程图修复过程  
**适用范围**: 所有AI生成的Draw.io流程图

---

## 🎯 核心原则

### 1. 严格遵循Draw.io XML标准
- 必须完全符合mxGraph格式规范
- 严禁使用自定义或非标准XML结构
- 确保100%的Draw.io兼容性

### 2. XML结构完整性
- 所有mxCell元素必须在`<root>`标签内部
- 严禁在`</root>`标签后添加任何mxCell元素
- 确保所有XML标签正确闭合

### 3. 元素ID唯一性
- 每个mxCell元素的ID必须在文档内唯一
- 严禁重复定义相同ID的元素
- 使用有意义的ID命名规则

---

## 🔧 技术规范细则

### 1. XML文档结构规范 ⭐⭐⭐⭐⭐

#### ✅ 正确的文档结构
```xml
<?xml version='1.0' encoding='utf-8'?>
<mxfile host="Electron" agent="Mozilla/5.0..." version="28.0.6">
  <diagram name="流程图名称" id="flowchart">
    <mxGraphModel dx="1042" dy="643" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="8000" pageHeight="6000" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- 所有业务节点、泳道、连接线都必须在这里 -->
        <mxCell id="title" value="标题文本" style="..." parent="1" vertex="1">
          <mxGeometry x="2400" y="40" width="600" height="80" as="geometry" />
        </mxCell>
        
        <!-- 其他所有元素 -->
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

#### ❌ 严禁的错误结构
```xml
<!-- 错误示例1：元素在root外部 -->
</root>
<mxCell id="Q01_IQC" ...>  <!-- 这里绝对不能有元素 -->
</mxGraphModel>

<!-- 错误示例2：重复ID定义 -->
<mxCell id="S25" parent="lane_customer">...</mxCell>
...
<mxCell id="S25" parent="1">...</mxCell>  <!-- 重复ID，禁止 -->
```

### 2. 连接线Array格式规范 ⭐⭐⭐⭐⭐

#### ✅ 标准Array格式（必须使用）
```xml
<mxCell id="edge_001" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;" parent="1" source="S01" target="S02" edge="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="265" y="300" />
      <mxPoint x="445" y="300" />
    </Array>
  </mxGeometry>
</mxCell>
```

#### ❌ 严禁的自定义Array格式
```xml
<!-- 错误示例1：缺少as="points"属性 -->
<Array>
  <mxPoint x="5170" y="465" />
  <mxPoint x="5132" y="432" />
</Array>

<!-- 错误示例2：使用自定义弧形Array -->
<Array>
  <mxPoint x="5198" y="465" />
  <mxPoint x="5170" y="432" />
  <mxPoint x="5053" y="400" />
  <!-- 复杂弧形点定义 -->
</Array>

<!-- 错误示例3：使用非标准样式 -->
style="curved=1;noEdgeStyle=1;curveFitting=1;"
```

### 3. XML注释规范 ⭐⭐⭐⭐⭐

#### ✅ 正确的注释位置
```xml
<!-- 正确：注释在元素外部 -->
<mxCell id="edge_030" style="..." parent="1" source="S22" target="S23" edge="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="4765" y="1335" />
    </Array>
  </mxGeometry>
</mxCell>

<!-- 品质部连接线开始 -->
<mxCell id="edge_Q01" style="..." parent="1" source="S13" target="Q01_IQC" edge="1">
```

#### ❌ 严禁的注释位置
```xml
<!-- 错误：注释在元素内部 -->
        </mxCell>
        
        <!-- 品质部连接线 -->  ← 绝对禁止在这里！
        <mxCell id="edge_Q01"
```

### 4. 泳道设计规范 ⭐⭐⭐⭐

#### ✅ 标准泳道定义
```xml
<mxCell id="lane_business" value="业务部" style="swimlane;html=1;startSize=20;horizontal=0;fillColor=#FFE6E6;strokeColor=#4A90E2;strokeWidth=2;strokeDashArray=15,5;fontSize=14;fontStyle=1;" parent="1" vertex="1">
  <mxGeometry x="100" y="250" width="5700" height="100" as="geometry" />
</mxCell>
```

#### 🎨 泳道样式规范
- **边框颜色**: 统一使用`#4A90E2`
- **边框样式**: `strokeDashArray=15,5`（长虚线）
- **边框宽度**: `strokeWidth=2`
- **背景色**: 每个部门使用不同的浅色背景
- **字体**: `fontSize=14;fontStyle=1`（粗体）

### 5. 业务节点设计规范 ⭐⭐⭐⭐

#### ✅ 标准业务节点格式
```xml
<mxCell id="S01" value="S01. 客户询价&#10;需求初步了解&#10;&#10;🏢 客户&#10;💻 询价系统&#10;&#10;📌 业务跟单要点:&#10;• 客户需求记录&#10;• 初步可行性评估" style="ellipse;whiteSpace=wrap;html=1;fillColor=#E6F3FF;strokeColor=#000000;fontSize=10;fontStyle=1;" parent="1" vertex="1">
  <mxGeometry x="200" y="165" width="130" height="70" as="geometry" />
</mxCell>
```

#### 📝 节点内容规范
- **节点编号**: S01, S02, S03... 按流程顺序编号
- **业务描述**: 简洁明确的2行描述
- **部门信息**: 🏢 负责部门
- **系统信息**: 💻 使用系统
- **要点说明**: 📌 业务跟单要点（2-3个要点）
- **节点尺寸**: 统一130×70像素

### 6. 连接线设计规范 ⭐⭐⭐⭐

#### ✅ 主流程连接线
```xml
<mxCell id="edge_001" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;" parent="1" source="S01" target="S02" edge="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

#### ✅ 分支流程连接线
```xml
<mxCell id="edge_005" value="接受" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#45B7D1;strokeWidth=2;" parent="1" source="D01" target="S06" edge="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="985" y="600" />
      <mxPoint x="1165" y="600" />
    </Array>
  </mxGeometry>
</mxCell>
```

#### 🎨 连接线颜色分类
- **黑色** (`#333333`): 主流程连接线
- **蓝色** (`#45B7D1`): 决策接受分支
- **红色** (`#FF6B6B`): 决策拒绝分支
- **橙色** (`#FF6600`): 品质管控连接线
- **青色** (`#4ECDC4`): 财务流程连接线

### 7. 交叉优化处理规范 ⭐⭐⭐

#### ✅ 标准交叉避让方法
```xml
<!-- 使用路径点实现交叉避让 -->
<mxCell id="edge_035" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;" parent="1" source="S27" target="S28" edge="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="5198" y="465" />
      <mxPoint x="5198" y="400" />
      <mxPoint x="4230" y="400" />
    </Array>
  </mxGeometry>
</mxCell>
```

#### ❌ 禁止的弧形处理方式
```xml
<!-- 禁止使用自定义弧形 -->
style="curved=1;noEdgeStyle=1;curveFitting=1;"
<Array>
  <!-- 复杂弧形控制点 -->
</Array>
```

### 8. 品质管控集成规范 ⭐⭐⭐

#### ✅ 品质部节点规范
```xml
<mxCell id="Q01_IQC" value="IQC来料检验\n原材料质量检查" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF0E6;strokeColor=#FF6600;strokeWidth=2;fontSize=9;" parent="1" vertex="1">
  <mxGeometry x="2950" y="1485" width="120" height="50" as="geometry" />
</mxCell>
```

#### ✅ 品质连接线规范
```xml
<mxCell id="edge_Q01" value="来料检验" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#FF6600;strokeWidth=2;fontSize=9;fontColor=#FF6600;" parent="1" source="S13" target="Q01_IQC" edge="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="2965" y="1000" />
      <mxPoint x="3010" y="1000" />
      <mxPoint x="3010" y="1510" />
    </Array>
  </mxGeometry>
</mxCell>
```

---

## 🚨 重点错误防范

### 1. 绝对禁止的操作

#### ❌ XML结构错误
- 在`</root>`标签后添加任何mxCell元素
- 元素嵌套错误或标签未闭合
- 使用不标准的XML语法

#### ❌ Array格式错误
- 使用`<Array>`而不是`<Array as="points">`
- 在Array中使用非标准属性
- 创建过于复杂的弧形路径

#### ❌ ID重复错误
- 在同一文档中使用重复的元素ID
- 忘记为新增元素分配唯一ID

#### ❌ 注释位置错误
- 在XML元素内部添加注释
- 注释破坏XML元素结构

### 2. 常见错误修复方法

#### 🔧 Array格式修复
```xml
<!-- 错误格式 -->
<Array><mxPoint x="100" y="200" /></Array>

<!-- 正确格式 -->
<Array as="points">
  <mxPoint x="100" y="200" />
</Array>
```

#### 🔧 重复ID修复
```xml
<!-- 删除重复定义，保留在正确位置的元素 -->
<!-- 保留 --> <mxCell id="S25" parent="lane_customer">...</mxCell>
<!-- 删除 --> <!-- <mxCell id="S25" parent="1">...</mxCell> -->
```

#### 🔧 XML结构修复
```xml
<!-- 错误结构 -->
</root>
<mxCell id="Q01">...</mxCell>

<!-- 正确结构 -->
  <mxCell id="Q01">...</mxCell>
</root>
```

---

## 📊 质量检查清单

### 生成前检查 ✅
- [ ] 确认XML文档结构完整
- [ ] 验证所有元素ID唯一性
- [ ] 检查Array格式标准性
- [ ] 确认注释位置正确性

### 生成后验证 ✅
- [ ] XML语法检查无错误
- [ ] Draw.io兼容性测试通过
- [ ] 连接线显示正常
- [ ] 节点布局合理
- [ ] 交叉处理有效

### 修复指导 🔧
- [ ] 按规范修复Array格式
- [ ] 移除重复ID定义
- [ ] 调整XML结构嵌套
- [ ] 移除错误位置注释
- [ ] 优化连接线路径

---

## 🎯 最佳实践总结

### 1. 遵循标准第一
- 严格按照Draw.io官方XML格式规范
- 不使用任何自定义或非标准结构
- 确保100%兼容性

### 2. 结构完整性
- 所有元素必须在正确的XML层级内
- 保持清晰的文档结构层次
- 确保所有标签正确闭合

### 3. 视觉专业性
- 使用统一的设计规范
- 保持颜色和样式一致性
- 实现有效的交叉避让

### 4. 业务完整性
- 包含完整的业务流程覆盖
- 集成必要的质量管控环节
- 提供详细的业务说明

---

## 📚 参考案例

**成功案例**: 小家电制造业详细生产流程图  
**文件路径**: `s:\PG-GMO\office\业务部\小家电制造业详细生产流程图-交叉优化版.drawio`  
**质量等级**: 🌟🌟🌟🌟🌟 企业级完美标准

**关键特点**:
- 35个业务步骤 + 2个决策节点
- 14个部门泳道布局
- 50条连接线（包括8条品质连线）
- 完美的交叉避让处理
- 100% Draw.io兼容性

---

**制定人**: AI助手  
**版本**: v1.0  
**制定时间**: 2025年08月29日  
**适用范围**: 所有Draw.io流程图生成项目

**重要提醒**: 🚨 **严格遵循本规范，确保生成的流程图达到企业级标准！**