# from os import path
#
# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# hadoop_mast =np.array(Image.open(path.join('./static/images/',"2.png")))
#
# text= "的啊 是 周 周 的 c "
# wc=WordCloud(background_color="white",repeat=True,mask=hadoop_mast)
# wc.generate(text)
# plt.axis("off")
# plt.imshow(wc,interpolation="bilinear")
# plt.show()
# wc.to_file("./files/world_cloud_images/world_cloud01.png")

# from pyspark.sql import SparkSession
# spark=SparkSession.builder.appName('saprk')
#
# from os import path
# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator

from operator import add
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator  # , STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import jieba  # cutting Chinese sentences into words


def plt_imshow(x, ax=None, show=True):
    if ax is None:
        fig, ax = plt.subplots()
        #不显示出来
    ax.imshow(x)
    ax.axis("off")
    #if show: plt.show()
    return ax


def count_frequencies(word_list):
    freq = dict()
    for w in word_list:
        if w not in freq.keys():
            freq[w] = 1
        else:
            freq[w] += 1
    return freq


#if __name__ == '__main__':
    # setting paths
def world_cloud(key):
    fname_text='./files/scrapy_files/'
    fname_text=fname_text+key+'.txt'
    #fname_text = './files/scrapy_files/lagou.txt'

    fname_stop = './static/cn_stopwords.txt'

    fname_mask = './static/images/公路.jpg'
        #'./static/images/词云.png'
    fname_font = 'C:/Windows/Fonts/simkai.ttf'
        #'SourceHanSerifK-Light.otf'

    # read in texts (an article)
    text = open(fname_text, encoding='utf8').read()
    # Chinese stop words
    STOPWORDS_CH = open(fname_stop, encoding='utf8').read().split()

    # processing texts: cutting words, removing stop-words and single-charactors
    word_list = [
        w for w in jieba.cut(text)
        if w not in set(STOPWORDS_CH) and len(w) > 1
    ]
    freq = count_frequencies(word_list)

    # processing image
    im_mask = np.array(Image.open(fname_mask))
    im_colors = ImageColorGenerator(im_mask)

    # generate word cloud
    wcd = WordCloud(font_path=fname_font,  # font for Chinese charactors
                    background_color='white',
                    mode="RGBA",
                    mask=im_mask,
                    )
    # wcd.generate(text) # for English words
    wcd.generate_from_frequencies(freq)
    wcd.recolor(color_func=im_colors)

    # visualization
    ax = plt_imshow(wcd, )
    images_path='./static/images/scrapy_files/'
    images_path=images_path+key+'.png'
    ax.figure.savefig(images_path, bbox_inches='tight', dpi=150)


