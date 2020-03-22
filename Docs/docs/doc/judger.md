
# 判题机功能说明

## Special Judge

如果要使用Special Judge，请在提交数据的时候，把特判程序一同上传

如果没有一同上传，判题机会把题目视为一般题目。如果上传了spj.cpp，无论你在添加题目时有没有把题目设置为spj，判题机都会认为是spj题目。

特判程序命名为 spj.cpp


所以你的数据文件夹内应该有如下格式的内容

1.in

1.out

2.in

2.out

...

spj.cpp


然后spj.cpp的写法为：

```cpp
#include<stdio.h>
using namespace std;
int main(int argc, char* argv[]) {
    FILE * f_in=fopen(argv[1],"r"); //测试输入
	FILE * f_out=fopen(argv[2],"r"); //测试输出
	FILE * f_user=fopen(argv[3],"r"); //用户输出
	int ret=0; //AC=0, WA=1, 其他均为 System Error

	/*****spj代码区域*******/
    // 以下是一个a+b的例子

    int a,b,c,d;
	fscanf(f_in,"%d %d",&a,&b);
	fscanf(f_out,"%d",&c);
	fscanf(f_user,"%d",&d);
	if(c==d)
        ret=0;
    else 
        ret = 1;
	/*****spj-end********/ 
	
    fclose(f_in);
    fclose(f_out);
    fclose(f_user);

    //如果你想输出更多的信息，可以在同目录下，输出一个叫做 **spjmsg.txt** 的文件，当返回1时，系统会读取spjmsg.txt中的内容，显示在判题信息中。
    //如果你想输出更多的信息，可以在同目录下，输出一个叫做 **spjmsg.txt** 的文件，当返回1时，系统会读取spjmsg.txt中的内容，显示在判题信息中。
    //如果你想输出更多的信息，可以在同目录下，输出一个叫做 **spjmsg.txt** 的文件，当返回1时，系统会读取spjmsg.txt中的内容，显示在判题信息中。
    //重要事情说三遍，这样的话可以给用户更多的错误信息！！

    #include <fstream>
    ofstream out("spjmsg.txt");
    if (out.is_open()) 
    {
        out << "This is a line.\n";
        out << "This is another line.\n";
        out.close();
    }

    return ret;//返回结果，返回值为0时，答案正确，为1时，答案错误，返回值为其他时，会报System Error
}


```


## 模板题

模板题就是类似LeetCode那种，用户需要提交特定的接口函数。

如果需要判断模板题，就要有 **template.对应语言** 这个文件

模板题必须包含**template.对应语言**，判题机会简单的把用户代码拼接在template上面


如果要使用模板题，请在提交数据的时候，把模板程序一同上传。判题机只会做简单的判断有没有template文件，有的话就拼接。


如果没有一同上传，判题机会把题目视为一般题目。如果上传了模板程序，无论你在添加题目时有没有把题目设置为模板题，判题机都会认为是模板题目。

目标程序命名为 

template.语言

如

1. template.c
   
2. template.cpp
   
3. template.java
   
4. template.py2
   
5. template.py3

6.  template.swift


所以你的数据文件夹内应该有如下格式的内容

1.in

1.out

2.in

2.out

...

template.c

template.cpp

template.java

template.py2

template.py3

template.swift


有时候你可能需要在用户代码上面添加代码。那么你可以多添加这几个文件

1.in

1.out

2.in

2.out

...

template.c

template.cpp

template.java

template.py2

template.py3

template.swift

**template.c.top**

**template.cpp.top**

**template.java.top**

**template.py2.top**

**template.py3.top**

**template.swift.top**



**.top的代码，判题机会把他们放在用户程序的上面，没有top的会放在下面**


例如

template.py2.top
```py
msg = "这在用户代码上面"
```

用户提交的代码
```py
def myfunc(t):
    print(msg,t)
```

template.py2
```py
myfunc("这在用户代码下面")
```


最后生成的程序为

```py
msg = "这在用户代码上面"
def myfunc(t):
    print(msg,t)
myfunc("这在用户代码下面")
```

最后就会运行上面这个代码。


.top文件很有用，比如在Python中，就可以防止用户作弊！或者做某些重定向的工作啥的。



如果没有某种语言的模板程序，判题机只会简单的运行用户的代码。如果有模板程序，判题机会将用户代码拼接在模板程序上面。然后作为新的用户代码进行运行。


## 模板题和spj题

这两个可以一起使用过，提交的数据文件为

1.in

1.out

2.in

2.out

...

**spj.cpp**

template.c

template.cpp

template.java

template.py2

template.py3

template.swift

**template.c.top**

**template.cpp.top**

**template.java.top**

**template.py2.top**

**template.py3.top**

**template.swift.top**