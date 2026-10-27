# 主页发布

主站：https://tianangleng.github.io/
旧站：https://dragondescentzerotsu.github.io/
PepLink：https://tianangleng.github.io/peptide_to_smiles/

两个主页仓库发布相同的 main 分支和文件。旧域名访问主页时通过 JavaScript 跳到新主站，并保留查询参数和锚点；关闭 JavaScript 时仍能看到最新页面，canonical 指向新主站。旧 PDF、图片、视频等资源持续同步。

## 日常更新

在此本地目录修改并提交后执行：

```sh
python3 scripts/publish.py
```

本目录的 origin 已配置两个 push URL，会依次推送新、旧仓库。上述脚本先推送，再检查两个站点的 deployment.json，只有它们均显示当前提交时才报告发布成功；工作流失败或等待超过 10 分钟会报错。需要本机已安装并登录 GitHub CLI（gh）。

也可以直接运行 `git push origin main`，但它只确认 Git 推送，不确认网页上线。双推送不是跨仓库的原子事务；一边失败时解决错误再重试，不要强制推送。

直接在 GitHub 网页上修改某一个仓库、显式推送到 legacy，或从未配置的新克隆推送，不会自动同步另一边。请集中从本目录发布。

## 新克隆恢复双推送

确认 origin 的抓取地址为 TianangLeng/tianangleng.github.io 后运行：

```sh
git config --local --replace-all remote.origin.pushurl https://github.com/TianangLeng/tianangleng.github.io.git
git config --local --add remote.origin.pushurl https://github.com/DragonDescentZerotsu/DragonDescentZerotsu.github.io.git
git remote get-url --push --all origin
```

保留两个仓库及其 Pages 设置（Source: GitHub Actions）。`.github/workflows/pages.yml` 只发布 main 分支，保留原 Jekyll 构建，部署前校验关键文件，并通过 `concurrency: pages`、`cancel-in-progress: false` 让部署依次完成。不要同时开启旧式分支发布。PepLink 是独立的网站仓库，在本机 Published_packages/PepLink_Page 目录维护；它也配置了新旧双推送。

## 验证与排错

- 两个站点的 `/deployment.json` 分别记录仓库和当前已发布提交，不影响网页显示。
- GitHub Actions 的 `Publish homepage` 工作流必须成功；历史失败记录不会因新部署成功而消失。
- 失败通知来自 GitHub Actions，Google Search Console 的开通邮件是使用指南。无需为了修复部署而关闭通知。
- 旧入口跳转、历史资源路径、PepLink 独立项目站点继续保留。
