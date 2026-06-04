# 类型注解 type hints

## 类型注解是什么?
给变量、参数、返回值标注类型,提升可读性,编辑器也能据此提示和检查:
```
def greet(name: str, age: int) -> str:
    return f"{name} 今年 {age} 岁"
```
`name: str` 表示参数是字符串,`-> str` 表示返回字符串。

## 注解会强制类型检查吗?
不会。Python 运行时不强制,传错类型也能跑。注解主要是给人和工具看的"提示"。

## 变量也能注解?
```
count: int = 0
names: list[str] = []
```

## 常见的复合类型怎么写?
- 列表:`list[int]`;字典:`dict[str, int]`;元组:`tuple[int, int]`。
- 可能为 None:`str | None`(Python 3.10+)或 `Optional[str]`(从 typing 导入)。

## 有什么好处?
- 编辑器自动补全更准、能提前发现类型错误。
- 大项目里读代码时一眼知道每个参数该传什么。

## 要不要用?
新手了解能看懂即可;写稍大的项目或团队协作时,加注解是好习惯。
