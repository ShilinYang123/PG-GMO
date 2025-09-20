@echo off
REM 下载 n8n 可执行文件
REM 作者: AI Assistant
REM 日期: 2025-09-07

title 下载 n8n 可执行文件

echo ========================================
echo        下载 n8n 可执行文件
echo ========================================
echo.

REM 检查 D:\Program Files 目录
if not exist "D:\Program Files" (
    echo [错误] D:\Program Files 目录不存在
    pause
    exit /b 1
)

echo [信息] D:\Program Files 目录存在

REM 创建 n8n 安装目录
set N8N_PATH=D:\Program Files\n8n
if not exist "%N8N_PATH%" (
    mkdir "%N8N_PATH%"
    echo [信息] 创建目录: %N8N_PATH%
)

REM 使用 PowerShell 下载 n8n Windows 可执行文件
echo [信息] 正在从 GitHub 下载 n8n Windows 可执行文件...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/n8n-io/n8n/releases/latest/download/n8n-windows.exe' -OutFile '%N8N_PATH%\n8n.exe'"

if %errorlevel% == 0 (
    echo [成功] n8n 可执行文件下载完成
    
    REM 创建启动脚本
    echo @echo off > "%N8N_PATH%\start_n8n.bat"
    echo REM n8n 启动脚本 >> "%N8N_PATH%\start_n8n.bat"
    echo echo ======================================== >> "%N8N_PATH%\start_n8n.bat"
    echo echo           启动 n8n 服务 >> "%N8N_PATH%\start_n8n.bat"
    echo echo ======================================== >> "%N8N_PATH%\start_n8n.bat"
    echo echo. >> "%N8N_PATH%\start_n8n.bat"
    echo echo 请在浏览器中访问 http://localhost:5678 >> "%N8N_PATH%\start_n8n.bat"
    echo echo 按 Ctrl+C 停止服务 >> "%N8N_PATH%\start_n8n.bat"
    echo echo. >> "%N8N_PATH%\start_n8n.bat"
    echo "%N8N_PATH%\n8n.exe" >> "%N8N_PATH%\start_n8n.bat"
    echo echo. >> "%N8N_PATH%\start_n8n.bat"
    echo echo 服务已停止 >> "%N8N_PATH%\start_n8n.bat"
    echo pause >> "%N8N_PATH%\start_n8n.bat"
    
    echo [成功] 创建启动脚本: %N8N_PATH%\start_n8n.bat
    
    REM 创建配置目录
    set CONFIG_PATH=%USERPROFILE%\.n8n
    if not exist "%CONFIG_PATH%" (
        mkdir "%CONFIG_PATH%"
        echo [信息] 创建配置目录: %CONFIG_PATH%
    )
    
    echo.
    echo ========================================
    echo        n8n 安装完成!
    echo ========================================
    echo 可执行文件路径: %N8N_PATH%\n8n.exe
    echo 配置路径: %CONFIG_PATH%
    echo.
    echo 使用方法:
    echo 1. 双击 %N8N_PATH%\start_n8n.bat 启动 n8n
    echo 2. 在浏览器中访问 http://localhost:5678
    echo 3. 开始使用 n8n 创建自动化工作流
    echo.
    echo 文档参考: https://docs.n8n.io/
    echo ========================================
) else (
    echo [错误] 下载失败
    echo 请手动从 https://github.com/n8n-io/n8n/releases 下载 n8n Windows 版本
    echo 并将其放置在 %N8N_PATH% 目录中
)

pause