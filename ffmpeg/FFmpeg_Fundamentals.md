# FFmpeg

## 0x01 FFmpeg组成

FFmpeg是用于多媒体处理的开发软件库，基于GNU GPL发布。`FF`为`Fast Forward`的缩写，`mpeg`为`Moving Pictures Experts Group`的缩写。

- 命令行工具
 - ffmpeg，用来对音频和视频进行编码和解码。
 - ffplay，用来播放音频和视频。
 - ffprobe, 多媒体流分析工具。
 - ffserver, 提供多媒体流广播服务，支持HTTP和RTSP协议。
- 库
 - libavcodec, 编解码库。
 - libavdevice, 输入输出设备库。
 - libavfilter, 多媒体过滤器库。
 - libavformat, 多媒体封装格式库。
 - libavutil, 实用工具库。
 - libpostproc, 后处理库。
 - libswresample, 音频采样库。
 - libswscale, 图像缩放、颜色空间转换、像素格式转换库。

## 0x02 FFmpeg的开发者

FFmpeg项目始于2000年，由Fabrice Bellard创建，Fabrice Bellard创建的其他知名项目有QUMU，TCC(Tiny C Compiler)。FFmpeg现在由FFmpeg项目组进行维护开发，开发成员来自不同的国家。

## 0x03 参与FFmpeg的开发

任何人都可以加入到FFmpeg的开发当中，访问如下页面[Join development][ffmpeg_contact]。

## 0x04 FFmpeg下载

FFmpeg源码下载：http://ffmpeg.org/download.html。

Windows用户下载：https://ffmpeg.zeranoe.com/builds/。

## 0x05 命令的基本语法

FFmpeg命令的语法非常简洁，重要的是在正确的位置输入必须的参数，而且不要将输入参数和输出参数混淆。基本语法如下：

```shell
ffmpeg [global options] [input file options] -i input_file [output file options] output_file
```

**NB**: `global options`影响输入与输出。

如果有多个输入与输出参数，则：
```shell
ffmpeg global_options input1_options -i input1 input2_options -i input2 output1_options output1 output2_options output2
```

## 0x06 显示输出

对于视频的测试，我们希望直接看到处理的结果，而不是将其保存为文件。

### 使用ffplay进行视频播放

对于如下的命令：

```shell
ffmpeg -i input_file ... test_options ... output_file
```

使用如下命令进行视频的预览：

```shell
ffplay -i input_file ... test_options
```

### 使用SDL进行视频播放

```shell
ffmpeg -i input_file -pix_fmt yuv420p -f sdl title
```

SDL只能显示格式为`yuv420p`的图像，使用`-pix_fmt`指定输出为`yuv420p`，`title`是显示窗口的标题。

## 0x07 国际单位

当指定比特率或者文件大小时，需要输入很多的数字，可以使用国际单位后缀，`K`表示10<sup>3</sup>，`M`表示10<sup>6</sup>，`G`表示10<sup>9</sup>等。

如下命令都是等效的：

```shell
ffmpeg -i input.avi -b:v 1500000 output.mp4
ffmpeg -i input.avi -b:v 1500K output.mp4
ffmpeg -i input.avi -b:v 1.5M output.mp4
ffmpeg -i input.avi -b:v 0.0015G output.mp4
```

`B`表示字节，可以和上面介绍的`K`,`M`等一同使用，如指定输出为10000000字节：

```shell
ffmpeg -i input.avi -fs 10MB output.mp4
```      

FFmpeg还支持其他的一些标准的单位，到具体使用时再进行介绍。

## 0x08 ffmpeg转码

ffmpeg程序将使用`-i`参数指定的输入内容读入内存，根据输入参数和默认参数进行处理，然后将结果写到不同的输出中。输入和输出都可以是文件、管道、网络流、抓取设备等。

在转码过程中，ffmpeg调用`libavformat`中的分离器(demuxer)，从输入中读取编码的数据包(package)。如果有多个输入，ffmpeg会将其进行同步读取，接着解码器(decoder)从得到的包中解压出帧(frame)，然后应用必要的过滤器(filter)，将frame发送给编码器(encoder)，enoder编码出新的package，最发送给混流器(muxer)，并写到输出。

通过上面的描述可以看到，在FFmpeg中最重要的工具是过滤器(filter)。filter可以组织成过滤器链(filterchains)或者过滤器图(filtergraphs)。filtergraphs可以很简单，也可以很复杂。filter是在decoding和encoding之间执行的。整个过程如下图所示。

![transcoding][transcoding]

## 0x09 过滤器，过滤器链和过滤器图

在多媒体处理中，过滤器意味着一种在编码输出之前对输入进行修改的软件工具。过滤器分为音频过滤器和视频过滤器。FFmpeg有许多内建的过滤器，可以将它们组合进行使用。复杂的命令可以直接将frame从一个过滤器传递给另一个过滤器，这可以简化多媒体处理流程，而且减少编解码的处理次数，减少视音频质量的下降。过滤器使用的`libavfitler`库，它允许多个输入与输出。使用`-vf`参数引入视频过滤器(video filter)，使用`-af`参数引入音频过滤器(audio filter)。如下命令将视频顺时针旋转90度：

```shell
ffplay -f lavfi -i testsrc -vf transpose=1
```



[ffmpeg_contact]:http://www.ffmpeg.org/contact.html
[ffmpeg_website]:http://ffmpeg.org/download.html
[transcoding]:https://raw.githubusercontent.com/Furzoom/booknote/master/images/ffmpeg/ffmpeg_basic.png
