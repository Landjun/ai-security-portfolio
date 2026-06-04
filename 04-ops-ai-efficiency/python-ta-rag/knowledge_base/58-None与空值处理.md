# None 与空值处理

## None 是什么?
表示"什么都没有""空"的特殊值。函数没有 return 时,默认返回 None。

## 怎么判断一个值是不是 None?
用 `is`,不要用 `==`:
```
if x is None:
    print("x 是空的")
if x is not None:
    print("x 有值")
```

## None、空字符串、0 有什么区别?
- None:没有值。
- ""、[]:有值,但是"空的"。
- 0、False:有值,只是为零/假。
在 if 里它们都为"假",但语义不同,判断"是否存在"用 `is None` 更准确。

## 函数参数默认值常用 None?
```
def f(items=None):
    if items is None:
        items = []       # 在函数内创建,避免可变默认参数陷阱
    items.append(1)
    return items
```
不要写 `def f(items=[])`,那个空列表会在多次调用间共享(经典坑)。

## 字典取值避免 None 报错?
`d.get("key")` 不存在返回 None;`d.get("key", 默认值)` 返回默认值,避免后续对 None 操作出错。
