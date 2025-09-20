# 自动化品牌名称可用性检查器 - 输出结果说明

## 输出文件格式

检查结果将保存为 CSV 格式文件，包含以下列：

| 列名 | 说明 |
|------|------|
| name | 品牌名称前缀 |
| com_domain | 完整的 .com 域名 |
| domain_available | 域名可用性状态 (✅ 可用 / ❌ 已注册) |
| youtube_handle | YouTube 用户名 (@username) |
| youtube_available | YouTube 用户名可用性状态 (✅ 可用 / ❌ 已占用) |
| instagram_handle | Instagram 用户名 (@username) |
| instagram_available | Instagram 用户名可用性状态 (✅ 可用 / ❌ 已占用) |
| facebook_handle | Facebook 用户名 |
| facebook_available | Facebook 用户名可用性状态 (✅ 可用 / ❌ 已占用) |
| tiktok_handle | TikTok 用户名 (@username) |
| tiktok_available | TikTok 用户名可用性状态 (✅ 可用 / ❌ 已占用) |

## 状态标识说明

- ✅ 可用/可用: 表示该名称在对应平台上可以使用
- ❌ 已注册/已占用: 表示该名称在对应平台上已被使用

## 示例数据

```
name,com_domain,domain_available,youtube_handle,youtube_available,instagram_handle,instagram_available,facebook_handle,facebook_available,tiktok_handle,tiktok_available
HQPro,hqpro.com,✅,@hqpro,❌,@hqpro,✅,hqpro,✅,@hqpro,✅
PrimeAppliance,primeappliance.com,❌,@primeappliance,✅,@primeappliance,❌,primeappliance,✅,@primeappliance,✅
```

## 文件位置

- 模板文件: `brand_availability_results_template.csv`
- 实际结果文件: 将在此目录下生成带时间戳的结果文件，例如 `brand_availability_results_20250915_153000.csv`