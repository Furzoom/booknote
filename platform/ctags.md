# Ctags快速入门
---

在vim下阅读代码，特别是阅读不熟悉的代码时，ctags是一个提高效率的强大的工具。

## 1. ctags是什么？

ctags可以将代码中的函数、方法、类、变量和其他的标识符进行索引，将索引结果进行排序存储在`tags`中。在该文件中每一行就是一个tag。根据语言及生成时参数的不同，存储的具体内容也是不同的。

ctags当前支持41种语言，具体参考[ctags支持的语言](http://ctags.sourceforge.net/languages.html)，若要新增语言也是十分方便的。

使用ctags，可以方便的在大项目中进行导航。在你不熟悉项目时，当你不确定一个方法到底做什么，或者如何使用时，可以直接跳转到方法的定义位置。当然，也可以很方便的跳转到原来的地方。

## 2. ctags的安装

在Ubuntu下安装ctags：

```shell
$ sudo apt-get install ctags
```

## 3. ctags的使用

首先，进入到要进行索引代码的目录中，执行以下命令：

```shell
$ ctags -R .
```

将会递归的遍历当前文件夹，对所有它认识的文件进行索引，并将结果写入到当前目录下的tags文件。一般它很快就执行完了，速度取决于你项目中源文件的多少。

其他参数使用的不多。

## 4. ctags在vim的使用示例

在代码的目录使用vim打开源文件开始浏览代码，vim将自动加载当前目录中的tags文件。

假如你有如下的两个文件：

global.h

```c
#define NAME "Furzoom"

int g_count;
```

main.c

```c
#include <stdio.h>
#include "global.h"

void say_hello(void)
{
    printf("%s\n", NAME);
    printf("Hello\n");
}

int main()
{
    printf("%d\n", g_count);
    say_hello();
    return 0;
}
```

先生成tags，然后在当前目录打开main.c文件。

当光标停留在`main()函数中的`say_hello`函数调用上时，按下`<C-]>`，直接跳到了`say_hello`定义的位置。

然后将光标移动到`NAME`上，按下`<C-]>`，跳到了global.h文件中的`NAME`的定义处。接着按上`<C-T>`，又跳回到main.c文件的NAME处。

在命令模式输入`:tag say_hello`,也会跳转到`say_hello`函数的定义处。

当然好多时候函数名字那么长，怎么能记得清楚，`:tag`是支持正则表达式的，如`tag /^say`, 在本例中同样会跳转到`say_hello`函数的定义处。它会查找到所有以`say`开头的标识符，具体的跳转顺序以后会给大家介绍。

是不是如此的方便。

## 5. ctags在vim中的快捷键

- `<C-]>`，跳转到定义处。
- `<C-T>`，跳回上次跳转之前。
- `:ts`或者`:tselect`，显示`tag`命令选择的列表，半进行跳转。
- `:tn`或者`:tnext`，跳转到列表中下一个。
- `:tp`或者`:tprevious`，跳转到列表中上一个。
- `:tf`或者`:tfirst`，跳转到列表中第一个。
- `:tl`或者`:tlast`，跳转到列表中的最后一个。

https://courses.cs.washington.edu/courses/cse451/10au/tutorials/tutorial_ctags.html
https://andrew.stwrt.ca/posts/vim-ctags/
http://ctags.sourceforge.net/languages.html
