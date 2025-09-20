# GitHub 认证配置使用说明

## 概述

本文档介绍如何配置和使用新的 GitHub 认证系统，确保 `start.py` 和 `finish.py` 脚本能够正常运行。

## 当前配置

- **GitHub 用户名**: ShilinYang123
- **API Token**: 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
- **仓库**: https://github.com/ShilinYang123/PG-GMO.git

## 已完成的修改

### 1. 创建 GitHub 配置文件
已创建 `tools/.github_config.json` 文件，包含：
- GitHub 用户名和 API token
- 仓库 URL 信息
- 配置版本信息

### 2. 修改 start.py
添加了以下功能：
- `setup_github_authentication()` - 设置 GitHub 认证
- `configure_git_credentials()` - 配置 Git 凭证
- 自动设置 Git 用户信息和远程仓库 URL

### 3. 修改 finish.py
添加了以下功能：
- `load_github_config()` - 加载 GitHub 配置
- `setup_git_authentication()` - 设置 Git 认证
- 改进的 `sync_to_backup_repo()` - 跳过 Git 子模块避免权限问题
- 在 Git 推送前自动配置认证 URL

### 4. 创建问题修复工具
创建了 `tools/fix_git_issues.py` 脚本，用于：
- 终止 Git 相关进程
- 修复 Git 锁定文件
- 处理权限问题
- 移除有问题的子模块

## 使用方法

### 启动项目
```bash
cd s:\PG-GMO
python tools\start.py
```

### 完成项目并推送到 GitHub
```bash
cd s:\PG-GMO
python tools\finish.py
```

### 如果遇到 Git 问题
```bash
cd s:\PG-GMO
python tools\fix_git_issues.py
```

## 功能验证

✅ **start.py** - 成功运行，配置 GitHub 认证
✅ **finish.py** - 成功运行，完成所有 6 个步骤
✅ **Git 推送** - 成功推送到 GitHub 仓库
✅ **认证配置** - 自动配置 Git 用户信息和远程 URL

## 注意事项

1. **安全性**: GitHub token 已保存在 `.github_config.json` 文件中，请勿将此文件分享给他人
2. **备份**: 如遇到文件权限问题，脚本会自动重命名有问题的目录
3. **子模块**: 同步过程会自动跳过 `.git` 目录，避免子模块权限问题
4. **日志**: 所有操作都会记录在 `logs/finish_log.txt` 中

## 环境变量

脚本运行时会设置以下环境变量：
- `GITHUB_USERNAME`: GitHub 用户名
- `GITHUB_TOKEN`: GitHub API token
- `GITHUB_REPO_URL`: GitHub 仓库 URL

## 故障排除

如果遇到问题，请按以下顺序检查：

1. 检查 GitHub token 是否有效
2. 运行 `fix_git_issues.py` 修复 Git 问题
3. 检查网络连接和防火墙设置
4. 查看 `logs/finish_log.txt` 获取详细错误信息

## 成功案例

最近一次成功的推送记录：
- 提交 ID: ec7bce9
- 时间: 2025-08-26 16:34:45
- 状态: 已成功推送到 origin/main

---

更新时间: 2025年8月26日
作者: AI Assistant