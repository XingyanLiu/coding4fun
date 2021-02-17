# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:42:14 2021

@author: Cynthia
"""

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


# In[]
if __name__ == '__main__':
    # setting paths
    fname_text = 'texts/article.txt'
    fname_stop = 'stopwords/hit_stopwords.txt'
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

