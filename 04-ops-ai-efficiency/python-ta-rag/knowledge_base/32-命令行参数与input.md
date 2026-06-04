# 命令行参数与 input

## 怎么读用户在程序里输入的内容?
用 input(),返回的是字符串:
```
name = input("请输入姓名:")
age = int(input("请输入年龄:"))   # 需要数字时记得转换
```

## 怎么读命令行参数(运行时传入)?
最简单用 sys.argv:
```
import sys
print(sys.argv)          # ['脚本名', '参数1', '参数2', ...]
```
运行 `python a.py hello 123`,sys.argv 就是 `['a.py', 'hello', '123']`。
注意:取到的都是字符串,需要数字要自己转换。

## 参数多、需要选项时用什么?
用标准库 argparse,能自动解析 `--name 值` 这类选项并生成帮助:
```
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--name", default="世界")
args = parser.parse_args()
print(f"你好, {args.name}")
```
运行 `python a.py --name 小明`。

## input 和命令行参数怎么选?
交互式、运行中需要用户输入用 input;一次性、可脚本化的配置用命令行参数。
