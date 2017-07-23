# Important Note

- 除非有一个好理由允许构造函数被用于隐式类型转换，否则就把它声明为`explicit`。
- copy构造函数是一个重要的函数，它定义了一个对象如何passed by value。
- 以by value传递用户自定义类型通常是个坏主意，Pass-by-reference-to-const往往是比较好的选择。
- 对于单纯常量，最好使用const对象或enums替换#define。
- 对于形似函数的宏(macros)，最好改用inline函数替换#define。
- 为内置类型对象进行手工初始化，因为C++不保证初始化它们。
- 构造函数最好使用成员初始化列表，而不要在构造函数内本体内使用赋值操作。初始化列表中成员变量，其排列次序应该和它们在class中的声明次序相同。
- 为避免跨编译单元初始化次序问题，请使用local static对象替换non-local static对象。
- 编译器会默认为类生成default构造函数、copy构造函数、copy assignment操作符，以及析构函数。这些函数都是public且inline的。default函数只要没有声明任何构造函数时才会被生成。
-
