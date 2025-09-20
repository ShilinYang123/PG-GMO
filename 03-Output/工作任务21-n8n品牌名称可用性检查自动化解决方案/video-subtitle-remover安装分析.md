# Video Subtitle Remover (VSR) 安装分析报告

## 软件概述
Video-subtitle-remover (VSR) 是一款基于AI技术的视频硬字幕去除软件，支持：
- 自定义字幕位置移除
- 自动检测并移除整个视频中的所有文本
- 批量处理图片水印文字移除

## 系统要求
### 基础要求
- **Python版本**: Python 3.12+ （必需）
- **操作系统**: Windows/Linux
- **显卡支持**: 
  - NVIDIA显卡（推荐，支持CUDA加速）
  - AMD/Intel显卡（支持DirectML加速）
  - CPU模式（无GPU也可运行）

### 硬件加速支持
- **NVIDIA显卡**:
  - 10/20/30系列: CUDA 11.8
  - 40系列: CUDA 12.6
  - 50系列: CUDA 12.8
- **AMD/Intel显卡**: DirectML支持

## 安装方式

### 方式1: 直接下载（推荐新手）
1. 从GitHub Releases页面下载.zip包
2. 解压后直接运行
3. 如无法运行，按方式2安装

### 方式2: 源码安装
```bash
# 1. 克隆仓库
git clone https://github.com/YaoFANGUK/video-subtitle-remover.git
cd video-subtitle-remover

# 2. 创建虚拟环境（推荐）
python -m venv vsr_env
vsr_env\Scripts\activate  # Windows
# source vsr_env/bin/activate  # Linux

# 3. 安装依赖
pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
pip install -r requirements.txt

# 4. 根据显卡类型安装额外依赖
# DirectML (AMD/Intel显卡):
pip install -r requirements_directml.txt
# 或者
pip install torch_directml==0.2.5.dev240914
```

### 方式3: Docker安装
```bash
# NVIDIA 10/20/30系显卡
docker run -it --name vsr --gpus all eritpchy/video-subtitle-remover:1.1.1-cuda11.8

# NVIDIA 40系显卡
docker run -it --name vsr --gpus all eritpchy/video-subtitle-remover:1.1.1-cuda12.6

# NVIDIA 50系显卡
docker run -it --name vsr --gpus all eritpchy/video-subtitle-remover:1.1.1-cuda12.8

# AMD/Intel显卡
docker run -it --name vsr --gpus all eritpchy/video-subtitle-remover:1.1.1-directml
```

## 当前环境兼容性分析

### ✅ 可以安装的理由
1. **Python支持**: Windows系统可以安装Python 3.12+
2. **无GPU要求**: 软件支持CPU模式运行
3. **依赖管理**: 使用pip安装，依赖管理相对简单
4. **多种安装方式**: 提供直接下载、源码安装、Docker等多种选择

### ⚠️ 需要注意的问题
1. **Python版本**: 需要确保安装Python 3.12或更高版本
2. **虚拟环境**: 强烈建议使用虚拟环境避免依赖冲突
3. **网络访问**: 需要访问GitHub和Python包索引
4. **存储空间**: AI模型文件可能较大，需要足够存储空间

## 推荐安装步骤

### 第一步: 检查Python版本
```cmd
python --version
```
如果版本低于3.12，需要先升级Python。

### 第二步: 尝试直接下载方式
1. 访问: https://github.com/YaoFANGUK/video-subtitle-remover/releases
2. 下载最新版本的.zip文件
3. 解压到合适位置
4. 运行主程序

### 第三步: 如直接运行失败，使用源码安装
按照上述"方式2"的步骤进行安装。

## 结论
**可以安装**。这个软件设计良好，提供了多种安装方式，对硬件要求不高（支持CPU模式），主要需要确保Python版本符合要求。建议先尝试直接下载方式，如有问题再使用源码安装。

## 相关链接
- 项目主页: https://github.com/YaoFANGUK/video-subtitle-remover
- 英文文档: https://github.com/YaoFANGUK/video-subtitle-remover/blob/main/README_en.md
- 发布页面: https://github.com/YaoFANGUK/video-subtitle-remover/releases

---
*分析时间: 2025年1月16日*
*分析基于: GitHub搜索结果和项目文档*