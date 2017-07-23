# 显式拒绝编译器生成的函数

如果需要阻止对象被复制，应该禁用copy构造函数和copy assignment操作符。方法就是将copy构造函数和copy assignment操作符定义为private，这样就不能对象就不能被外界复制，但还是可以被对象member函数及friend函数复制。方法就是只声明copy构造函数和copy assignment操作符，而不定义它们，这样链接器就会报错。如：

```cpp
class A {
public:
  ...
private:
  A(const A& a);
  A& operator=(const A& a);
};
```

通常将阻止复制的特性设计为一个类：

```cpp
class Uncopyable {
protected:
  Uncopyable() {}
  ~Uncopyable() {}
private:
  Uncopyable(const Uncopyable&);
  Uncopyable& operator=(const Uncopyable&);
};
```
