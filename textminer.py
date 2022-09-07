# from unittest import result
from cgitb import text
from pydoc import tempfilepager
from tempfile import tempdir
import pandas as pd
# import nltk
from nltk.tokenize import word_tokenize as wt
from nltk.corpus import stopwords
import re
import emoji

# nltk.download('stopwords')
# nltk.download('punkt')

# 이모지 제거 전처리 // source : https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
def remove_emoji(string):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', string)

# 이모지 제거 전처리 2
def give_emoji_free_text(text):
    # allchars = [str for str in text.decode('utf-8')]
    # emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    emoji_list = [c for c in text if c in emoji.distinct_emoji_list(text)]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text


def del_stopword(text):
    stopWordList = ['à','et','en', 'détail', 'contactez', 'nous', 'suis', 'un', 'peu', 'de', 'problème', 'proposez', 'num', ',','!', '?', 'show' ]
    clean_text = ' '.join([str for str in text.split() if any(i in str for i in stopWordList)])
    return clean_text


def get_contents(RAWDATA_PATH):
    df = pd.read_excel(RAWDATA_PATH)
    contents = df["postDetail"].to_list()

    #stopwords set up

    temp = []
    for line in contents:
        line = line.lower()
        line = give_emoji_free_text(line)
        line = remove_emoji(line)
        temp.append(line)

    out = pd.DataFrame(temp, columns=['content'], dtype='string')
    out.drop_duplicates(['content'], keep='first', ignore_index=True, inplace= True)
    out.dropna()

    dic = {}
    temp = []
    for line in out['content']:
        line = line.split(' ')
        temp.append(line)
        
    dic["raw"] = out['content'].to_list()
    dic["word"] = temp

    out = pd.DataFrame(dic, dtype="object")
    
    return out

RAWDATA_PATH = "facebookData.xlsx"
df = get_contents(RAWDATA_PATH)
# df.to_csv("facebookData")
price = []
product = []
memory = []
battery = []

product_list = ['iphone', '5s', '6','6s','6+', '6s+', '7', '7+', '8',' 8+', 'se', 'x', 'xs', 'max', 'xr', '11','pro', 'promax', '12' ,'mini', 'spark', 's16', 's8', 'samsung', 'a36']

for line in df["word"]:
    price.append([text for text in line if '$' in text])
    product.append([text for text in line if any(i in text for i in product_list) ])
    # [text for text in line if any(i in str for i in stopWordList)]
    memory.append([text for text in line if 'gb' in text])
    battery.append([text for text in line if '%' in text])

dic = {}
dic["price"] = price
dic["product"] = product
dic["memory"] = memory
dic["battery"] = battery

df = pd.DataFrame(dic, dtype="object")
df.to_excel("outputData.xlsx")