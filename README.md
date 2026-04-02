# Care Page

一个可直接部署到 Vercel 的静态网页，用来表达你对张威最近身体不舒服时的关心。

## 当前结构

- `index.html`：页面内容
- `styles.css`：视觉样式
- `script.js`：轻交互
- `vercel.json`：Vercel 静态部署配置
- `.github/workflows/deploy-aliyun-oss.yml`：GitHub Actions 自动同步到阿里云 OSS
- `scripts/sync_oss.py`：同步脚本

## 本地预览

如果本机有 Python：

```powershell
cd E:\codex\third
python -m http.server 4173
```

然后访问 `http://127.0.0.1:4173`

## 部署到 Vercel

Vercel 后台导入仓库时：

1. Framework Preset 选择 `Other`
2. Build Command 留空
3. Output Directory 留空

如果你想用 CLI：

```powershell
cd E:\codex\third
vercel.cmd
vercel.cmd --prod
```

## GitHub Actions 同步到阿里云 OSS

这个项目已经带了自动同步工作流：

- 文件：`.github/workflows/deploy-aliyun-oss.yml`
- 触发方式：
  - 推送到 `main`
  - 推送到 `master`
  - GitHub Actions 手动执行

### 需要在 GitHub 仓库里设置的 Secrets

在仓库的 `Settings -> Secrets and variables -> Actions` 里添加：

- `ALIYUN_OSS_ACCESS_KEY_ID`
- `ALIYUN_OSS_ACCESS_KEY_SECRET`
- `ALIYUN_OSS_BUCKET`
- `ALIYUN_OSS_ENDPOINT`

可选：

- `ALIYUN_OSS_PREFIX`
  - 例如 `care-page`
  - 不填就上传到 Bucket 根目录

- `ALIYUN_OSS_DELETE_EXTRA`
  - 填 `true` 时，会删除 OSS 上这个前缀下多余的旧文件
  - 默认不删除，更安全

### 推荐配置示例

- `ALIYUN_OSS_BUCKET`: `your-bucket-name`
- `ALIYUN_OSS_ENDPOINT`: `https://oss-cn-hangzhou.aliyuncs.com`
- `ALIYUN_OSS_PREFIX`: `zhangwei-care`
- `ALIYUN_OSS_DELETE_EXTRA`: `true`

### 同步规则

会上传站点文件，比如：

- `index.html`
- `styles.css`
- `script.js`
- 未来新增的图片、字体、子目录静态资源

不会上传这些：

- `.github`
- `.vercel`
- `scripts`
- `README.md`
- `.gitignore`
- `vercel.json`

## 已验证

- 页面本地静态访问正常
- Vercel 生产部署已成功
- Vercel 项目已绑定
- GitHub Actions 工作流文件已创建

## 后续升级到 Next.js

后续如果要升级：

- 首页迁移到 `app/page.tsx`
- 样式迁移到 `app/globals.css`
- 当前交互迁移为一个小型 `use client` 组件

这次先保持静态站，方便你最快上线和同步镜像。
