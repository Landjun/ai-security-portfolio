# with 上下文管理器

## with 是干什么的?
自动管理资源的"打开-使用-关闭",即使中途出错也保证关闭。最常见是文件操作:
```
with open("a.txt", encoding="utf-8") as f:
    data = f.read()
# 出了 with 块,文件自动关闭,不用手动 f.close()
```

## 不用 with 会怎样?
手动 open 后如果忘了 close,或中间报错,文件句柄可能一直占用。with 更安全省心。

## 还能同时管理多个资源吗?
```
with open("in.txt") as fin, open("out.txt", "w") as fout:
    fout.write(fin.read())
```

## 还有哪些地方用 with?
- 数据库连接、网络请求会话(requests.Session)、线程锁等。
- 很多库的对象支持 with,用了能自动释放资源。

## 自己的类怎么支持 with?
实现 `__enter__` 和 `__exit__` 两个方法即可(进阶内容,了解即可):
```
class Timer:
    def __enter__(self): ...
    def __exit__(self, *a): ...
```
新手先掌握用 with 处理文件就够了。
