@echo off
chcp 65001 >nul
echo 高效办公助手系统快速完成脚本（禁用虚拟环境）
echo ================================================

:: 设置环境变量禁用虚拟环境
set VIRTUAL_ENV=
set CONDA_DEFAULT_ENV=
set CONDA_PREFIX=

:: 使用系统Python执行快速完成脚本
echo 使用系统Python执行快速完成脚本...
python "%~dp0finish_fast.py" %*

echo.
echo 执行完成，按任意键退出...
pause >nul