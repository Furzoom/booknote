# FFmpeg基础

FFmpeg是用于多媒体处理的开发软件库，基于GNU GPL发布。`FF`为`Fast Forward`的缩写，`mpeg`为`Moving Pictures Experts Group`的缩写。

## 0x01 术语

- **容器**(Container)，容器就是一种文件格式，比如flv，mkv等，包含流及文件头信息。
- **流**(Stream)，是一种视频数据信息的传输方式，包含：音频，视频，字幕，附件，数据。
- **帧**(Frame)，帧代表一幅静止的图像，分为I帧、P帧、B帧。
- **编解码器**(Codec)，是对流进行压缩或者解压缩的工具，CODEC是code和decode的合成。
- **混流**/**分离**(Mux/Demux)，混流为把不同的流按照容器的规则放入容器。分离是把不同的流从容器中解析出来。

## 0x02 FFmpeg组成

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

## 0x03 FFmpeg处理流程

![Transcoding][transcoding]

## 0x04 Filter

Filter的意思是被编码到输出文件之前用来修改输入文件内容的一个工具。如：视频翻转，旋转，绽放等。

- 视频过滤器`-vf`
 - 视频左右翻转播放，命令`ffplay -i testvideo.wmv -vf hflip`。
 - 视频上下翻转播放，命令`ffplay -i testvideo.wmv -vf vflip`。
 - 视频顺时针旋转90度播放，命令`ffplay -i testvideo.wmv -vf transpose=1`。
 - 视频逆时针旋转90度播放，命令`ffplay -i testvideo.wmv -vf transpose=2`。
 - transpose参数值：
   - 0，表示逆时针旋转90度，然后垂直翻转。
   - 1，表示顺时针旋转90度。
   - 2，表示逆时针旋转90度。
   - 3，表示顺时针旋转90度，然后水平翻转。
- 音频过滤器`-af`
 - 以1.2倍的速度播放音频，命令`ffplay -i testaudio.mp3 -af atempo=1.2`。


还有更复杂的Filter，如FilterChain, FilterGraph。

## 0x05 视频基础知识

- 帧率，也称为帧频率，是视频文件中每一秒的帧数，肉眼想看到连续移动图像至少需要15帧。
- 码率，也称为比特率，是一个确定整体视频/音频质量的参数，是每秒处理的字节数。码率与视频质量成正比，使用`bps`来表示。

使用参数`-r`设置帧率，`ffmpeg -i input -r fps output`。帧率的预定义值：

Abbreviation | Exact value | Corresponding FPS
--- | --- | ---
ntsc-film | 24000/1001 | 23.97
film | 24/1 | 24
pal, qpal, spal | 25/1 | 25
ntsc, qntsc, sntsc | 30000/1001 | 29.97

使用参数`-b`设置码率，`ffmpeg -i input -b 1.5M output`。音频使用`-b:a`，视频使用`-b:v`。

## 0x06 视频分辨率

使用`-s`设置视频的分辨率，参数值为`wxh`，`ffmpeg -i input -s 640x480 output`。

也可以使用Filter进行调解，`ffmpeg -i input -vf scale=640:480 output`。二者是等效的。

如果想将视频分辨设置为原来的大小的一半，使用`ffmpeg -i input -vf scale=iw/2:ih/2 output`。

为保证原始比例，且不知道输入视频的分辨率时，使用:

```shell
# 固定宽度400
ffmpeg -i input -vf scale=400:400/a output
ffmpeg -i input -vf scale=400:-1 output

# 固定高度300
ffmpeg -i input -vf scale=-1:300 output
ffmpeg -i input -vf scale=300*a:300 output
```

## 0x06 裁剪视频(crop)

从输入文件中选取想要的矩形区域到输出文件中，常用来去除视频轩边。

语法：`-vf crop=ow[:oh[:x[:y[:keep_aspect]]]]`。

`x`默认值是`(iw - ow)/2`，同理`y`默认值是`(ih - oh)/2`。

`ffplay -i input -vf cropdetect`自动检测黑边尺寸，然后可以进行黑边剪裁。

## 0x07 填充视频(pad)

在视频帧上增加一块额外区域，经常用在播放的时候显示不同的横纵比。

语法：`-vf pad=width[:height[:x[:y[:color]]]]`。

`width`默认为`iw`，`height`默认为`ih`，`x`默认为0，`y`默认为0，`color`默认为`black`。

如：`ffplay -i input -vf pad=848:412:0:30:pink`，在原视频`848x352`的上下边添加30像素粉边。

## 0x08 改变横纵比

视频由16：9变为4：3，为保证不切掉有用的信息，宽度不变，将高度进行填充。使用如下命令：`ffplay -i input -av pad=iw:iw*3/4:0:(oh-ih)/2:pink`。

同理，如果将4：3的视频变为16：9，则需要保持高度不变，将宽度方向进行填充，使用如下命令：`ffplay -i input -av pad=ih*16/9:ih:(ow-iw)/2:0:pink`。

## 0x09 模糊与锐化

模糊语法：`-vf boxblur=luma_r:luma_p[:chroma_r:chroma_p[:alpha_r:alpha_p]]`。

锐化语法：`-vf unsharp=l_msize_x:l_msize_y:l_amount:c_msize_x:c_msize_y:c_amount`。默认值为`5:5:1.0:5:5:0.0`。

- `l_msize_x`,水平亮度矩阵，取值范围3～13,默认值为5。
- `l_msize_y`,垂直亮度矩阵，取值范围3～13,默认值为5。
- `l_amount`,亮度强度，取值范围-2.0~5.0,负数为模糊效果，默认值为1.0。
- `c_msize_x`,水平色彩矩阵，取值范围为3～13,默认值为5。
- `c_msize_y`,垂直色彩矩阵，取值范围为3～13,默认值为5。
- `c_amount`,色彩强度，取值范围-2.0~5.0，负数为模糊效果，默认值0.0。

## 0x09 覆盖

语法：`-filter_complex overlay[=x[:y]]`，所有参数都是可选的，默认值为0。其中使用`W`和`H`表示较大视频的尺寸，`w`和`h`表示较小视频的尺寸。

删除logo，`-vf delogo=x:y:w:h[:t[:show]]`。`x:y`离左上角的坐标，`w:h`logo的宽和高，`t`矩形边缘的厚度，默认值为4。`show`若设置为1,显示一个绿色的矩形，默认值为0。

## 0x10 添加文本

语法：`-vf drawtext=fontfile=font_f:text=text1:textfile=ff:fontsize=fs:fontcolor:fc:x=x1:y=y1:t=t1:n=n1:enable=0`。

- `fontfile`，指定字体文件。
- `text`，指定文本内容。
- `textfile`，指定文本文件。
- `fontsize`，指定字体大小。
- `fontcolor`，指定字体颜色。
- `x`，指定横坐标。
- `y`，指定纵坐标。
- `t`表示时间。
- `n`表示帧数。
- `enable`，控制文本显示，为1表示显示，0表示不显示。

如下，在在上角显示当前时间
```shell
ffplay -i sintel.wmv -vf drawtext="fontfile=/usr/share/fonts/truetype/freefont/FreeMono.ttf:text='%{localtime\:%H}\:%{localtime\:%M}\:%{localtime\:%S}':fontcolor=green"
```

## 0x11 图片处理

FFmpeg支持绝大多数图片处理。除LJPEG之外，其他都能被解码，除了EXR，PIC，PTX外，都能被编码。

### 截取图片

使用`-ss`参数，表示`seek from start`。

```shell
ffmpeg -ss 00:00:10 -i input image.jpg
```

### 从视频生成gif

```shell
ffmpeg -i input -t 10 -pix_fmt rbg24 image.gif
```

### 视频转图片

```shell
ffmpeg -i input frame%4d.jpg
```

### 图片转视频

```shell
ffmpeg -f image2 -i img%4d.jpg -r 25 video.mp4
```

### 图像裁剪

```shell
ffmpeg -i input -vf crop=150:150 cropped.jpg
```

### 图像填充

```shell
ffmpeg -i input -vf pad=360:280:20:20:orange pad_img.jpg
```

### 图像翻转

```shell
ffmpeg -i input -vf hflip image.jpg
ffmpeg -i input -vf vflip image.jpg
```

### 图像旋转

```shell
ffmpeg -i input -vf transpose=1 image.jpg
```

### 图像覆盖

```shell
ffmpeg -i input -s 400x300 rgb.png
```

## 0x12 其他

### 屏幕录像

```shell
ffmpeg -f x11grab -r 25 -s 800x600 -i :0.0 out.mkv
```

### 添加字幕

```shell
ffmpeg -i input -vf subtitles=rgb.srt output.mkv
```

该方法是将字幕添加到视频的封装格式，并不是所有的容器都支持字幕流。

### 将视频转为黑白

```shell
ffmpeg -i input -vf lutyuv="u=128:v=128" output.mkv
```

### 变速播放

视频3倍速度播放：
```shell
ffplay -i input -vf setpts=PTS/3
```

音频2倍速度播放：
```shell
ffplay -i input.mp3 -af atempo=2
```

### 截图

每隔1秒截图一张：
```shell
ffmpeg -i input.avi -f image2 -vf fps=fps=1 out%d.png
```

每隔20秒截图一张：
```shell
ffmpeg -i input.avi -f image2 -vf fps=fps=1/20 out%d.png
```





[transcoding]:https://raw.githubusercontent.com/Furzoom/booknote/master/images/ffmpeg/ffmpeg_basic.png
