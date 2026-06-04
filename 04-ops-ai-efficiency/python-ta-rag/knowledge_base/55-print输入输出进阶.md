# print 输入输出进阶

## print 怎么控制分隔符和结尾?
```
print("a", "b", "c", sep="-")    # a-b-c,用 sep 控制分隔
print("不换行", end="")          # end="" 让它不换行
print("续在同一行")
```
默认 sep 是空格,end 是换行符 \n。

## 怎么打印不换行地刷新(进度提示)?
```
import time
for i in range(101):
    print(f"\r进度 {i}%", end="", flush=True)
    time.sleep(0.02)
```
`\r` 回到行首,end="" 不换行,flush=True 立即刷新,实现原地更新。

## 怎么把内容打印到文件?
```
with open("log.txt", "w", encoding="utf-8") as f:
    print("写进文件", file=f)
```

## input 的提示语怎么写?
`name = input("请输入姓名:")`,括号里的文字会显示给用户。
记住 input 返回的是字符串,需要数字要 int()/float() 转换。

## 怎么一行输入多个值?
```
a, b = input("输入两个数(空格分隔):").split()
a, b = int(a), int(b)
```
