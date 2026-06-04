# Git 与版本控制基础

## Git 是什么?为什么要学?
代码版本管理工具,能记录每次修改、回退、协作。配合 GitHub 还能展示作品集,
是技术人求职的基本素养。

## 最常用的命令?
```
git init                 # 初始化仓库
git add .                # 暂存所有改动
git commit -m "说明"     # 提交
git status               # 看当前状态
git log --oneline        # 看提交历史
```

## 怎么推送到 GitHub?
```
git remote add origin https://github.com/用户名/仓库名.git
git push -u origin main
```
首次推送会要求登录授权(浏览器或令牌)。

## .gitignore 是干什么的?
列出"不提交"的文件,比如:
```
.env            # 密钥绝不提交!
__pycache__/
*.log
```
**API Key、密码等敏感信息一定要用 .env 管理并写进 .gitignore。**

## 不小心提交了密钥怎么办?
立刻去对应平台**重置/删除该密钥**(历史里仍有记录),再把它加入 .gitignore。

## commit 信息怎么写?
简洁说明这次改了什么,如 "feat: 新增爬虫数据存储模块"。清晰的提交记录方便回顾和协作。

## 作品集怎么用 Git?
每个项目一个仓库,持续提交,写好 README。绿色贡献格子也能体现你的活跃度。
