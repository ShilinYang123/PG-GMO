# 项目合规性监控启动脚本
Write-Host "启动项目合规性监控系统..." -ForegroundColor Green
Set-Location "s:\PG-GMO"
python "s:\PG-GMO\tools\compliance_monitor.py" --start
Read-Host "按任意键退出"
