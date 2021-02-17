![来自得到某篇文章](https://img-blog.csdnimg.cn/20210216162117230.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zOTE2NjE4OQ==,size_16,color_FFFFFF,t_70#pic_center)


@[TOC](使用Python制作中文词云)

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 0 素材 & 库 准备
## 0.1 文本和图片
制作词云之前, 我们需要事先准备以下素材:
1. 一篇文章, 以文本文件 (.txt) 格式保存.
2. 停用词表 (英文非必要, 中文需要自己准备, 可以从[这里 (GitHub)](https://github.com/goto456/stopwords)下载).
3. 避免中文乱码的字体文件 (英文非必要)
4. 一张你喜欢的图片. (为词云上色, 或者制作剪影, 非必要)

<font color=#999AAA >完整素材见上面文件.


从素材准备可以看出来, 相比英文, 制作中文词云会稍微麻烦一点, 因为需要解决额外的两个问题:
1. (使用 [jieba](https://github.com/fxsjy/jieba/)) 分词, 将连续的中文句子切割成单个词语.
2. 设置字体, 避免中文乱码.


注:
* 这次例子用的是得到老师王立铭的文章: "《巡山报告》第二十四期：有了疫苗，世界会好吗？"

## 0.2 库准备
主要涉及以下Python库:
*  `wordcloud` (词云制作)
*  `jieba` (中文分词)
* `numpy` (数组处理)
* `matplotlib` (基础画图)
* `PIL` (读取图片)
 
如果没有安装, 需要使用pip或conda进行安装. 如果是在Windows下使用 `pip` 安装, 首先打开命令行 (`cmd`), 进入安装 Python 的文件夹地址, 输入以下代码 (也可以直接使用 Anaconda Powershell Prompt):

<font color=#999AAA >制作词云的库:
```
pip install wordcloud
```
<font color=#999AAA >用于中文分词的库:
```
pip install jieba 
```

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 步骤

1. 准备工作
	1.1. 安装并引入必要的函数库
	1.2. 设置文件路径
2. 文本处理: 分词, 过滤, 词频计算
3. 词云生成, 画图 


## 1. 准备工作
1.1. 引入库

```python
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator#, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import jieba # cutting Chinese sentences into words
```

1.2.设置文件路径

<font color=#999AAA >完整教程涉及四个文件, 见前面的 "素材准备"：

```py
# setting paths
fname_text = 'texts/article.txt'
fname_stop = 'texts/hit_stopwords.txt'
fname_mask = 'pictures/owl.jpeg'
fname_font = 'SourceHanSerifK-Light.otf'
```

## 2. 文本处理
这一步的主要目的是**将一篇文章转化为一个"词频"表** (字典 `dict`).

### 2.1 读取文本
首先, 我们得读取一篇文章, 以及停用词表: 
```py
# read in texts (an article)
text = open(fname_text, encoding='utf8').read()
# Chinese stop words
STOPWORDS_CH = open(fname_stop, encoding='utf8').read().split()
```
初学者需要注意以下几点:
* `open(filename, encoding='utf8')` 命令打开一个文件, 且 ` encoding='utf8'` 告诉计算机该文件的编码方式是 'utf-8', 如果没有这个设定, 会导致中文字符乱码.
* 对打开的文件, `.read()` 操作会返回一个字符串. 因此代码中的 `text` 是字符串类型.
* 最后一行中的 `.split()` 操作将字符串 (按照空格, tab`\t`, 换行符 `\n`) 分割成了一系列字符串, 因此`STOPWORDS_CH` 是一个由字符串组成的列表  `list`.

### 2.2 分词和过滤
首先用 `jieba.cut(text)` 函数将字符串 `text` 分割成一个个词或词组 (该函数返回的是一个'生成器 `generator`), 然后对里面的每一个词, 过滤掉没有意义的 '停用词' (`w not in STOPWORDS_CH`), 最后只保留长度大于1的词组 (`len(w) > 1`).
```py
# processing texts: cutting words, removing stop-words and single-charactors
word_list = [
        w for w in jieba.cut(text) 
        if w not in STOPWORDS_CH and len(w) > 1
        ]
```

### 2.3 统计词频:

下面代码定义了一个函数, 输入一个词语列表, 输出保存每个词语出现频率的字典.
```py
def count_frequencies(word_list):
    freq = dict()
    for w in word_list:
        if w not in freq.keys():
            freq[w] = 1
        else:
            freq[w] += 1
    return freq
freq = count_frequencies(word_list)
```
当然也可以利用 `pandas.value_count()` 函数来计算, 以下代码与上面等价:
```py
import pandas as pd
freq = pd.value_counts(word_list).to_dict()
```


<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">


## 3. 制作并画出词云 
### 3.1 默认颜色
首先用 `WordCloud()` 建立一个词云的对象, 并设置好初始参数 (字体的路径). 然后基于刚刚建立的词频生成词云.
```py
wcd = WordCloud(font_path=fname_font)
wcd.generate_from_frequencies(freq)
```

词云做好之后, 怎么看呢? 需要三行代码:
```py
ax.imshow(wcd)
ax.axis("off")
plt.show()
```
![默认颜色下的词云](https://img-blog.csdnimg.cn/20210217145522867.png)

当然我个人习惯性把常用代码打包:
```py
def plt_imshow(x, ax=None, show=True):
    if ax is None:
        fig, ax = plt.subplots()
    ax.imshow(x)
    ax.axis("off")
    if show: plt.show()
    return ax
plt_imshow(wcd)
```

### 3.2 设置背景颜色
我们可以通过修改参数 `background_color` 来设置背景颜色, 比如把背景改成白色:
```py
wcd = WordCloud(font_path=fname_font, 
                background_color='white',
                )
plt_imshow(wcd)
```
![将背景颜色改成白色](https://img-blog.csdnimg.cn/20210217150838194.png)


### 3.3 从图片提取颜色
我们也可以选择自己喜欢的图片作为背景色:

![猫头鹰](https://img-blog.csdnimg.cn/20210217152334973.png)

 - 首先读取图片, 将其转化为 RGB 数组;  
 - 然后用 `ImageColorGenerator` 从中提取颜色, 它会得到一个颜色生成器, 依照每个词所占的矩形区域的颜色平均来确定改词最终的颜色.

```py
# processing image
im_mask = np.array(Image.open(fname_mask))
im_colors = ImageColorGenerator(im_mask)
```
准备好了, 生成词云. 相比上面代码有两处修改: 
1. 设置图片底板 `mask=im_mask`;
2. 重新对每个词染色 `wcd.recolor(color_func = im_colors)`
```py
wcd = WordCloud(font_path=fname_font, 
                background_color='white',
                mask=im_mask,
                )
wcd.generate_from_frequencies(freq)
wcd.recolor(color_func = im_colors)
ax = plt_imshow(wcd,)
```
看效果吧~

![从图片提取颜色](https://img-blog.csdnimg.cn/20210217151102736.png)

如果想要保存图片:
```py
ax.figure.savefig(f'conbined_wcd.png', bbox_inches='tight', dpi=150)
```
* `bbox_inches='tight'` 可以确保你保存的图片形状合适.

当然, 我们还可以来个拼图:
```py
fig, axs = plt.subplots(1, 2)
plt_imshow(im_mask, axs[0], show=False)
plt_imshow(wcd, axs[1])
```
![pinjietupian](https://img-blog.csdnimg.cn/20210217153542211.png)

保存图片:
```py
fig.savefig(f'conbined_wcd.png', bbox_inches='tight', dpi=150)
```

# 完整代码

```python
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator#, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import jieba # cutting Chinese sentences into words


def plt_imshow(x, ax=None, show=True):
    if ax is None:
        fig, ax = plt.subplots()
    ax.imshow(x)
    ax.axis("off")
    if show: plt.show()
    return ax

def count_frequencies(word_list):
    freq = dict()
    for w in word_list:
        if w not in freq.keys():
            freq[w] = 1
        else:
            freq[w] += 1
    return freq

if __name__ == '__main__':
    # setting paths
    fname_text = 'texts/article.txt'
    fname_stop = 'texts/hit_stopwords.txt'
    fname_mask = 'pictures/owl.jpeg'
    fname_font = 'SourceHanSerifK-Light.otf'
    
    # read in texts (an article)
    text = open(fname_text, encoding='utf8').read()
    # Chinese stop words
    STOPWORDS_CH = open(fname_stop, encoding='utf8').read().split()
    
    # processing texts: cutting words, removing stop-words and single-charactors
    word_list = [
            w for w in jieba.cut(text) 
            if w not in STOPWORDS_CH and len(w) > 1
            ]
    freq = count_frequencies(word_list)
    
    # processing image
    im_mask = np.array(Image.open(fname_mask))
    im_colors = ImageColorGenerator(im_mask)
    
    # generate word cloud
    wcd = WordCloud(font_path=fname_font, # font for Chinese charactors
                    background_color='white',
                    mode="RGBA", 
                    mask=im_mask,
                    )
    #wcd.generate(text) # for English words
    wcd.generate_from_frequencies(freq)
    wcd.recolor(color_func = im_colors)
    
    # visualization
    ax = plt_imshow(wcd,)
    ax.figure.savefig(f'single_wcd.png', bbox_inches='tight', dpi=150)
    
    fig, axs = plt.subplots(1, 2)
    plt_imshow(im_mask, axs[0], show=False)
    plt_imshow(wcd, axs[1])
    fig.savefig(f'conbined_wcd.png', bbox_inches='tight', dpi=150)

```

