# C++默认编写和调用的函数

编译器给empty class添加4个函数：
- default构造函数。
- copy构造函数。
- copy assignment操作符。
- 析构函数。

这些函数都是public且inline的。default函数只要没有声明任何构造函数时才会被生成。

如下声明：

```cpp
class Empty {};
```

相当于如下代码：

```cpp
class Empty {
public:
  Empty() {...}
  Empty(const Empty& empty) {...}
  ~Empty() {...}

  Empty& operator=(const Empty& empty) {...}
};
```

惟有当这些函数被需要(调用)时，它们才会被编译器创建出来。

这4个函数会被默认创建，这些函数默认会做些什么呢？default构造函数和析构函数主要是给编译器一个地方用来放置藏身幕后的代码，像调用base classes和non-static成员变量的构造函数和析构函数。编译器产出的析构函数是个non-virtual，除非这个class的base class自身声明有virtual析构函数。

至于copy构造函数和copy assignment操作符，编译器创建的版本只是单纯地将来源对象的每一个non-static成员变量拷贝到目标对象。

如果类内含有reference成员，或者const成员时，编译器不能生成合法的copy assignment函数，就会不生成copy assignment操作符。还有一种情况，如果某个base classes将copy assignment操作符声明为private，编译器将拒绝为其derived classes生成一个copy assignment操作符。
