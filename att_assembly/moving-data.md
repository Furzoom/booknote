# Moving Data

## Defining Data Elements

### The data section

- `.ascii`
- `.asciz`
- `.byte`
- `.double`
- `.float`
- `.int`
- `.long`
- `.octa`
- `.quad`
- `.short`
- `.single`

```asm
.section .data
msg:
  .ascii "This is line"
height:
  .int 24, 30
```

### Defining static symbols

The `.equ` directive is used to set a constant value to a symbol that can be
used in the text section. Once set, the data symbol value cannot be changed.

```asm
.equ factor, 3
.equ LINUX_SYS_CALL, 0x80
```

To reference the static data element, you must use a dollar sign before the
label name. For example

```asm
movl $LINUX_SYS_CALL, %eax
```

### The bss section

The data declared in the bss section is not included in the executable
program.

- `.comm`, not initialized.
- `.lcomm`, local, not initialized.

While the two sections work similarly, the local common memory area is
reserved for data that will not be accessed outside of the local assembly
code.

```asm
.section .bss
.comm symbol, length
.comm buffer, 100
```

## Moving Data Elements

The `mov` instruction formats

```asm
movx source, destination
```

movx, where x can be the following:

- `l`, for a 32-bit long word value
- `w`, for a 16-bit word value
- `b`, for an 8-bit byte value

`mov` instruction rules:

- An immediate data element to a general-purpose register
- An immediate data element to a memory location
- A general-purpose register to another general-purpose register
- A general-purpose register to a segment register
- A segment register to a general-purpose register
- A general-purpose register to a control register
- A control register to a general-purpose register
- A general-purpose register to a debug register
- A debug register to a general-purpose register
- A memory location to a general-purpose register
- A memory location to a segment register
- A general-purpose register to a memory location
- A segment register to a memory location

### Using indexed memory locations

Indexed memory location foramt is

```asm
base_address(offset_address, index, size)
```

The data value retrived is located at 
`base_address + offset_address + index * size`.

The `offset_address` and `index` value must be registers.

```asm
.section .data
values:
  .int 1, 2, 3, 4
.section .text
  movl $2, %edi
  movl values(, %edi, 4), %eax
```

## Conditional Move Instructions

### The `CMOV` instructions

```asm
cmovx source, destination
```


