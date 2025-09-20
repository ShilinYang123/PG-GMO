@echo off
chcp 65001 >nul
echo ========================================
echo       MCP Server 管理脚本
echo ========================================
echo.
echo 请选择要执行的操作：
echo 1. 启动 Maigret MCP Server (OSINT工具)
echo 2. 启动 Shodan MCP Server (设备搜索)
echo 3. 启动 Apifox MCP Server (API文档)
echo 4. 启动 Bright Data MCP Server (Web爬取)
echo 5. 启动 MindsDB MCP Server (AI分析)
echo 6. 查看所有MCP Server状态
echo 7. 停止所有MCP Server
echo 8. 显示配置指南
echo 0. 退出
echo.
set /p choice=请输入选项 (0-8): 

if "%choice%"=="1" goto start_maigret
if "%choice%"=="2" goto start_shodan
if "%choice%"=="3" goto start_apifox
if "%choice%"=="4" goto start_bright_data
if "%choice%"=="5" goto start_mindsdb
if "%choice%"=="6" goto show_status
if "%choice%"=="7" goto stop_all
if "%choice%"=="8" goto show_guide
if "%choice%"=="0" goto exit
goto main

:start_maigret
echo.
echo 启动 Maigret MCP Server...
echo 注意：Maigret 不需要额外的API密钥
start "Maigret MCP" cmd /k "python -m maigret_mcp"
echo Maigret MCP Server 已在新窗口中启动
pause
goto main

:start_shodan
echo.
echo 启动 Shodan MCP Server...
echo 注意：需要设置 SHODAN_API_KEY 环境变量
set /p shodan_key=请输入 Shodan API Key (或按回车跳过): 
if not "%shodan_key%"=="" set SHODAN_API_KEY=%shodan_key%
cd /d "S:\PG-GMO\project\MCP\servers\shodan"
start "Shodan MCP" cmd /k "node build/index.js"
echo Shodan MCP Server 已在新窗口中启动
pause
goto main

:start_apifox
echo.
echo 启动 Apifox MCP Server...
echo 注意：需要提供项目ID或文档站点ID
set /p project_id=请输入 Apifox Project ID: 
if "%project_id%"=="" (
    echo 错误：必须提供项目ID
    pause
    goto main
)
cd /d "S:\PG-GMO\project\MCP\servers\apifox"
start "Apifox MCP" cmd /k "node dist/index.js --project-id %project_id%"
echo Apifox MCP Server 已在新窗口中启动
pause
goto main

:start_bright_data
echo.
echo 启动 Bright Data MCP Server...
echo 注意：需要设置 API_TOKEN 环境变量
set /p api_token=请输入 Bright Data API Token: 
if "%api_token%"=="" (
    echo 错误：必须提供API Token
    pause
    goto main
)
set API_TOKEN=%api_token%
start "Bright Data MCP" cmd /k "npx @brightdata/mcp"
echo Bright Data MCP Server 已在新窗口中启动
pause
goto main

:start_mindsdb
echo.
echo 启动 MindsDB MCP Server...
echo 注意：需要设置 MINDS_API_KEY 环境变量
set /p minds_key=请输入 Minds API Key (或按回车跳过): 
if not "%minds_key%"=="" set MINDS_API_KEY=%minds_key%
cd /d "S:\PG-GMO\project\MCP\servers\bright-data\mindsdb\minds-mcp"
start "MindsDB MCP" cmd /k "python server.py"
echo MindsDB MCP Server 已在新窗口中启动
pause
goto main

:show_status
echo.
echo ========================================
echo           MCP Server 状态检查
echo ========================================
echo.
echo 检查各MCP Server的安装状态...
echo.
echo 1. Maigret MCP Server:
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\Lib\site-packages\maigret_mcp" (
    echo    ✅ 已安装 (全局Python包)
) else (
    echo    ❌ 未找到安装
)
echo.
echo 2. Shodan MCP Server:
if exist "S:\PG-GMO\project\MCP\servers\shodan\build\index.js" (
    echo    ✅ 已安装 (源代码编译)
) else (
    echo    ❌ 未找到编译文件
)
echo.
echo 3. Apifox MCP Server:
if exist "S:\PG-GMO\project\MCP\servers\apifox\dist\index.js" (
    echo    ✅ 已安装 (源代码)
) else (
    echo    ❌ 未找到安装
)
echo.
echo 4. Bright Data MCP Server:
npx @brightdata/mcp --version >nul 2>&1
if %errorlevel%==0 (
    echo    ✅ 已安装 (全局npm包)
) else (
    echo    ❌ 未找到安装
)
echo.
echo 5. MindsDB MCP Server:
if exist "S:\PG-GMO\project\MCP\servers\bright-data\mindsdb\minds-mcp\server.py" (
    echo    ✅ 已安装 (源代码)
) else (
    echo    ❌ 未找到安装
)
echo.
pause
goto main

:stop_all
echo.
echo 停止所有MCP Server进程...
taskkill /f /im python.exe /fi "WINDOWTITLE eq Maigret MCP*" >nul 2>&1
taskkill /f /im node.exe /fi "WINDOWTITLE eq Shodan MCP*" >nul 2>&1
taskkill /f /im node.exe /fi "WINDOWTITLE eq Apifox MCP*" >nul 2>&1
taskkill /f /im node.exe /fi "WINDOWTITLE eq Bright Data MCP*" >nul 2>&1
taskkill /f /im python.exe /fi "WINDOWTITLE eq MindsDB MCP*" >nul 2>&1
echo 所有MCP Server进程已停止
pause
goto main

:show_guide
echo.
echo 打开配置指南文档...
start "" "S:\PG-GMO\project\MCP\MCP_Server_配置指南.md"
echo 配置指南已在默认编辑器中打开
pause
goto main

:exit
echo.
echo 感谢使用 MCP Server 管理脚本！
echo.
pause
exit

:main
cls
goto :eof