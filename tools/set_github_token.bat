@echo off
REM 设置GitHub令牌环境变量
REM 使用方法: set_github_token.bat [令牌值]

if "%1"=="" (
    echo 用法: set_github_token.bat [GitHub令牌]
    echo 示例: set_github_token.bat YOUR_GITHUB_TOKEN_HERE
    pause
    exit /b 1
)

set GITHUB_TOKEN=%1
echo 已设置GitHub令牌环境变量
echo 令牌前缀: %GITHUB_TOKEN:~0,10%******
echo.
echo 要在当前会话中使用此令牌，请运行:
echo set GITHUB_TOKEN=%1
echo.
pause