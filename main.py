
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import warnings
from nltk import FreqDist
warnings.simplefilter(action='ignore', category=FutureWarning)
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download("averaged_perceptron_tagger")
import itertools


# random sample of 10,000 records from past 12 weeks of workorder data
df = pd.read_csv(r'C:\Users\ssingh2\Documents\sampleWoDf.csv')

# function that takes in list of strings (sentences) and returns list of list of tokens (~words)
# i.e. ['   ', '', ''] becomes [[' ', '  '], [''], ['']]
def tokenize(list):
    tokenizedSents = []
    for sent in list:
        if isinstance(sent, str):
            tokenizedSent = nltk.word_tokenize(sent)
            tokenizedSents.append(tokenizedSent)
    return tokenizedSents

# function that takes in list of list of tokens and returns list with blank strings replacing
# any "stop words"
def filterStopWords(tokens):
    stop_words = set(stopwords.words("english"))
    finalFiltered = []

    for t in tokens:
        filtered = []
        for word in t:
            temp = ''
            if word.casefold() not in stop_words:
                temp += word
            filtered.append(temp)
        finalFiltered.append(filtered)
    return finalFiltered

# function which takes in a series (i.e. descriptions grouped by location), tokenizes and filters items (i.e.
# descriptions) in series, places them in a dictionary with keys as series values (i.e. location)
def createDictionary(series):
    dict = {}
    for location, descriptions in series.items():
        tokenized = tokenize(descriptions)
        filtered = filterStopWords(tokenized)
        concatenated = list(itertools.chain.from_iterable(filtered))
        dict[location] = concatenated
    return dict

# creates a frequency distribution of words per location
def createFreqDist(dict):
    freqDict = {}
    for key in dict:
        fd = FreqDist(word_tokenize(' '.join((dict[key]))))
        freqDict[key] = fd
    return freqDict

# creates
def createPOSTags(dict):
    posDict = {}
    for key in dict:
        pt = nltk.pos_tag(word_tokenize(' '.join((dict[key]))))
        posDict[key] = pt
    return posDict

# use above functions to perform desired analysis
# groups descriptions by location
df['DESCRIPTION'] = df['DESCRIPTION'].str.lower()
dbl = df.groupby(['LOCATION'])['DESCRIPTION'].apply(list)
# create frequency distribution
dblProcessed = createDictionary(dbl)
freqDict = createFreqDist(dblProcessed)
posDict = createPOSTags(dblProcessed)
# converting dictionary to dataframe to enable exportation
freqDictDf_v2 = pd.DataFrame(data=freqDict, columns=['Location', 'FrequencyPerWord'])
print(freqDictDf_v2.shape)
print(freqDictDf_v2.columns)

sample = ['hi', 'my name is', 'pycharm is mid', 'just kidding!']
tokenizedSample = tokenize(sample)
tagged = nltk.pos_tag(tokenizedSample[0])
filteredTokenizedSample = filterStopWords(tokenizedSample)

freqDictDf = pd.DataFrame.from_dict(freqDict)
cols = freqDictDf.columns
freqDictDf = freqDictDf.assign(location='')
freqDictDf = freqDictDf.assign(freq='')
freqDictDf = freqDictDf.assign(word='')


freqDictDf = freqDictDf.pivot(columns='location', values=cols)
# table = pd.pivot_table(freqDictDf, values=)

df3 = pd.DataFrame()
df3 = df3.assign(location=freqDict.keys())
df3 = df3.assign(freqPerWord=freqDict.values())



freqDictDf = pd.DataFrame.from_dict(freqDict)
print(freqDictDf.shape)
print(freqDictDf.columns)


freqDictDf.to_csv(r'Y:\PUBLIC\Analytics COE\USAM\Maximo_tables\freqDictDf.csv')