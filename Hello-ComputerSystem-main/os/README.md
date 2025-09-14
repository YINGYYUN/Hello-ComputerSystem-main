# OS Simulator - Mini Operating System

这是一个简单的操作系统模拟器，帮助你理解操作系统的核心概念：进程管理、系统调用和进程调度。通过这个模拟器，你可以体验到操作系统提供的系统调用和并发调度功能，理解用户程序如何和操作系统交互。

## 项目结构

```
os/
├── src/               # 核心OS模拟器代码
│   ├── myos.py       # 操作系统核心模块
│   ├── process.py    # 进程和系统调用定义
│   └── __init__.py   # Python包初始化
├── lab1/              # 实验1：进程调度器
│   ├── lab1.py       # 学生需要实现的调度算法
│   └── __init__.py   # Python包初始化
├── tests/             # 测试代码
│   ├── test_lab1.py  # Lab1的测试用例
│   └── __init__.py   # Python包初始化
├── examples/          # 示例代码
│   ├── main.py       # 主程序入口，演示OS功能
│   └── __init__.py   # Python包初始化
├── run_tests.py      # 测试脚本
└── README.md         # 项目说明文档
```

## 代码说明

### 运行示例


```bash
# 运行示例
python3 examples/main.py
```

**如果你使用Windows，且python3运行无反应，可以尝试用python代替python3**

### process.py - 进程和系统调用定义

```python
class Process:
    def __init__(self, syscalls: List[Syscall]):
        self.syscalls = syscalls  # 进程要执行的系统调用序列
        self.step = 0             # 当前执行步骤

class Syscall:
    def __init__(self, syscall: SyscallType, arg: object=None):
        self.syscall = syscall   # 系统调用类型
        self.arg = arg           # 系统调用参数
```

### myos.py - 操作系统核心

该模块实现了操作系统的核心功能，提供了完整的进程管理和调度接口：

#### 初始化

```python
def init(my_scheduler, my_procs: List[Process])
```

初始化操作系统，建立运行环境

- `my_scheduler`: 调度函数，接收进程列表返回选中的进程

- `my_procs`: 初始进程列表

#### 2. 统计进程数

返回当前运行队列中的进程数量。

```python
def process_count() -> int
```

#### 进程调度

```python
def process_schedule() -> Process
```

这个函数会返回选择的下一个要运行的进程，它会把当前正在运行的进程列表作为参数传递给`init`函数中设置好的调度函数，由用户设置的调度函数来选择下一个进程。

#### 步进进程

```python
def process_step(proc: Process) -> Syscall
```

用来模拟`proc`进程的执行，当进程执行到一个系统调用指令的时候，会从这个函数返回，请求操作系统处理。这个函数会返回进程请求的系统调用。

#### 添加进程

```python
def process_push(proc: Process)
```

将进程`proc`添加到运行中进程列表的末尾。

#### 退出进程
```python
def process_exit(proc: Process)
```

终止进程并清理相关资源

### main.py - 演示程序

在演示程序中，我们首先定义了一个随机调度器，它会随机选择一个进程执行：

```python
def random_scheduler(procs):
    """A random scheduler that selects a process randomly"""
    return random.choice(procs)
```

演示程序创建三个进程，每个进程执行5次写操作然后退出：

```python
# Initialize the Operating System
init(
    random_scheduler,
    [
        Process([Syscall(SyscallType.SYS_WRITE, 'A')] * 5 + [Syscall(SyscallType.SYS_EXIT)]),  # Process A runs 5 steps, outputs character 'A'
        Process([Syscall(SyscallType.SYS_WRITE, 'B')] * 5 + [Syscall(SyscallType.SYS_EXIT)]),  # Process B runs 5 steps, outputs character 'B'
        Process([Syscall(SyscallType.SYS_WRITE, 'C')] * 5 + [Syscall(SyscallType.SYS_EXIT)]),  # Process C runs 5 steps, outputs character 'C'
        ]
    )
```

`run()`函数是操作系统的核心调度循环，模拟了真实操作系统的工作方式。让我们逐步分析它的工作原理：

```python
def run():
    while process_count() > 0:           # 1. 检查是否还有进程需要运行
        current = process_schedule()     # 2. 选择下一个要运行的进程
        call = process_step(current)     # 3. 执行选中进程的一步
        
        if call.syscall == SyscallType.SYS_EXIT:     # 4. 处理系统调用
            process_exit(current)                    # 4a. 进程退出
        elif call.syscall == SyscallType.SYS_WRITE:
            print(call.arg, end='')                  # 4b. 输出字符
    
    print()  # 所有进程结束后换行
```

### 运行示例

程序运行时会输出类似以下的随机字符序列：
```
AABCACBACACCBBB
```

每次运行结果都不同，但每个字符（A、B、C）都会出现5次

## 实验内容

我们编写了自动测试脚本。如果题目有难度，你也可以提交思路文档。

```bash
# 查看如何运行测试
python3 run_tests.py help

# 运行所有测试
python3 run_tests.py all
```

### LAB1 顺序调度器

在lab1.py中实现一个顺序调度器，它总是选择`procs`中的第一个进程运行。

### LAB2 优先级调度器

在lab2.py中实现一个优先级调度器，它总是选择`procs`中属性`priority`值最大的那个进程运行，当`priority`值相同的时候，选择更靠前的进程运行。

具体的，你需要使用`proc.priority`来获取进程的优先级。

*也许你想使用堆或其他数据结构，在通过了最基本的测试之后，你可以随意修改所有代码，或者描述一下你的时间复杂度更小的实现思路*

### LAB3 WRITE_DOUBLE 系统调用

在仿照`main.py`中的`run()`函数，lab3.py中编写你自己的`my_run()`函数，你需要支持三个系统调用：`EXIT`、`WRITE`和`WRITE_DOUBLE`，其中`WRITE_DOUBLE`和`WRITE`类似，只是它会输出两遍。

### LAB4 FORK 系统调用

支持`FORK`系统调用，这个系统调用需要操作系统复制原始进程的状态，并把新的进程添加到进程列表的末尾。

### LAB5 真实世界的操作系统

查找资料，什么是内核态，什么是用户态？我们的小型OS模型在运行哪部分的时候在模拟内核态，哪部分的时候再模拟用户态？

我们使用了函数调用来模拟返回用户程序，函数调用和真实的CPU状态切换有什么区别？你应该尽可能刨根问底，查找资料和询问AI。
