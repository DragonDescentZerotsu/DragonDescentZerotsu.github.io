#!/usr/bin/env python3
"""Push the homepage to both repositories and verify both live revisions."""

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = {
    "TianangLeng/tianangleng.github.io": "https://tianangleng.github.io/",
    "DragonDescentZerotsu/DragonDescentZerotsu.github.io":
        "https://dragondescentzerotsu.github.io/",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main():
    if git("branch", "--show-current") != "main":
        raise RuntimeError("请切换到 main 后发布。")
    if git("status", "--porcelain"):
        raise RuntimeError("请先检查并提交本地修改，再运行发布命令。")
    targets = git("remote", "get-url", "--push", "--all", "origin").splitlines()
    expected = {"https://github.com/" + repo + ".git" for repo in SITES}
    if set(targets) != expected or len(targets) != 2:
        raise RuntimeError("origin 双推送配置不匹配，请按 PUBLISHING.md 恢复。")

    commit = git("rev-parse", "HEAD")
    subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, check=True)
    print("两边推送完成，正在等待实际上线：" + commit, flush=True)
    pending = dict(SITES)
    deadline = time.monotonic() + 600
    while pending and time.monotonic() < deadline:
        for repo, base in list(pending.items()):
            try:
                with urllib.request.urlopen(
                    base + "deployment.json?commit=" + commit, timeout=15
                ) as response:
                    published = json.load(response)
                if published.get("commit") == commit and published.get("repository") == repo:
                    print("已验证上线：" + base, flush=True)
                    del pending[repo]
                    continue
            except (OSError, ValueError):
                pass  # The previous deployment may still be served during the build.

            # Fail promptly on a failed workflow; a successful push is not a deployment.
            runs = subprocess.run(
                ["gh", "run", "list", "--repo", repo, "--workflow", "pages.yml",
                 "--commit", commit, "--limit", "1", "--json", "status,conclusion,url"],
                text=True, capture_output=True, timeout=30,
            )
            if runs.returncode == 0:
                for run in json.loads(runs.stdout):
                    if run["status"] == "completed" and run["conclusion"] != "success":
                        raise RuntimeError("部署未成功：" + run["url"])
        if pending:
            time.sleep(10)
    if pending:
        raise RuntimeError("等待上线超时，尚未验证：" + ", ".join(pending.values()))
    print("发布成功：新旧地址均已上线同一提交。", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.SubprocessError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
