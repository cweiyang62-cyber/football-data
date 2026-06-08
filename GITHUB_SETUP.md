# GitHub Actions 自动采集设置指南

## 步骤一：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`football-data` (或其他名称)
3. 选择 **Private** (私有) 或 **Public** (公开)
4. 点击 **Create repository**

## 步骤二：上传代码

```bash
# 在 football-data 目录下
cd C:\Users\Administrator\.openclaw\workspace\football-data

# 初始化 git
git init
git add .
git commit -m "Initial commit"

# 添加远程仓库 (替换为你的仓库地址)
git remote add origin https://github.com/你的用户名/football-data.git

# 推送
git branch -M main
git push -u origin main
```

## 步骤三：配置 API Key (Secrets)

1. 进入你的 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**，添加两个：

| Secret 名称 | 值 |
|:---|:---|
| `FD_API_KEY` | `c50e3649bded4ee09620aaf8c820a8ac` |
| `AF_API_KEY` | `270f70b7e6558bd77dc1fa7239fde118` |

## 步骤四：验证 Actions

1. 进入仓库 → **Actions** 标签
2. 你会看到 "Football Data Collection" workflow
3. 点击 **Run workflow** → **Run workflow** 手动测试

## 完成后

- ✅ 每6小时自动采集一次
- ✅ 数据保存在 `cache/` 目录
- ✅ 可在 Actions 日志查看采集结果
- ✅ 数据会自动推送到仓库

## 修改采集频率

编辑 `.github/workflows/collect.yml`：

```yaml
schedule:
  # 每6小时: '0 */6 * * *'
  # 每天凌晨2点: '0 2 * * *'
  # 每天早晚各一次: '0 8,20 * * *'
```

## 常见问题

### Q: 看不到数据更新？
检查 Actions 日志，看是否有错误。API Key 可能过期。

### Q: 达到 API 限制？
- Football-data: 无每日限制，但请求过快会限速
- API-Football 免费版: 100次/天

### Q: 如何停止自动采集？
删除 `.github/workflows/collect.yml` 或在 Actions 页面禁用 workflow。
