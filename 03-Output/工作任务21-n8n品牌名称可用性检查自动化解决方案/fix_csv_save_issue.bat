@echo off
chcp 65001 >nul
echo ===== n8n CSV文件保存问题修复脚本 =====
echo.

echo 1. 创建文件保存目录...
if not exist "C:\temp" mkdir "C:\temp"
if not exist "C:\temp\n8n-files" mkdir "C:\temp\n8n-files"
if not exist "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\results" mkdir "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\results"

echo   ✓ 目录创建完成
echo.

echo 2. 设置目录权限...
icacls "C:\temp" /grant Everyone:F /T /Q >nul 2>&1
icacls "C:\temp\n8n-files" /grant Everyone:F /T /Q >nul 2>&1
icacls "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\results" /grant Everyone:F /T /Q >nul 2>&1

echo   ✓ 权限设置完成
echo.

echo 3. 创建测试文件验证权限...
echo name,domainAvailable,youtubeAvailable,checkTime > "C:\temp\test.csv"
echo TestBrand,true,false,2024-01-16T10:30:00.000Z >> "C:\temp\test.csv"
if exist "C:\temp\test.csv" (
    del "C:\temp\test.csv"
    echo   ✓ C:\temp 写入权限正常
) else (
    echo   ✗ C:\temp 写入权限异常
)

echo name,domainAvailable,youtubeAvailable,checkTime > "C:\temp\n8n-files\test.csv"
echo TestBrand,true,false,2024-01-16T10:30:00.000Z >> "C:\temp\n8n-files\test.csv"
if exist "C:\temp\n8n-files\test.csv" (
    del "C:\temp\n8n-files\test.csv"
    echo   ✓ C:\temp\n8n-files 写入权限正常
) else (
    echo   ✗ C:\temp\n8n-files 写入权限异常
)
echo.

echo 4. 生成配置建议文件...
echo # n8n文件保存配置建议 > "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo # 生成时间: %date% %time% >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo. >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo ## 推荐的文件保存路径 >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo 1. C:\\temp\\n8n-files\\{{ $json.fileName }} >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo 2. C:\\temp\\{{ $json.fileName }} >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo 3. S:\\PG-GMO\\03-Output\\工作任务21-n8n品牌名称可用性检查自动化解决方案\\results\\{{ $json.fileName }} >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo. >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo ## 故障排除 >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo - 确保目录存在且有写入权限 >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo - 检查文件名不包含非法字符 >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo - 验证n8n服务正在运行 >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"
echo - 查看n8n控制台日志获取详细错误信息 >> "S:\PG-GMO\03-Output\工作任务21-n8n品牌名称可用性检查自动化解决方案\n8n_config_recommendations.txt"

echo   ✓ 配置建议已保存
echo.

echo ===== 修复完成 =====
echo.
echo 下一步操作:
echo 1. 在n8n中打开工作流
echo 2. 编辑'保存文件到磁盘'节点
echo 3. 将fileName参数改为推荐路径之一:
echo    - C:\\temp\\n8n-files\\{{ $json.fileName }}
echo    - C:\\temp\\{{ $json.fileName }}
echo 4. 保存并重新执行工作流
echo 5. 检查指定目录是否生成CSV文件
echo.
echo 如果问题仍然存在，请查看生成的配置建议文件获取更多帮助。
echo.
pause