#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
由Pygubu GUI设计器自动生成的代码
UI文件: basic_form.ui
生成时间: 2025-09-19 13:51:23
"""

import tkinter as tk
import tkinter.ttk as ttk
import pygubu

class BasicFormApp:
    def __init__(self, master=None):
        # 构建UI
        self.builder = pygubu.Builder()
        self.builder.add_from_file(r"gui-templates\basic_form.ui")
        
        # 创建主窗口
        if master is None:
            self.mainwindow = tk.Tk()
        else:
            self.mainwindow = master
            
        # 构建界面
        self.builder.get_object('main_window', self.mainwindow)
        
        # 连接回调函数
        self.builder.connect_callbacks(self)
        
    def run(self):
        """运行应用程序"""
        self.mainwindow.mainloop()
        
    # 在这里添加你的回调函数
    def on_submit_clicked(self):
        """提交按钮点击事件"""
        print("提交按钮被点击")
        
    def on_cancel_clicked(self):
        """取消按钮点击事件"""
        print("取消按钮被点击")
        self.mainwindow.quit()

def main():
    """主函数"""
    app = BasicFormApp()
    app.run()

if __name__ == "__main__":
    main()
