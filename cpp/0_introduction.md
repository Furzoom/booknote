# 0 导言

## 术语Terminology

### Declaration

声明是告诉编译器某个东西名称和类型。

```cpp
extern int x;                       // object
std::size_t numDigits(int number);  // function
class Widget;                       // class

template<typename T> class Graph;   // template
```

### Definition

定义提供是提供编译器一些声明遗漏的细节。对对象而言，定义是编译器为此对象分配内存;对函数或者函数模板而言，定义提供代码本体;对类和类模板而言，定义列出他们的成员。

```cpp
int x;                              // object
std::size_t numDigits(int number)   // function
{
  std::size_t digits = 1;
  while ((number /= 10) != 0) ++digits;
  return digits;
}

class Widget {                      // class
public:
  Widget();
  ~widget();
  ...
};

template<typename T> class Graph {  // template
public:
  Graph();
  ~Graph();
  ...
};
```

### Initialization

初始化是给对象赋初值的过程。对用户自定义的类型的对象而言，初始化由构造函数执行。默认构造函数是一个可被调用而不带任何参数者。

```cpp
class A {
public:
  A();                              // default constructor
};

class B {
public:
  explicit B(int x = 0, bool b = true); // default constructor
};
```

## explicit

除非有一个好理由允许构造函数被用于隐式类型转换，否则就把它声明为`explicit`。

## copy构造函数和copy assignment操作符

copy构造函数用来以同类型对象初始化自我对象，copy assignment操作符用来从另一个同类型对象中拷贝其值到自我对象。

```cpp
class Widget {
public:
  Widget();                             // default构造函数
  Widget(const Widget &rhs);            // copy构造函数
  Widget& operator=(const Widget &rhs); // copy assignment操作符
  ...
};

Widget w1;                              // 调用default构造函数
Widget w2(w1);                          // 调用copy构造函数
w1 = w2;                                // 调用copy assignment操作符
```

copy构造函数是一个重要的函数，它定义了一个对象如何passed by value。

```cpp
bool hasAcceptableQuality(Widget w);
...
Widget aWidget;
if (hasAcceptableQuality(aWidget)) ...
```

pass-by-value意味着调用copy构造函数。
