# Tkinter

## Toplevel

```python
Toplevel()
```

- 主顶层，作为根被引用。
- 子顶层，依赖于根，若根被销毁，则子顶层也被销毁。
- 临时顶层，总是画于父顶层的顶部。如果父顶层被最小化，则它们也被最隐藏。
- 将顶层使用`overrideredirect()`设置为非零值，则该窗口不能被绽放或拖动。

## Frame

Frame是个容器，常用于几何管理器处理一组控件。

relief设置：

- RAISED
- SUNKEN
- FLAT
- RIDGE
- GROOVE
- SOLID

## Label

Label用于显示文本或者图像。文本可以根据Label的宽度进行自动换行，或者使用换行符进行强制换行。

## Button

严格来说，Button是对鼠标和键盘事件起反应的标签。可以绑定事件。可以包含文本和图像。

## Entry

Entry是用来收集用户输入的基本控件。被限制在公能容纳一种字体的单行文本范围内。
