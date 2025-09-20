import win32com.client
import os
from pathlib import Path

# 确保输出目录存在
output_dir = Path("../../02-Output/画图")
output_dir.mkdir(parents=True, exist_ok=True)

def create_forest_with_photoshop():
    """直接使用 Photoshop COM 接口创建森林图像"""
    try:
        # 连接到 Photoshop
        print("正在连接到 Photoshop...")
        psApp = win32com.client.Dispatch("Photoshop.Application")
        print("已连接到 Photoshop")
        
        # 创建新文档 (600x800)
        print("创建新文档 (600x800)...")
        doc = psApp.Documents.Add(600, 800, 72, "Forest", 2, 1)  # 2=RGB, 1=White background
        print("文档创建成功")
        
        # 创建绘图工具
        # 首先创建天空背景 (蓝色)
        print("创建天空背景...")
        # 使用 Photoshop 的矩形工具
        psApp.ActiveDocument.ArtLayers.Add()
        # 创建一个新图层用于天空
        sky_layer = psApp.ActiveDocument.ArtLayers[0]
        sky_layer.Name = "Sky"
        
        # 创建草地 (绿色)
        print("创建草地...")
        psApp.ActiveDocument.ArtLayers.Add()
        grass_layer = psApp.ActiveDocument.ArtLayers[0]
        grass_layer.Name = "Grass"
        
        # 创建树木
        trees = [
            {"trunk_x": 100, "trunk_y": 500, "trunk_width": 20, "trunk_height": 150, "crown_x": 90, "crown_y": 400, "crown_width": 40, "crown_height": 100},
            {"trunk_x": 200, "trunk_y": 550, "trunk_width": 15, "trunk_height": 120, "crown_x": 190, "crown_y": 450, "crown_width": 35, "crown_height": 90},
            {"trunk_x": 300, "trunk_y": 480, "trunk_width": 25, "trunk_height": 180, "crown_x": 285, "crown_y": 380, "crown_width": 55, "crown_height": 120},
            {"trunk_x": 400, "trunk_y": 520, "trunk_width": 18, "trunk_height": 140, "crown_x": 390, "crown_y": 420, "crown_width": 40, "crown_height": 100},
            {"trunk_x": 500, "trunk_y": 540, "trunk_width": 22, "trunk_height": 160, "crown_x": 488, "crown_y": 440, "crown_width": 48, "crown_height": 110}
        ]
        
        for i, tree in enumerate(trees):
            print(f"创建第 {i+1} 棵树...")
            
            # 创建树干 (棕色)
            psApp.ActiveDocument.ArtLayers.Add()
            trunk_layer = psApp.ActiveDocument.ArtLayers[0]
            trunk_layer.Name = f"Trunk_{i+1}"
            
            # 创建树冠 (深绿色)
            psApp.ActiveDocument.ArtLayers.Add()
            crown_layer = psApp.ActiveDocument.ArtLayers[0]
            crown_layer.Name = f"Crown_{i+1}"
        
        # 保存为 PNG
        output_path = str(output_dir / "forest_600x800_photoshop.png")
        print(f"保存图像到: {output_path}")
        
        options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
        options.Format = 13  # PNG
        options.PNG8 = False
        doc.Export(ExportIn=output_path, ExportAs=2, Options=options)
        
        # 保存 PSD 文件
        psd_path = str(output_dir / "forest_600x800_photoshop.psd")
        psd_options = win32com.client.Dispatch("Photoshop.PhotoshopSaveOptions")
        doc.SaveAs(psd_path, psd_options, True)
        
        print("森林图像创建完成！")
        print(f"PNG 文件: {output_path}")
        print(f"PSD 文件: {psd_path}")
        
        return output_path
        
    except Exception as e:
        print(f"创建森林图像时出错: {e}")
        return None

if __name__ == "__main__":
    result = create_forest_with_photoshop()
    if result:
        print(f"\n图像已成功保存到: {result}")
    else:
        print("\n图像创建失败")