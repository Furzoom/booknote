# 尽可能使用const

const允许指定一个语义约束，而编译器会强制实施这项约束。它允许你告诉编译器和其他程序员某值应该保持不变，只要这是事实，你就应该确实说出来，因为这可以获得编译器的帮助。

const有多种使用方式。可以用在class外部修饰global或namespace作用域的常量，或者修饰文件、函数、区块作用域中被声明为static的对象。也可以用于修饰class内部的static和non-static成员变量。对于指针，即可指出指针自身，指针所指物，或两者都(或都不)是const。

## const通用方法

```cpp
char greeting[] = "Hello";
char *p = greeting;                       // non-const pointer, non-const data
const char *p = greeting;                 // non-const pointer, const data
char* const p = greeting;                 // const pointer, non-const data
const char * const p = greeting;          // const pointer, const data
```

STL迭代器系以指针为基础建立的，迭代器就的作用就像个`T*`指针。声明迭代器为const就像声明指针为const一样(T* const)，表示这个迭代器不得指向不同的东西，但它所指的东西的值是可以改动的。如果希望迭代器所指的东西不可被改动(即const T*)，需要使用const_iterator。

```cpp
std::vector<int> sec;
...
const std::vector<int>::iterator iter = vec.begin();    // iter <==> T* const
*iter = 10;                                             // OK
++iter;                                                 // Error

std::vector<int>::const_iterator iter = vec.begin();    // iter <==> const T*
*iter = 10;                                             // Errro
++iter;                                                 // OK
```

const在有用的地方是在函数声明时使用的，在函数声明中，const可以和函数返回值，各参数，函数本身产生联系。

令函数返回一个常量值，往往可以降低用户错误而造成的意外，而又不至于许诺安全性和高效性。如：

```cpp
class Rational {...};
const Rational operator* (const Rational& lhs, const Rational& rhs);
```

这可以避免以下的错误：

```cpp
Rational a, b, c;
...
(a * b) = c;                            // 在a*b的结果上调用operator=
```

const参数，就像是local const对象一样。除非需要改动参数或者local对象，否则请将它们声明为const，可以省下恼人的错误。

## const成员函数

将const应用于成员函数的目的，是为了确认该成员函数可作用于const对象身上。const成员函数很重要，原因有二。第一，它们使class接口比较容易被理解。得知哪个函数可以改动对象内容而哪个函数不行。第二，这使得对const对象的操作成为可能。这对编写高效代码是个关键，因为改善C++程序效率的一个根本方法是以Pass-by-reference-to-const方式传递对象，而此技术可行的前提就是，有const成员函数可用来处理取得的const对象。

两个成员函数如果只是常量性(constness)不同，可以被重载。

```cpp
class TextBlock {
public:
  ...
  const char& operator[] (std::size_t position) const // operator[] for const
  { return text[position]; }
  char& operator[] (std::size_t position)             // operator[] for non-const
  { return text[position]; }
private:
  std::string text;
};

TextBlock tb("Hello");
std::cout << tb[0];               // 调用non-const TextBlock::operator[]
const TextBlock ctb("World");
std::cout << ctb[0];              // 调用const TextBlock::operator[]
```

## Bitwise constness和logical constness

Bitwise是指成员函数在不更改对象任何成员变量(static除外)时才可以说是const。也就是说他不更改对象内的任何一个bit。

但是如果const成员函数更改了指针成员变量所指的对象，是被编译器允许的。但这与现实的需要是不符的。

上面的情况就是导出了所谓的logical constness。一个const成员函数可以修改它所处理的对象内的某些bits，但只有在客户端侦测不出的情况下才得如此。

如在TextBlock类内有高速缓存文本区块的长度以便就会询问：

```cpp
class TextBlock {
public:
  ...
  std::size_t length() const;
private:
  char* pText;
  std::size_t textLength;
  bool lengthIsValid;
};

std::size_t TextBlock::length() const
{
  if (!lengthIsValid) {
    textLength = std::strlen(pText);          // Error, 在const成员函数内不能修改
    lengthIsValid = true;                     // textLength和lengthIsValid的值
  }
  return textLength;
}
```

length的实现不是bitwise const，因为它修改了textLength和lengthIsValid，但这两处的修改对于const TextBlock对象而言是可以接受的，但是编译器认为这是一个错误。

使用C++的关键字mutable，可以释放掉non-static成员变量的bitwise constness约束。

```cpp
class TextBlock {
public:
  ...
  std::size_t length() const;
private:
  char* pText;
  mutable std::size_t textLength;
  mutable bool lengthIsValid;
};

std::size_t TextBlock::length() const
{
  if (!lengthIsValid) {
    textLength = std::strlen(pText);          // Now, it's ok
    lengthIsValid = true;                     // ok
  }
  return textLength;
}
```

## const与non-const成员函数重复的问题

在const成员函数和non-const成员函数中处理的流程基本流程是一致的，这就导致了代码重复的问题。当然可以将二者重复的部分提取成一个priavte函数，但学是会有重复的调用和返回。真正该做的是实现一次，能使用两次。也就是说令其中的一个调用另一个。

```cpp
class TextBlock {
public:
  //...
  const char& operator[] (std::size_t position) const
  {
    //...
    return text[position];
  }
  char& operator[] (std::size_t position)
  {
    return const_cast<char&>(static_cast<const TextBlock&>(* this)[position]);
  }
};
```

上面的代码让non-const成员函数调用const成员函数。其中使用了两次的转型，在non-const operator[]中要调用const operator[]，需要将*this从原始类型TextBlock转型为const TextBlock。两次转型，第一次是为*this添加const，第二次将const operator[]返回值的const移除。

添加const的转型强迫使用了一次安全转型(将non-const对象转为const对象)，所以使用`static_cast`。移除const的动作使用`const_cast`完成。

令const版本调用non-const版本以避免重复的做法是不推荐的。const成员函数承诺绝不改变其对象的逻辑状态，non-const成员函数去没有这般承诺。如果在const函数内调用non-const函数，就是冒了这样的风险。
