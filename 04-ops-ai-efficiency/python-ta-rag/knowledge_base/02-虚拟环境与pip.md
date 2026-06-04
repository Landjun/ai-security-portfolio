# 虚拟环境与 pip 包管理

## pip 是什么?怎么装第三方库?
pip 是 Python 的包管理工具。安装库用:
```
pip install 库名
```
例如 `pip install requests`。卸载用 `pip uninstall 库名`,查看已装用 `pip list`。

## 安装太慢或失败怎么办?
多半是网络问题,换国内镜像源:
```
pip install 库名 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 虚拟环境是什么?为什么要用?
虚拟环境是一个独立的 Python 运行环境,让不同项目的依赖互不干扰,避免版本冲突。
创建并激活:
```
python -m venv .venv          # 创建,目录名 .venv
.venv\Scripts\activate        # Windows 激活
source .venv/bin/activate     # Mac/Linux 激活
```
激活后命令行前面会出现 (.venv),此时 pip install 只装到这个环境里。退出用 deactivate。

## requirements.txt 怎么用?
导出当前依赖:`pip freeze > requirements.txt`;
按清单安装:`pip install -r requirements.txt`。便于在别的机器复现环境。
