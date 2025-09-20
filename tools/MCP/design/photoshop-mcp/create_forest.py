import win32com.client
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 连接到正在运行的 Photoshop 实例
psApp = win32com.client.Dispatch("Photoshop.Application")

# 创建一个新文档 (600x800 像素)
doc = psApp.Documents.Add(600, 800, 72, "Forest", 2, 1)  # 2=RGB, 1=White background

print("已创建 600x800 的新文档")

# 由于我们无法直接生成真实的森林图像，我们可以通过创建一些基本形状来模拟森林
# 创建一个绿色的背景来代表草地
# 首先选择整个画布
psApp.ActiveDocument.Selection.Select([[0, 0], [600, 0], [600, 800], [0, 800]], 1, 0)
# 填充为绿色
psApp.ActiveDocument.Selection.Fill(psApp.SolidColor(255, 0, 128, 0))  # RGB(0, 128, 0) = 绿色

print("已创建草地背景")

# 取消选择
psApp.ActiveDocument.Selection.Deselect()

# 创建一些树木的形状
# 我们将创建几个棕色的树干和绿色的树冠来模拟森林
trees = [
    {"trunk_x": 100, "trunk_y": 500, "trunk_width": 20, "trunk_height": 150, "crown_x": 90, "crown_y": 400, "crown_width": 40, "crown_height": 100},
    {"trunk_x": 200, "trunk_y": 550, "trunk_width": 15, "trunk_height": 120, "crown_x": 190, "crown_y": 450, "crown_width": 35, "crown_height": 90},
    {"trunk_x": 300, "trunk_y": 480, "trunk_width": 25, "trunk_height": 180, "crown_x": 285, "crown_y": 380, "crown_width": 55, "crown_height": 120},
    {"trunk_x": 400, "trunk_y": 520, "trunk_width": 18, "trunk_height": 140, "crown_x": 390, "crown_y": 420, "crown_width": 40, "crown_height": 100},
    {"trunk_x": 500, "trunk_y": 540, "trunk_width": 22, "trunk_height": 160, "crown_x": 488, "crown_y": 440, "crown_width": 48, "crown_height": 110}
]

# 创建树木
for i, tree in enumerate(trees):
    # 创建树干 (棕色)
    # 使用正确的数组格式
    psApp.ActiveDocument.Selection.Select([
        [tree["trunk_x"], tree["trunk_y"]], 
        [tree["trunk_x"] + tree["trunk_width"], tree["trunk_y"]], 
        [tree["trunk_x"] + tree["trunk_width"], tree["trunk_y"] + tree["trunk_height"]], 
        [tree["trunk_x"], tree["trunk_y"] + tree["trunk_height"]]
    ], 1, 0)
    # 填充为棕色
    psApp.ActiveDocument.Selection.Fill(psApp.SolidColor(255, 139, 69, 19))  # RGB(139, 69, 19) = 棕色
    
    # 取消选择
    psApp.ActiveDocument.Selection.Deselect()
    
    # 创建树冠 (绿色)
    # 使用正确的数组格式
    psApp.ActiveDocument.Selection.Select([
        [tree["crown_x"], tree["crown_y"]], 
        [tree["crown_x"] + tree["crown_width"], tree["crown_y"]], 
        [tree["crown_x"] + tree["crown_width"], tree["crown_y"] + tree["crown_height"]], 
        [tree["crown_x"], tree["crown_y"] + tree["crown_height"]]
    ], 1, 0)
    # 填充为深绿色
    psApp.ActiveDocument.Selection.Fill(psApp.SolidColor(255, 34, 139, 34))  # RGB(34, 139, 34) = 森林绿
    
    # 取消选择
    psApp.ActiveDocument.Selection.Deselect()
    
    print(f"已创建第 {i+1} 棵树")

# 创建天空区域 (蓝色)
# 使用正确的数组格式
psApp.ActiveDocument.Selection.Select([[0, 0], [600, 0], [600, 400], [0, 400]], 1, 0)
# 填充为浅蓝色
psApp.ActiveDocument.Selection.Fill(psApp.SolidColor(255, 135, 206, 235))  # RGB(135, 206, 235) = 天蓝色

print("已创建天空背景")

# 取消选择
psApp.ActiveDocument.Selection.Deselect()

# 保存文件
EXPORT_DIRECTORY = os.getenv("EXPORT_DIRECTORY", "exports")
if not os.path.exists(EXPORT_DIRECTORY):
    os.makedirs(EXPORT_DIRECTORY)

file_path = os.path.join(EXPORT_DIRECTORY, "forest_600x800.png")
options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
options.Format = 13  # PNG
options.PNG8 = False
doc.Export(ExportIn=file_path, ExportAs=2, Options=options)

print(f"森林图像已保存到: {file_path}")

# 保存为 PSD 格式
psd_path = os.path.join(EXPORT_DIRECTORY, "forest_600x800.psd")
psd_options = win32com.client.Dispatch("Photoshop.PhotoshopSaveOptions")
doc.SaveAs(psd_path, psd_options, True)

print(f"PSD 文件已保存到: {psd_path}")

print("任务完成！已创建 600x800 的森林图像。")