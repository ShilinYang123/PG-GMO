@echo off
echo 启动项目合规性监控系统...
cd /d "s:\PG-GMO"
python "s:\PG-GMO\tools\compliance_monitor.py" --start
pause
