# 推送到 GitHub（新建仓库）操作备忘

在 **`week10` 项目根目录**（含 `app.py`、`requirements.txt` 的目录）执行。

## 1. 初始化并提交（仅此文件夹作为独立仓库）

```bash
cd /path/to/week10
git init
git branch -M main
git add .
git status   # 确认未出现 实验报告.md、image/、.hf_cache/
git commit -m "Initial commit: Week10 sentiment dashboard"
```

若误加入了应忽略的文件：

```bash
git rm -r --cached .hf_cache 2>/dev/null
git rm --cached 实验报告.md 2>/dev/null
git rm -r --cached image 2>/dev/null
git commit -m "Stop tracking local-only files"
```

## 2. 在 GitHub 网页新建空仓库

GitHub → New repository → **不要**勾选 “Add a README”（本地已有则避免冲突）。

记下远程地址，例如：

`https://github.com/<你的用户名>/<仓库名>.git`

## 3. 关联远程并推送

```bash
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

若使用 SSH：

```bash
git remote add origin git@github.com:<你的用户名>/<仓库名>.git
git push -u origin main
```

## 4.（可选）GitHub CLI

```bash
gh repo create <仓库名> --private --source=. --remote=origin --push
```

---

推送前请再次确认：**实验报告、截图目录、模型缓存不在提交列表中**。详见仓库根目录 `请勿上传到Git仓库的本地文件说明.md`。
