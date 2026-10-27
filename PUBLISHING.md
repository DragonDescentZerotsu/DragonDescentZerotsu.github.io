# 主页发布

主站：https://tianangleng.github.io/
旧站：https://dragondescentzerotsu.github.io/
PepLink：https://tianangleng.github.io/peptide_to_smiles/

两个主页仓库发布相同的 main 分支和文件。旧域名访问主页时通过 JavaScript 跳到新主站，并保留查询参数和锚点；关闭 JavaScript 时仍能看到最新页面，canonical 指向新主站。旧 PDF、图片、视频等资源持续同步。

## 日常更新

在此本地目录修改并提交后执行：

```sh
git push origin main
```

本目录的 origin 已配置两个 push URL，会依次推送新、旧仓库。必须检查两次推送都成功；它不是跨仓库的原子事务。一边失败时解决错误再重试，不要强制推送。

直接在 GitHub 网页上修改某一个仓库、显式推送到 legacy，或从未配置的新克隆推送，不会自动同步另一边。请集中从本目录发布。

## 新克隆恢复双推送

确认 origin 的抓取地址为 TianangLeng/tianangleng.github.io 后运行：

```sh
git config --local --replace-all remote.origin.pushurl https://github.com/TianangLeng/tianangleng.github.io.git
git config --local --add remote.origin.pushurl https://github.com/DragonDescentZerotsu/DragonDescentZerotsu.github.io.git
git remote get-url --push --all origin
```

保留两个仓库及其 Pages 设置（main，根目录）。PepLink 是独立的网站仓库，在本机 Published_packages/PepLink_Page 目录维护；它也配置了新旧双推送。

## 搜索站点地图

`sitemap.xml` 与 `sitemap.txt` 列出同一组规范网址；新增页面时同时更新。纯文本版本用于提供独立的抓取入口，Google 官方支持这种格式。Search Console 的实时检测已成功抓取 XML，但提交报告此前仍显示无法抓取，不能据此断言 XML 格式有错。
