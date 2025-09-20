# n8n 手动安装步骤

## 概述
由于自动化安装遇到问题，以下是手动安装 n8n 的详细步骤。

## 步骤 1: 安装 Node.js

1. 打开浏览器，访问 https://nodejs.org/zh-cn/
2. 下载 LTS 版本的 Node.js Windows 安装程序 (通常是 .msi 文件)
3. 运行下载的安装程序
4. 按照安装向导的指示完成安装
5. 重启计算机以确保环境变量生效

## 步骤 2: 验证 Node.js 安装

1. 按 `Win + R` 打开运行对话框
2. 输入 `cmd` 并按回车打开命令提示符
3. 在命令提示符中输入以下命令并按回车:
   ```
   node --version
   ```
4. 如果显示版本号，说明 Node.js 安装成功
5. 同样验证 npm 是否安装:
   ```
   npm --version
   ```

## 步骤 3: 安装 n8n

1. 在命令提示符中输入以下命令来全局安装 n8n:
   ```
   npm install -g n8n
   ```
2. 等待安装完成（这可能需要几分钟时间）

## 步骤 4: 配置安装路径

如果您希望将 n8n 安装到 D:\Program Files 目录:

1. 创建目录:
   ```
   mkdir "D:\Program Files\n8n"
   ```

2. 设置 npm 全局安装路径:
   ```
   npm config set prefix "D:\Program Files\n8n"
   ```

3. 重新安装 n8n:
   ```
   npm install -g n8n
   ```

## 步骤 5: 启动 n8n

### 方法一: 直接启动
在命令提示符中输入:
```
n8n
```

### 方法二: 指定路径启动
如果 n8n 不在系统 PATH 中:
```
cd /d "D:\Program Files\n8n"
node node_modules\n8n\bin\n8n
```

### 方法三: 创建启动脚本
创建一个批处理文件 `start_n8n.bat`，内容如下:
```batch
@echo off
echo 启动 n8n...
echo 请在浏览器中访问 http://localhost:5678
echo 按 Ctrl+C 停止服务
echo.
node "D:\Program Files\n8n\node_modules\n8n\bin\n8n"
pause
```

## 步骤 6: 访问 n8n 界面

1. 打开浏览器
2. 访问 http://localhost:5678
3. 如果是首次访问，系统会要求您创建账户

## 故障排除

### 1. 权限问题
以管理员身份运行命令提示符。

### 2. 路径问题
确保所有路径都用双引号括起来，特别是包含空格的路径。

### 3. 端口冲突
如果 5678 端口被占用，可以使用其他端口启动:
```
n8n --port 3000
```

### 4. 网络问题
如果 npm 安装失败，可能是网络问题。可以尝试:
```
npm config set registry https://registry.npm.taobao.org
```
然后再安装 n8n。

## 配置

### 1. 环境变量
n8n 支持多种环境变量配置，可以在系统环境变量中设置:
- `N8N_PORT`: 端口号
- `N8N_PROTOCOL`: 协议 (http 或 https)
- `N8N_HOST`: 主机地址
- `N8N_ENCRYPTION_KEY`: 加密密钥

### 2. 配置文件
n8n 的配置文件位于:
```
%USERPROFILE%\.n8n\
```

## 升级和维护

### 1. 升级 n8n
```
npm update -g n8n
```

### 2. 卸载 n8n
```
npm uninstall -g n8n
```

## 支持资源

- 官方文档: https://docs.n8n.io/
- GitHub 仓库: https://github.com/n8n-io/n8n
- 社区论坛: https://community.n8n.io/

## 联系信息

如有问题，请参考官方文档或联系技术支持。