@echo off
echo 正在将工作任务17转换为HTML并打开...
cd /d %~dp0
python md_to_html.py "..\03-WorkTask\任务清单\工作任务17-全球首个世界一致性模型AI视频评估.md"
pause