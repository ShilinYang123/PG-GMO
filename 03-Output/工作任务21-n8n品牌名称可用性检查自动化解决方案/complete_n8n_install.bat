@echo off
REM 完整的 n8n 安装脚本
REM 作者: AI Assistant
REM 日期: 2025-09-07

title n8n 完整安装程序

echo ========================================
echo        n8n 完整安装程序
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

REM 检查 Node.js 是否已下载
if not exist "D:\Program Files\node.exe" (
    echo [错误] Node.js 未下载到 D:\Program Files
    echo 请先下载 Node.js 到 D:\Program Files
    pause
    exit /b 1
)

echo [信息] Node.js 已存在: D:\Program Files\node.exe

REM 将 Node.js 目录添加到 PATH
set PATH=%PATH%;D:\Program Files

REM 尝试安装 n8n
echo.
echo [信息] 正在安装 n8n...
cd /d "%N8N_PATH%"

REM 使用 Node.js 直接安装 n8n
echo [信息] 使用 npm 安装 n8n...
call npm install n8n

if %errorlevel% == 0 (
    echo [成功] n8n 安装完成
) else (
    echo [警告] npm 安装失败，尝试其他方法...
    
    REM 尝试使用 npx 运行 n8n
    echo [信息] 尝试使用 npx 运行 n8n...
    call npx n8n --version >nul 2>&1
    if %errorlevel% == 0 (
        echo [成功] n8n 可以通过 npx 运行
        echo [信息] 创建 npx 启动脚本...
        
        echo @echo off > "%N8N_PATH%\start_n8n.bat"
        echo REM n8n 启动脚本 >> "%N8N_PATH%\start_n8n.bat"
        echo echo ======================================== >> "%N8N_PATH%\start_n8n.bat"
        echo echo           启动 n8n 服务 >> "%N8N_PATH%\start_n8n.bat"
        echo echo ======================================== >> "%N8N_PATH%\start_n8n.bat"
        echo echo. >> "%N8N_PATH%\start_n8n.bat"
        echo echo 请在浏览器中访问 http://localhost:5678 >> "%N8N_PATH%\start_n8n.bat"
        echo echo 按 Ctrl+C 停止服务 >> "%N8N_PATH%\start_n8n.bat"
        echo echo. >> "%N8N_PATH%\start_n8n.bat"
        echo npx n8n >> "%N8N_PATH%\start_n8n.bat"
        echo echo. >> "%N8N_PATH%\start_n8n.bat"
        echo echo 服务已停止 >> "%N8N_PATH%\start_n8n.bat"
        echo pause >> "%N8N_PATH%\start_n8n.bat"
        
        echo [成功] 创建启动脚本: %N8N_PATH%\start_n8n.bat
    ) else (
        echo [错误] 无法安装或运行 n8n
        echo 尝试手动下载 n8n Windows 版本
        pause
        exit /b 1
    )
)

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
echo 安装路径: %N8N_PATH%
echo 配置路径: %CONFIG_PATH%
echo.
echo 使用方法:
echo 1. 双击 %N8N_PATH%\start_n8n.bat 启动 n8n
echo 2. 在浏览器中访问 http://localhost:5678
echo 3. 开始使用 n8n 创建自动化工作流
echo.
echo 文档参考: https://docs.n8n.io/
echo ========================================

pause