import win32com.client
import os

def edit_image_with_photoshop():
    try:
        # 启动Photoshop应用程序
        psApp = win32com.client.Dispatch("Photoshop.Application")
        print("Photoshop已启动")
        
        # 打开指定的PNG文件
        image_path = r"D:\7.Desktop\ls\Trae\白名单.png"
        
        if not os.path.exists(image_path):
            print(f"文件不存在: {image_path}")
            return
            
        # 打开文件
        doc = psApp.Open(image_path)
        print(f"已打开文件: {image_path}")
        
        # 创建文本图层
        text_layer = doc.ArtLayers.Add()
        text_layer.Kind = 2  # 文本图层类型
        text_layer.Name = "作废标记"
        
        # 设置文本内容
        text_item = text_layer.TextItem
        text_item.Contents = "作废"
        text_item.Size = 72  # 字体大小
        text_item.Color.RGB.Red = 255
        text_item.Color.RGB.Green = 0
        text_item.Color.RGB.Blue = 0  # 红色文字
        
        # 设置文本位置（居中）
        text_item.Position = [doc.Width / 2 - 100, doc.Height / 2]
        
        print("已添加'作废'文字")
        
        # 保存文件
        save_path = r"D:\7.Desktop\ls\Trae\白名单_作废.png"
        
        # 导出为PNG
        png_options = win32com.client.Dispatch("Photoshop.ExportOptionsSaveForWeb")
        png_options.Format = 13  # PNG格式
        png_options.PNG8 = False  # 使用PNG24
        
        doc.Export(save_path, 2, png_options)  # 2表示SaveForWeb导出
        print(f"文件已保存为: {save_path}")
        
        # 关闭文档
        doc.Close(2)  # 2表示不保存原文件
        print("操作完成")
        
    except Exception as e:
        print(f"操作失败: {str(e)}")
        print("请确保:")
        print("1. Photoshop已安装")
        print("2. 文件路径正确")
        print("3. 有足够的权限访问文件")

if __name__ == "__main__":
    edit_image_with_photoshop()