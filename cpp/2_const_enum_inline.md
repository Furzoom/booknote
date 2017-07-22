# 使用const, enum, inline替代#define

使用`#define`的名称不会进入到符号表。

定义常量使用const，如：

```cpp
#define PI 3.14
const double PI = 3.14;
```

在定义常量字符串时，需要注意，不希望其指向其他的常量，所以需要如下定义：

```cpp
const char * const AUTHOR_NAME = "Furzoom";
```

另一个值得注意的是，为了将常量的作用域限制于class内，必须让他成为class的一个成员，而为确保此常量至多只一份实体，必须让它成为一个static成员：

```cpp
class GamePlayer {
private:
  static const int NumTurns = 5;      // 常量声明
  int scores[NumTurns];               // 使用常量
  ...
};
```

为什么说上面是常量声明，而不是定义呢？通常C++要求对所使用的任何东西提供一个定义，但如果它是个class专属常量又是static且为整数类型，则需要特殊处理。只要不取它们的地址，可以声明并使用它们而不需要提供定义。但如果取这个常量的地址，或者不取地址，但编译器要看到这个地址，就必须提供定义，放在实现文件中：

```cpp
const int GamePlayer::NumTurns;
```

由于在声明时已经获得了初值，所以上面不需要再进行赋初值。

如果编译器不支持static整型class常量in class初始化，那么后续的`int scores[NumTurns];`,就会有问题。这时可以使用the enum hack的方式。原因是：一个属于枚举类型的数值可权充ints被使用。于是：

```cpp
class GamePlayer {
private:
  enum {NumTurns = 5};                // the enum hack
  int scores[NumTurns];               // 使用常量
  ...
};
```

enum hack的行为比较像#define，而不像const。因为取一个const的地址是合法的，但取一个enum的地址就不合法。如果不想让别人得一个pointer或reference指向你的某个整数常量，使用enum可以实现这个约束。

另一点关于enum hack，它是template metaprogramming(模板元编程)的基础技术。

下一个关于使用宏的问题是如下：

```cpp
#define CALL_WITH_MAX(a, b) f((a) > (b) ? (a) : (b))
```

下面这个宏实现了类型函数的功能，但却不会带来函数调用的开销。对于定义，首先要记住每个实参都要使用小括号进行包裹，否则在使用表达式调用时，可能会有问题。即使使用小括号，也不是万事大吉了。如：

```cpp
int a = 5, b = 0;
CALL_WITH_MAX(++a, b);            // a会被累加2次
CALL_WITH_MAX(++a, b+10);         // a会被累加1次
```

显然，上面是有问题的，使用的时候要十分小心，而且调试起来也是比较困难。使用inline可以解决上面的问题。

```cpp
template<typename T>
inline void callWithMax(const T& a, const T& b)
{
  f(a > b ? a : b);
}
```

这里不需要在函数本体中为参数加上括号，也不需要操心参数被求值多次。同时完全可以写出一个class内的private inline函数。上面的代码，由于不知道T是什么，所以采用Pass-by-reference-to-const的形式。

**总结**:
- 对于单纯常量，最好使用const对象或enums替换#define。
- 对于形似函数的宏(macros)，最好改用inline函数替换#define。
