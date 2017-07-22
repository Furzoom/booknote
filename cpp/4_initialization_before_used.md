# 确实对象使用前进行初始化

```cpp
int x;
```

这条语句在不同的语境下，可能被初始化(为0)，也可能没有初始化。这样的问题听起来都让人头疼。有一定的规则来描述对象的初始化何时一定发生，何时不一定发生。但记忆起来还是负担太重了。

其实也简单，对于无任何成员的内置类型，必须手工完成初始化：

```cpp
int x = 0;
const char* text = "A C-style string";
double d;
std::cin >> d;
```

对于内置类型以外的任何其他类型，初始化是在构造函数内完成的。规则很简单，确保每一个构造函数都将对象的每一个成员初始化了。

关键一点区分开初始化与赋值。

```cpp
class PhoneNumber {...};
class ABEntry {                         // ABEntry = "Address Book Entry"
public:
  ABEntry(const std::list<PhoneNumber>& phones);
private:
  std::list<PhoneNumber> thePhones;
  int numTimesConsulted;
};

ABEntry::ABEntry(const std::list<PhoneNumber>& phones)
{
  thePhones = phones;                  // 都是assignments而不是initializations
  numTimesConsulted = 0;
}
```

C++规定对象的成员变量的初始化动作发生在进入构造函数本体之前。在进行构造函数本体之前，非内置类型的对象都已经使用default构造函数进行了初始化，numTimesConsulted却不保证，因为它是内置类型。构造函数应该使用member initialization list进行初始化。如：

```cpp
ABEntry::ABEntry(const std::list<PhoneNumber>&phones)
  :thePhones(phones), numTimesConsulted(0)
{}
```

这个构造函数的结果与上一个最终结果相同，但效率更高。对于内置类型来讲，初始化和赋的成本相同。对于希望调用default构造函数的成员变量，同样使用成员列表进行初始化。如：

```cpp
ABEntry::ABEntry()
  :thePhones(), numTimesConsulted()
{}
```

有些情况下对于内置类型，也一定得显式的初始化。如果，成员变量是const或reference时，它们就一定得需要初值，不能赋值。

C++成员初始化的次序问题相同的，先Base class，然后Derived class。class中的成员变量问题按照声明的顺序进行初始化。这就要求在成员初始化时按照声明的顺序，否则，达不到高效的目的。

## 不同编译单元non-local static对象初始化

研究完以上初始化内容，还是一个就是不同编译单元的non-local static对象初始化顺序问题。

所谓static对象，其寿命从被构造出来直到程序结束为止，因此stack和heap-based对象都被排除。static对象包括global对象、定义于namespace作用域内的对象、在classes内、在函数内、以及在file作用域内被声明为static的对象。函数内的static对象称为local static对象，其他static对象称为non-local static对象。程序结束时static对象会被自动销毁，也就是它们的析构函数会在main()结束时被自动调用。

所谓编译单元(translation unit)是指产生单一目标文件的那些源码。基本上它是单一源码文件加上其所含入的头文件。

现在的问题是：如果某个编译单元内的某个non-local static对象的初始化动作使用了另一编译单元内的某个non-local static对象，它所用到的这个对象可能尚未被初始化，因为C++对定义于不编译单元内的non-local static对象的初始化次序并无明确定义。

为解决上面的问题，将每个non-local static对象放到自己的专属函数内(该对象在此函数内被声明为static)。这些函数返回一个reference指向它所含的对象。换句话说，non-local static对象被local static对象替换了。这就是Singleton模式的一个常见的实现手法。

这个方法可行的原因是：C++保证，函数内local static对象会在该函数被调用的首次遇上该对象的定义时被初始化。

## 总结

- 为内置类型对象进行手工初始化，因为C++不保证初始化它们。
- 构造函数最好使用成员初始化列表，而不要在构造函数内本体内使用赋值操作。初始化列表中成员变量，其排列次序应该和它们在class中的声明次序相同。
- 为避免跨编译单元初始化次序问题，请使用local static对象替换non-local static对象。
