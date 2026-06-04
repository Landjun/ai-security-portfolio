# lambda 与函数进阶

## lambda 是什么?
匿名函数,适合写一行的小函数:
```
square = lambda x: x * x
print(square(5))   # 25
```
等价于:
```
def square(x):
    return x * x
```

## lambda 常和什么一起用?
常用于 sorted、map、filter 的 key/函数参数。例如按绝对值排序:
```
nums = [-3, 1, -2]
print(sorted(nums, key=lambda x: abs(x)))   # [1, -2, -3]
```

## 全局变量和局部变量(作用域)?
函数内定义的变量是局部的,函数外访问不到。要在函数内修改全局变量,需用 global 声明:
```
count = 0
def add():
    global count
    count += 1
```
但尽量少用 global,优先用参数和返回值传递数据。

## 什么是递归?
函数调用自己。必须有"终止条件",否则会无限递归报错(RecursionError):
```
def factorial(n):
    if n <= 1:        # 终止条件
        return 1
    return n * factorial(n - 1)
```
