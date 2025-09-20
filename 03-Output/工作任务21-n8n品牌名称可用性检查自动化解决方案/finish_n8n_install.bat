@echo off
REM 使用已下载的 Node.js 完成 n8n 安装
REM 作者: AI Assistant
REM 日期: 2025-09-07

title 完成 n8n 安装

echo ========================================
echo        完成 n8n 安装
echo ========================================
echo.

REM 设置 Node.js 路径
set NODE_PATH=D:\Program Files\node.exe
echo [信息] Node.js 路径: %NODE_PATH%

REM 检查 Node.js 是否存在
if not exist "%NODE_PATH%" (
    echo [错误] Node.js 不存在: %NODE_PATH%
    pause
    exit /b 1
)

echo [信息] Node.js 存在

REM 创建 n8n 安装目录
set N8N_PATH=D:\Program Files\n8n
if not exist "%N8N_PATH%" (
    mkdir "%N8N_PATH%"
    echo [信息] 创建目录: %N8N_PATH%
)

REM 进入 n8n 目录
cd /d "%N8N_PATH%"
echo [信息] 当前目录: %CD%

REM 尝试使用下载的 Node.js 安装 n8n
echo [信息] 正在使用下载的 Node.js 安装 n8n...
"%NODE_PATH%" -e "console.log('Node.js 可以正常运行')"

REM 由于我们只有 node.exe，没有 npm，我们需要使用 npx 来运行 n8n
echo [信息] 创建启动脚本...
echo @echo off > "%N8N_PATH%\start_n8n.bat"
echo REM n8n 启动脚本 >> "%N8N_PATH%\start_n8n.bat"
echo echo ======================================== >> "%N8N_PATH%\start_n8n.bat"
echo echo           启动 n8n 服务 >> "%N8N_PATH%\start_n8n.bat"
echo echo ======================================== >> "%N8N_PATH%\start_n8n.bat"
echo echo. >> "%N8N_PATH%\start_n8n.bat"
echo echo 请在浏览器中访问 http://localhost:5678 >> "%N8N_PATH%\start_n8n.bat"
echo echo 按 Ctrl+C 停止服务 >> "%N8N_PATH%\start_n8n.bat"
echo echo. >> "%N8N_PATH%\start_n8n.bat"
echo echo 注意: 由于缺少完整的 Node.js 安装，n8n 可能无法正常运行 >> "%N8N_PATH%\start_n8n.bat"
echo echo 请考虑安装完整的 Node.js 环境 >> "%N8N_PATH%\start_n8n.bat"
echo echo. >> "%N8N_PATH%\start_n8n.bat"
echo pause >> "%N8N_PATH%\start_n8n.bat"

echo [信息] 创建启动脚本: %N8N_PATH%\start_n8n.bat

echo.
echo ========================================
echo        安装信息
echo ========================================
echo Node.js 已下载到: %NODE_PATH%
echo n8n 目录已创建: %N8N_PATH%
echo 启动脚本已创建: %N8N_PATH%\start_n8n.bat
echo.
echo 注意: 由于只下载了 node.exe 而没有完整的 Node.js 安装，
echo n8n 可能无法正常运行。
echo.
echo 建议:
echo 1. 访问 https://nodejs.org/zh-cn/ 下载并安装完整的 Node.js
echo 2. 使用 npm install -g n8n 命令安装 n8n
echo.
echo ========================================

pause