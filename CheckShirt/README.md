# Design Your Check Shirt

设计你的衬衫格纹～


```python
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
```


```python
# 设置全局字体
plt.rcParams['font.family'] = "Bradley Hand"
```

注：可以从 https://colorhunt.co 这个网站选择喜欢的颜色，并获取它的十六进制颜色表示。


```python
# 将16进制的颜色转换成 RGB 形式的三维数组
def hex2rgb(hx):
    """returns a RGB array of length 3"""
    return np.array(mcolors.to_rgb(hx))
```

## 最简单的格子


```python
height, width = 60, 80  # 设置矩阵大小
alpha = 0.35            # 条纹透明度，取值 0～1
stride = 5              # 条纹之间的间隔
strip_width = 5         # 条纹宽度
bg = np.ones((height, width, 3)) * hex2rgb("#F6EABE") # 背景颜色
rgb_color_fg = hex2rgb("#87AAAA")  # 格纹颜色矩阵

# 画竖条纹 
for i, loc in enumerate(range(0, bg.shape[1], stride)):
    if i % 2 == 0:
        for _shift in range(strip_width):
            _loc = loc + _shift
            # 以下两行代码将混合格纹颜色和背景颜色，其中格纹颜色占比为 alpha
            bg[:, _loc, :] *= (1 - alpha)
            bg[:, _loc, :] += rgb_color_fg * alpha

# 画横条纹 
for i, loc in enumerate(range(0, bg.shape[0], stride)):
    if i % 2 == 0:
        for _shift in range(strip_width):
            _loc = loc + _shift
            bg[_loc, :, :] *= (1 - alpha)
            bg[_loc, :, :] += rgb_color_fg * alpha
            
fig, ax = plt.subplots()
ax.set_axis_off()  # 去掉边框
ax.imshow(bg)      # 画图
```




    <matplotlib.image.AxesImage at 0x7fb1e0fcbd90>




    
![png](figs/output_6_1.png)
    


加几个字：


```python
# plt.rcParams['font.family'] = "Bradley Hand"         # 设置字体
ax.text(width / 2, height / 2 + 4, "1024",             # 加上“1024”
        ha="center", fontsize=80, color="#6C4A4A")
fig.savefig("1024.png", bbox_inches="tight", dpi=200)  # 保存图片
fig
```




    
![png](figs/output_8_0.png)
    



## 函数打包


```python
def add_vertical_stripes(arr: np.ndarray, color, stride=5, width=None, offset=1, alpha=0.35,):
    """ Add vertical stripes to the given background (`arr`)
    better set `stride` much smaller than ``arr.shape[1] // 2``.
    
    color: RGB array of length 3.
    width: int. width of the strips.
    """
    arr = arr[:, offset:, :]
    end_id = arr.shape[1]
    width = stride if width is None else width
    for i, loc in enumerate(range(0, end_id, stride)):
        if i % 2 == 0:
            for _shift in range(width):
                _loc = loc + _shift
                if _loc >= end_id:
                    break
                arr[:, _loc, :] *= (1 - alpha)
                arr[:, _loc, :] += color * alpha


def add_horizontal_stripes(arr: np.ndarray, color, width=None, stride=5, offset=1, alpha=0.35):
    """ Add horizontal stripes to the given background (`arr`)
    better set `stride` much smaller than ``arr.shape[0] // 2``.
    
    color: RGB array of length 3.
    width: int. width of the strips.
    """
    arr = arr[offset:, :, :]
    end_id = arr.shape[0]
    width = stride if width is None else width

    for i, loc in enumerate(range(0, end_id, stride)):
        if i % 2 == 0:
            for _shift in range(width):
                _loc = loc + _shift
                if _loc >= end_id:
                    break
                arr[_loc, :, :] *= (1 - alpha)
                arr[_loc, :, :] += color * alpha


def image_show(arr, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    ax.imshow(arr)
    ax.set_axis_off()
    return ax
```

## 定制条纹分布的区域

可以在指定的范围内画格子：


```python
height, width = 60, 80
bg = np.ones((height, width, 3)) * hex2rgb("#FEF1E6")

add_vertical_stripes(bg[:, 20: 40, :], color=hex2rgb("#FF9292"), stride=1)
add_horizontal_stripes(bg[20: 40, :, :], color=hex2rgb("#87AAAA"), stride=1)

ax = image_show(bg)
ax.text(width / 2, height / 2 + 4, "1024", ha="center", fontsize=80, color="#C37B89")
```




    Text(40.0, 34.0, '1024')




    
![png](figs/output_12_1.png)
    


## 组合一下

进一步打包上面的函数：


```python
def add_vertical_stripe_groups(
        arr: np.ndarray, color, 
        stride=10, width=None, offset=1,
        sub_stride=1, sub_width=None, alpha=0.35,
):
    """ Add vertical stripes to the given background (`arr`)
    better set `stride` much smaller than ``arr.shape[1] // 2``.
    
    color: RGB array of length 3.
    sub_width: int. width of the strips.
    """
    arr = arr[:, offset:, :]
    end_id = arr.shape[1]
    width = stride if width is None else width
    for i, loc in enumerate(range(0, end_id, stride)):
        if i % 2 == 0:
            add_vertical_stripes(
                arr[:, loc: loc + width, :], color, 
                width=sub_width, stride=sub_stride, 
                alpha=alpha, offset=0)


def add_horizontal_stripe_groups(
        arr: np.ndarray, color, 
        stride=10, width=None, offset=1,
        sub_stride=1, sub_width=None, alpha=0.35,
):
    """ Add vertical stripes to the given background (`arr`)
    better set `stride` much smaller than ``arr.shape[1] // 2``.
    
    color: RGB array of length 3.
    sub_width: int. width of the strips.
    """
    arr = arr[offset:, :, :]
    end_id = arr.shape[1]
    width = stride if width is None else width
    for i, loc in enumerate(range(0, end_id, stride)):
        if i % 2 == 0:
            add_horizontal_stripes(
                arr[loc: loc + width, :, :], color, 
                width=sub_width, stride=sub_stride, 
                alpha=alpha, offset=0)


height, width = 60, 80
bg = np.ones((height, width, 3)) * hex2rgb("#FEF1E6")

v_stride = 11
add_vertical_stripes(bg, color=hex2rgb("#FF9292"), stride=v_stride, width=5, offset=6)
add_vertical_stripe_groups(bg, hex2rgb("#916BBF"), stride=v_stride, width=15)
h_stride = 10
add_horizontal_stripes(bg, color=hex2rgb("#FF9292"), stride=h_stride, width=5, offset=5)
add_horizontal_stripe_groups(bg, hex2rgb("#87AAAA"), stride=h_stride, width=13)
ax = image_show(bg)

ax.text(width / 2, height / 2 + 4, "1024", ha="center", fontsize=80, color="#A2416B")
```




    Text(40.0, 34.0, '1024')




    
![png](figs/output_14_1.png)
    



```python
ax.figure.savefig("happy1024.png", bbox_inches="tight", dpi=200)
ax.figure.savefig("happy1024.pdf", bbox_inches="tight", dpi=200)
```

## DIY

把上面的画图函数进一步打包；也可以根据自己的喜好，组合格子风格～


```python
def simple_grids(bg_color="#F6EABE", 
                 fg_color="#87AAAA", 
                 txt_color="#6C4A4A",
                 stride=5, offset=2, 
                 h=80, w=80, fontsize=60, 
                 ax=None, fname=None, **kwds):
    bg = np.ones((h, w, 3)) * hex2rgb(bg_color) # 背景颜色
    rgb_color_fg = hex2rgb(fg_color)  # 格纹颜色
    add_vertical_stripes(bg, color=rgb_color_fg, stride=stride, offset=offset, **kwds)
    add_horizontal_stripes(bg, color=rgb_color_fg, stride=stride, offset=offset, **kwds)

    ax = image_show(bg, ax=ax)
    ax.text(w / 2, h / 2 + 4, "1024", ha="center", fontsize=fontsize, color=txt_color)
    if fname is not None:
        ax.figure.savefig(fname, bbox_inches="tight", dpi=200)
    return ax


def simple_cross(bg_color="#FEF1E6", 
                 v_color="#FF9292", 
                 h_color="#87AAAA", 
                 txt_color="#6C4A4A",
                 stride=1,
                 h=80, w=80, fontsize=60, 
                 ax=None, fname=None, **kwds):
    bg = np.ones((h, w, 3)) * hex2rgb(bg_color)
    add_vertical_stripes(bg[:, w // 6: w // 6 * 3, :], 
                         color=hex2rgb(v_color), stride=stride, **kwds)
    add_horizontal_stripes(bg[h // 3: h // 3 * 2, :, :], 
                           color=hex2rgb(h_color), stride=stride, **kwds)
    ax = image_show(bg, ax=ax)
    ax.text(w / 2, h / 2 + 4, "1024", ha="center", fontsize=fontsize, color=txt_color)
    if fname is not None:
        ax.figure.savefig(fname, bbox_inches="tight", dpi=200)
    return ax


def pattern1(bg_color="#FEF1E6", 
             v_color="#FF9292", v_group_color="#916BBF",
             h_color=None, h_group_color=None,
             alpha=0.35,
             txt_color="#A2416B",
             h=80, w=80, fontsize=60, 
             ax=None, fname=None,):
    h_color = v_color if h_color is None else h_color
    h_group_color = v_group_color if h_group_color is None else h_group_color

    bg = np.ones((h, w, 3)) * hex2rgb(bg_color)
    v_stride = 11
    add_vertical_stripes(bg, color=hex2rgb(v_color), stride=v_stride, width=5, offset=6)
    add_vertical_stripe_groups(bg, hex2rgb(v_group_color), stride=v_stride, width=15, alpha=alpha)
    h_stride = 10
    add_horizontal_stripes(bg, color=hex2rgb(h_color), stride=h_stride, width=5, offset=5)
    add_horizontal_stripe_groups(bg, hex2rgb(h_group_color), stride=h_stride, width=13, alpha=alpha)
    ax = image_show(bg)
    ax.text(w / 2, h / 2 + 4, "1024", ha="center", fontsize=fontsize, color=txt_color)
    if fname is not None:
        ax.figure.savefig(fname, bbox_inches="tight", dpi=200)
    return ax
    
    
def pattern2(bg_color="#FEF1E6", 
             v_color="#FF9292", v_group_color="#916BBF",
             h_color=None, h_group_color=None,
             txt_color="#A2416B",
             h=80, w=80, fontsize=60, ax=None,
             fname=None,
             ):
    h_color = v_color if h_color is None else h_color
    h_group_color = v_group_color if h_group_color is None else h_group_color

    bg = np.ones((h, w, 3)) * hex2rgb(bg_color)
    v_stride = 11
    add_vertical_stripes(bg, color=hex2rgb(v_color), stride=v_stride, width=15, alpha=0.2)
    add_vertical_stripe_groups(bg, hex2rgb(v_group_color), stride=v_stride, width=5, offset=6, alpha=0.3)
    h_stride = 10
    add_horizontal_stripes(bg, color=hex2rgb(h_color), stride=h_stride, width=15, alpha=0.2)
    add_horizontal_stripe_groups(bg, hex2rgb(h_group_color), stride=h_stride, width=5, offset=6, alpha=0.3)
    ax = image_show(bg)
    ax.text(w / 2, h / 2 + 4, "1024", ha="center", fontsize=fontsize, color=txt_color)
    if fname is not None:
        ax.figure.savefig(fname, bbox_inches="tight", dpi=200)
    return ax

```

以下是一些格子示例，供参考～


```python
pattern1("#FAF3F3", v_color="#E6DDC6", v_group_color="#A7BBC7", txt_color="#A19882", fname="supp1.png")
```




    <AxesSubplot:>




    
![png](figs/output_19_1.png)
    



```python
pattern1("#091353", v_color="#B2F9FC", txt_color="#D5D5D5", fname="supp2.png")
```




    <AxesSubplot:>




    
![png](figs/output_20_1.png)
    



```python
pattern2("#2C2E43", v_group_color="#C6B4CE", v_color="#6E85B2", txt_color="#F1E9E5", fname="supp3.png")
```




    <AxesSubplot:>




    
![png](figs/output_21_1.png)
    



```python
pattern2("#345B63", v_color="#9D84B7", v_group_color="#FFFD95", txt_color="#F1F7E7", fname="supp3.png")
```




    <AxesSubplot:>




    
![png](figs/output_22_1.png)
    



```python
pattern2("#F6EABE", v_color="#9D84B7", v_group_color="#091353", txt_color="#091353", fname="supp4.png")
```




    <AxesSubplot:>




    
![png](figs/output_23_1.png)
    



```python
simple_cross(bg_color="#D5D5D5", 
             v_color="#9D84B7", 
             h_color="#F6EABE", 
             txt_color="#664E88", 
             stride=2, offset=0, alpha=0.6, fname="supp5.png")
```




    <AxesSubplot:>




    
![png](figs/output_24_1.png)
    



```python
simple_grids("#EFEFEF", fg_color="#595260", txt_color="#2C2E43", stride=15, fname="supp6.png")
```




    <AxesSubplot:>




    
![png](figs/output_25_1.png)
    



```python
simple_grids("#EFEFEF", fg_color="#889EAF", txt_color="#A45D5D", fname="supp7.png")
```




    <AxesSubplot:>




    
![png](figs/output_26_1.png)
    



```python
simple_cross("#EEEEEE", h_color="#3C5186", v_color="#835151", fname="supp8.png")
```




    <AxesSubplot:>




    
![png](figs/output_27_1.png)
    



```python
simple_grids("#171717", fg_color="#DA0037", txt_color="#EEEEEE", stride=10, fname="supp9.png")
```




    <AxesSubplot:>




    
![png](figs/output_28_1.png)
    



```python

```


```python
pattern1(fname="main1.png", h_group_color="#87AAAA")
```




    <AxesSubplot:>




    
![png](figs/output_30_1.png)
    



```python
pattern1("#6C4A4A", 
         v_color="#FF9292", v_group_color="#90AACB",
         h_color="#FF9292", h_group_color="#90AACB",
         txt_color="#FEF1E6", alpha=0.4,
         fname="main2.png"
         )
```




    <AxesSubplot:>




    
![png](figs/output_31_1.png)
    



```python
ax = pattern2(fname="main3.png")
```


    
![png](figs/output_32_0.png)
    



```python
pattern2(v_color="#90AACB", h_color="#90AACB", txt_color="#916BBF", fname="main4.png")
```




    <AxesSubplot:>




    
![png](figs/output_33_1.png)
    



```python
pattern2(h_group_color="#87AAAA", v_group_color="#87AAAA", txt_color="#6C4A4A", fname="main5.png")
```




    <AxesSubplot:>




    
![png](figs/output_34_1.png)
    



```python
simple_grids(fname="main6.png")
```




    <AxesSubplot:>




    
![png](figs/output_35_1.png)
    



```python
simple_cross(fname="main7.png")
```




    <AxesSubplot:>




    
![png](figs/output_36_1.png)
    



```python
simple_grids("#A2416B", "#90AACB", "#FEF1E6", fname="main8.png")
```




    <AxesSubplot:>




    
![png](figs/output_37_1.png)
    



```python
simple_grids("#6C4A4A", "#F6EABE", "#F6EABE", stride=25, offset=2, fname="main9.png")
```




    <AxesSubplot:>




    
![png](figs/output_38_1.png)
    



```python
# simple_grids("#C37B89", "#6C4A4A", "black", stride=10, alpha=0.5)
simple_grids("#C37B89", "#6C4A4A", "#F6EABE", stride=10, alpha=0.35, fname="main11.png")
```




    <AxesSubplot:>




    
![png](figs/output_39_1.png)
    



```python
simple_grids("#FEF1E6", "#FF9292", "#90AACB", stride=1, fname="main11.png")
# simple_grids("#FEF1E6", "#FF9292", "#916BBF", stride=1)
```




    <AxesSubplot:>




    
![png](figs/output_40_1.png)
    



```python
simple_cross(bg_color="#90AACB", 
             v_color="#F6EABE", 
             h_color="#FF9292", 
             txt_color="#FEF1E6", 
             stride=2, offset=0, alpha=0.6, fname="main12.png")
```




    <AxesSubplot:>




    
![png](figs/output_41_1.png)
    

