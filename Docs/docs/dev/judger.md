# 判题机开发

测评机，测评机的功能就是进行判题，在收到判题服务器发送过来的判题消息后，会对该提交在沙盒中进行评测。具体过程如下图所示：

![判题过程示意图](/img/faq/db4.png)

测评机向数据库查询代码，将代码生成文件，然后编译。如果编译通过会进行程序运行。程序运行成功后，会将输出的文件和正确的输出文件进行比较，如果完全一致，则返回代码通过，否则不通过。同时将测试数据也一并截取保存到数据库中

## 结果解释 
1. WAITING = -6
1. PRESENTATION_ERROR = -5
1. COMPILE_ERROR = -4
1. WRONG_ANSWER = -3
1. PENDING = -1
1. JUDGINNG = -2
1. CPU_TIME_LIMIT_EXCEEDED = 1
1. REAL_TIME_LIMIT_EXCEEDED = 2
1. MEMORY_LIMIT_EXCEEDED = 3
1. RUNTIME_ERROR = 4
1. SYSTEM_ERROR = 5

## 开源的C++评测技术
由于系统追求稳定性，自己开发测评程序难免会有各种各样的问题，因此一个稳定的测评技术非常重要。在开源社区上有一款开源的测评模块，由青岛大学开发，该测评技术在青岛大学得到了运用，且非常的稳定，经过测试和改进后，可以运用到本系统当中。该测评技术只有一个简单的功能，即运行程序，并得到输出。函数结构如下：
```
Function (最大CPU时间，最大运行时间，最大允许内存，最大输出大小，最大栈大小，执行程序的路径，输入文件的路径，输出文件的路径，错误输出额路径)
```
调用该函数并传入对应参数后，该函数会生成一个沙盒，然后在沙盒内运行该程序，运行后程序会返回一个结构体，该结构体保存了程序的运行结果，具体如下：
```
{'cpu_time', 'signal':, 'memory', 'exit_code', 'result', 'error', 'real_time'}
```
分别对应着，程序运行使用CPU得时间，程序发出的信号，程序占用的内存，程序退出时的返回值，程序运行的结果，程序运行的时间（包括了系统调度的时间）其中result有如下6个枚举值

+ SUCCESS = 0 (此结果仅代表程序成功运行完毕并正确退出)
+ CPU_TIME_LIMIT_EXCEEDED = 1
+ REAL_TIME_LIMIT_EXCEEDED = 2
+ MEMORY_LIMIT_EXCEEDED = 3
+ RUNTIME_ERROR = 4
+ SYSTEM_ERROR = 5

如果程序正常退出的话，我们就可以将程序输出的内容，与正确的内容做比较，得出是答案错误还是通过。

## 自己写的Java 测评技术

- [x] 限时
- [x] 测时
- [ ] 限内存
- [ ] 测内存

### 编译

直接调用命令进行编译，并将编译结果保存，和错误信息也保存。

```py
result = os.system("javac Main.java -d %s 2>%sce.txt" %(judgername, judgername))
```

### 运行

通过**/usr/bin/time**命令来实现时间的计算

通过timeout命令来实现限时

```py
com1 = "/usr/bin/time -f '"+"%"+"U' -o %stime.txt " % (judgername)
com2 = "timeout %s java -cp %s -Djava.security.manager -Djava.security.policy==policy -Djava.awt.headless=true Main 1>%s 2>%s<%s" % (
        str(timelimit/1000.0), judgername, outputpath, errorpath, inputpath)
com = com1 + com2
result = os.system(com)
```