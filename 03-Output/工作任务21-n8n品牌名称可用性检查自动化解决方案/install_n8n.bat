@echo off
REM n8n 安装脚本
REM 作者: AI Assistant
REM 日期: 2025-09-07

title n8n 安装程序

echo ========================================
echo        n8n 自动安装程序
echo ========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [信息] 已获得管理员权限
) else (
    echo [警告] 建议以管理员身份运行此脚本
    echo.
)

REM 检查 D:\Program Files 目录
if exist "D:\Program Files" (
    echo [信息] D:\Program Files 目录存在
) else (
    echo [错误] D:\Program Files 目录不存在
    echo 请确保 D:\Program Files 目录存在后再运行此脚本
    pause
    exit /b 1
)

REM 创建 n8n 安装目录
set N8N_PATH=D:\Program Files\n8n
if not exist "%N8N_PATH%" (
    mkdir "%N8N_PATH%"
    echo [信息] 创建目录: %N8N_PATH%
)

echo.
echo 正在检查 Node.js 环境...

REM 检查 Node.js
node --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo [信息] Node.js 已安装: %NODE_VERSION%
) else (
    echo [错误] Node.js 未安装
    echo 请先访问 https://nodejs.org/zh-cn/ 下载并安装 Node.js LTS 版本
    echo 然后重新运行此脚本
    pause
    exit /b 1
)

REM 检查 npm
npm --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
    echo [信息] npm 已安装: %NPM_VERSION%
) else (
    echo [错误] npm 未安装
    pause
    exit /b 1
)

echo.
echo 正在设置 npm 全局路径...
npm config set prefix "%N8N_PATH%"

echo.
echo 正在安装 n8n...
echo 这可能需要几分钟时间，请耐心等待...

npm install -g n8n
if %errorlevel% == 0 (
    echo [成功] n8n 安装完成
) else (
    echo [错误] n8n 安装失败
    pause
    exit /b 1
)

echo.
echo 正在创建启动脚本...

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
echo node "%N8N_PATH%\node_modules\n8n\bin\n8n" >> "%N8N_PATH%\start_n8n.bat"
echo echo. >> "%N8N_PATH%\start_n8n.bat"
echo echo 服务已停止 >> "%N8N_PATH%\start_n8n.bat"
echo pause >> "%N8N_PATH%\start_n8n.bat"

echo [信息] 创建启动脚本: %N8N_PATH%\start_n8n.bat

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