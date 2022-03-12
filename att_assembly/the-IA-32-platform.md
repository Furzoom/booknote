# The IA-32 Platform

Processor, system memory, input devices, output devices.

## Processor

Processor consists of Control Unit, Execution Unit, Registers, Flags.

## Control unit

Control unit: Instruction prefetch and decoding, branch prediction, 
out-of-order execution, retirement.

## Execution unit

Execution unit (ALU): simple-integer operations, complex-integer operations, 
floating-point operations.

## Registers

Registers: general purpose(8), segment(6), instruction pointer(1), 
floating-point data(8), control(5), debug(8).

### General purpose registers

- EAX, Accumulator for operands and results data.
- EBX, Poiter to data in the data memory segment.
- ECX, Counters for string and loop operands.
- EDX, I/O pointer.
- EDI, Data pointer for destination of string operations.
- ESI, Data pointer for source of string operations.
- ESP, Stack pointer.
- EBP, Stack data pointer.

### Segment registers

Methods to access system memory:

- Flat memory model.
- Segmented memory model.
- Real-address model.

Each memory location is accessed by a specific addresss, called 
*linear addresss* in Flat memory model

Memory locations in segmented memory are defined by *logical addresses*. 
A logical address consists of a segment address and an offset address. 
The processor translates a logical address to a corresponding linear address 
location to access the byte of memory.

The segment registers are used to contain the segment address for specific data
access.

- CS, Code segment.
- DS, Data segment.
- SS, Stack segment.
- ES, Extra segment pointer.
- FS, Extra segment pointer.
- GS, Extra segment pointer.

All segment registers are 16 bits.

If a program is using the real address model, all of the segment registers
point to the zero linear address, and are not changed by the program. All
instruction codes, data elements, and stack elements are accessed directly
by their linear address.

### Instruction pointer register

(E)IP. In a flat memory model, the instruction pointer contains the linear
address of the memory location for the next instruction code. If the 
application is using a segmented memory model, the instruction pointer
points to a logical memory address, referenced by the coutents of the CS 
register.

### Control registers

- CR0, System flags that control the operating mode and status of the processor.
- CR1, Not currently used.
- CR2, Memory page fault information.
- CR3, Memory page directory information.
- CR4, Flags that enable processor features and indicate feature capabilities of the processor.
## Flags 
- Status falgs.
- Control flags.
- System flags.

### Status flags

The status flags are used to indicate the results of a mathematical operation
by the processor.

- CF, Carry flag. (Unsigned).
- PF, Parity flag.
- AF, Adjust flag. (BCD mathematical operation).
- ZF, Zero flag.
- SF, Sign flag.
- OF, Overflow flag. (Signed).

### Control flags

- DF, Directory flag.

### System falgs

- TF, Trap flag.
- IF, Interrupt enable flag.
- IOPL, I/O privilege level flag.
- NT, Nested task flag.
- RF, Resume flag.
- VM, Virtual-8086 mode flag.
- AC, Aligment check flag.
- VIF, Virtual interrupt flag.
- VIP, Virtual interrupt pending flag.
- ID, Identification flag.

## Advanced IA-32 Features

### x87 FPU

FPU(floating-point unit).

### MMX

MMX(Multimedia extensions) was the first technology to support the Intel
Single Instruction, Multiple Data(SIMD) execution model.

The MXX environment includes trhee new floating-point data types that can
be handled by the processor:

- 64-bit packed byte integers.
- 64-bit packed word integers.
- 64-bit pcaked doubleworl integers.

The MMX registers are named MM0 through MM7.

### Streaming SIMD extensions (SSE)

Introduced eight ewn 128-bit registers called XMM0 through XMM7 and a new
data type - a 128-bit packed single-precision floating-point.

SSE2 used the same XMM registers that SSE uses, and also introduces five
new data types.

- 128-bit packed double-precision floating point.
- 128-bit packed byte integers.
- 128-bit packed word integers.
- 128-bit packed doubleword integers.
- 128-bit packed quadword integers.

