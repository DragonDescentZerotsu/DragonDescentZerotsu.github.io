# 主页发布

主站：https://tianangleng.github.io/
旧站：https://dragondescentzerotsu.github.io/
PepLink：https://tianangleng.github.io/peptide_to_smiles/

两个主页仓库发布相同的 main 分支。旧主页通过 JavaScript 跳到新主站，保留查询参数和锚点；关闭 JavaScript 时仍显示最新页面，canonical 指向新主站。旧 PDF、图片、视频等资源持续同步，保留历史路径。

## 日常更新

需要 Python 3 和已登录的 GitHub CLI（`gh`）。在本目录检查并提交修改后运行：

```sh
python3 scripts/publish.py
```

脚本通过 origin 的两个 push URL 推送，再检查两站的 `deployment.json`。只有两站均上线当前提交才报告成功；工作流失败或等待超过 10 分钟会报错。一边失败时排错后重试，不要强制推送。

直接 `git push origin main` 不检查实际上线；GitHub 网页编辑、仅推送 legacy 或未配置的新克隆不会同步两边。PepLink 独立维护于本机 `Published_packages/PepLink_Page`，已配置双推送，不由主页脚本发布。

## 新克隆恢复配置

确认 origin 抓取地址为 `TianangLeng/tianangleng.github.io` 后执行：

```sh
git config --local --replace-all remote.origin.pushurl https://github.com/TianangLeng/tianangleng.github.io.git
git config --local --add remote.origin.pushurl https://github.com/DragonDescentZerotsu/DragonDescentZerotsu.github.io.git
git remote get-url --push --all origin
```

## 部署与排错

保留两个仓库，Pages Source 均设为 **GitHub Actions**。唯一工作流 `.github/workflows/pages.yml` 使用原 Jekyll 构建、检查关键文件并串行部署；不要切回旧式分支发布。

失败时检查当前提交的 **Publish homepage** 运行记录。手动重发用 Actions → Publish homepage → Run workflow（main），两仓库须分别操作并核对各站 `deployment.json`；不要重跑旧的 `pages build and deployment` 历史任务。
