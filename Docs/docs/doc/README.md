# 简介

暂无内容！欢迎补充！

# Special Judge

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

    return ret;//返回结果，返回值为0时，答案正确，为1时，答案错误，返回值为其他时，会报System Error
}

```