# 进行操作系统开发常用工具使用方法

## 二进制文件编辑与查看

### 使用vim编辑二进制文件

* 打开文件时使用`-b`参数，或者打开文件时执行命令`:set binary`。
* 对文件进行转换`:%!xxd -g 1`。
* 编辑文件。
* 将文件转换回来`:%!xxd -r`。
* 保存文件。

### Bless

### 查看

- hexdump -C
- xxd


## 写映像文件

生成512字节文件：

```shell
$ dd if=/dev/zero of=a.img bs=512 count=1
```

生成空的1.44M的软盘：

```shell
$ dd if=/dev/zero of=a.img bs=512 count=2880
```

将引导扇区写入软盘映像：

```shell
$ dd if=bootloader of=a.img bs=512 count=1 conv=notrunc
```

参数`conv=notrunc`表示不截断输出文件。


## 汇编

### 汇编命令

汇编文件：

```shell
$ nasm boot.asm -o boot.bin
```

反汇编:

```shell
$ ndisasm -o0x7c00 boot.bin
```

### NASM汇编语法

#### []

在NASM中任何没有放在`[]`中的变量和标签都代表地址，访问标签中的内容使用`[tag]`。

```asm
foo dw 1
mov ax, foo   ; 传送的是地址
mov ax, [foo] ; 传送的是foo的内容，也就是1
```

标签与变量的一样的，如下两行等价：

```asm
foo dw 1
foo: dw 1
```

#### $与$$

$表示当前行被汇编后的地址。
