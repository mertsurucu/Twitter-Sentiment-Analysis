import numpy as np
import scipy.io as sio
import re
import collections
import operator
import string
from nltk.corpus import stopwords
import math
import nltk
punctuation = list(string.punctuation)
punctuation.remove('!')
stop = stopwords.words('english') + punctuation + ['rt', 'via']
train=np.load('train_tweets.npy')
validation=np.load('validation_tweets.npy')
num_train=int(train.size/2)
num_validation=int(validation.size/2)
unique={}
unique_pos={}
unique_neutral={}
unique_neg={}
bigram_pos={}
bigram_neutral={}
bigram_neg={}
bigram={}
num_pos=0
num_pos_words=0
num_neutral=0
num_neutral_words=0
num_neg=0
num_neg_words=0
num_matches=0
def accuracy(num_matches,num_test):
    return (100*num_matches)/num_test
def list_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [idx for idx,item in enumerate(seq) if item in seen or seen_add(item)]
def duplicates(n): #n="123123123"
    counter=collections.Counter(n) #{'1': 3, '3': 3, '2': 3}
    dups=[i for i in counter if counter[i]!=1] #['1','3','2']
    result={}
    for item in dups:
        result[item]=[i for i,j in enumerate(n) if j==item]
    return result
def removeThis(seq,this):
    for item in range(seq.count(this)):
           seq.remove(this)
    return seq

def listSplit(split_list):
    split_list = split_list.replace('?', ' ?')
    split_list = split_list.replace('!', ' !')
    split_list = split_list.replace(']', '')
    split_list = split_list.replace('~', '')
    split_list = split_list.replace('_', '')


    split_list = split_list.replace('\'', '')
    split_list = split_list.replace('#', ' #')
    split_list = split_list.replace('..', '')
    split_list = split_list.replace(',', '')
    split_list = split_list.replace('|', '')
    split_list = split_list.replace('.', ' ')

    split_list = split_list.replace('-', '')
    split_list = split_list.replace('  ', ' ')
    split_list = re.split(' ', split_list)
    if('' in split_list):
        split_list=removeThis(split_list,'')
    if ('&amp' in split_list):
            split_list = removeThis(split_list, '&amp')


    return split_list

print(string.punctuation)
for i in range(num_train):#seek the every tweet
    split_list=train[i][1].decode('utf-8')
    polarity = int(train[i][0].decode('utf-8'))
    split_list = listSplit(split_list)
    a=0
    for w in split_list:#remove unnecessary things
        split_list[a]=w.lower()

        if(w in stop):
            split_list = removeThis(split_list, w)
        a += 1
    if(polarity==0):#negativ
        num_neg+=1
        num_neg_words+=len(split_list)

        for item in nltk.bigrams(split_list):#bigram
            if (item in bigram_neg):
                bigram_neg[item] += 1
            else:
                bigram_neg[item] = 1

        for j in split_list:
            if (j in unique_neg):

                unique_neg[j] += 1
            else:
                unique_neg[j] = 1
    elif (polarity == 2):#neutral
        num_neutral_words += len(split_list)
        num_neutral += 1
        for item in nltk.bigrams(split_list):#bigram
            if (item in bigram_neutral):
                bigram_neutral[item] += 1
            else:
                bigram_neutral[item] = 1

        for j in split_list:
            if (j in unique_neutral):

                unique_neutral[j] += 1
            else:
                unique_neutral[j] = 1
    elif (polarity == 4):#positive
        num_pos_words += len(split_list)#number of positive words(not unique)
        num_pos += 1#number of positive sentences
        for item in nltk.bigrams(split_list):#bigram
            if (item in bigram_pos):
                bigram_pos[item] += 1
            else:
                bigram_pos[item] = 1
        for j in split_list:
            if (j in unique_pos):

                unique_pos[j] += 1
            else:
                unique_pos[j] = 1
    # print("splited:",split_list)
    #  print("non-split:",train[i][1].decode('utf-8'))
    #   print()
    for item in nltk.bigrams(split_list):  # bigram
        if (item in bigram):
            bigram[item] += 1
        else:
            bigram[item] = 1
    for j in split_list:
        if(j in unique):
            unique[j]+=1
        else:
            unique[j] = 1
num_unique=len(unique)
sorted_x = sorted(unique.items(), key=operator.itemgetter(1))
print(sorted_x)
#print(sorted(unique.values()))
#print()
#print(num_pos,num_neutral,num_neg,num_train)

print(len(bigram))
print(len(unique))

for i in range(num_validation):#seek all the sentences in test data
    split_validation = validation[i][1].decode('utf-8')
    split_validation = listSplit(split_validation)
    a=0
    for w in split_validation:
        split_validation[a]=w.lower()
        if (w in stop):
            split_validation = removeThis(split_validation, w)
        a+=1
    probality_neg = float(num_neg / num_train)
    probality_neg_bigram=float(num_neg / num_train)

    probality_pos = float(num_pos / num_train)
    probality_pos_bigram = float(num_neg / num_train)

    probality_neutral = float(num_neutral / num_train)
    probality_neutral_bigram=float(num_neg / num_train)

    """for item in nltk.bigrams(split_validation):  # bigram
        probality_neg_bigram+=math.log((bigram_neg[item] if item in bigram_neg else 0)+1/(len(bigram)+len(bigram_neg)))
        probality_neutral_bigram += math.log((bigram_neutral[item] if item in bigram_neutral else 0) + 1 / (len(bigram) + len(bigram_neutral)))
        probality_pos_bigram += math.log((bigram_pos[item] if item in bigram_pos else 0) + 1 / (len(bigram) + len(bigram_pos)))
    #calculating only the bigram posibility in here
    probality_max = max(probality_neg_bigram, probality_neutral_bigram, probality_pos_bigram)
    if (probality_max == probality_pos_bigram):
        print("The result is positiv", probality_pos, probality_neutral, probality_neg)
        result = 4
    elif (probality_max == probality_neutral_bigram):
        print("The result is neutral", probality_pos, probality_neutral, probality_neg)
        result = 2
    elif (probality_max == probality_neg_bigram):
        print("The result is negativ", probality_pos, probality_neutral, probality_neg)
        result = 0"""
    for j in split_validation:#seek the sentence word by word
        count=split_validation.count(j)#number of the word in that sentence
        if(count>1):#if it repeats later in the sentence delete others because we already count them
            split_validation=removeThis(split_validation,j)
        probality_neg+=math.log((1+count+(unique_neg[j] if j in unique_neg else 0))/(num_unique+num_neg_words))
        probality_neutral += math.log((1+count + (unique_neutral[j] if j in unique_neutral else 0))/ (num_unique + num_neutral_words))
        probality_pos +=math.log((1+count + (unique_pos[j] if j in unique_pos else 0)) / (num_unique + num_pos_words))
    #i give weight to bigram
    """probality_pos+=probality_pos_bigram/800
    probality_neutral+=probality_neutral_bigram/800
    probality_neg+=probality_neg_bigram/800"""

    probality_max=max(probality_pos,probality_neutral,probality_neg)
    if(probality_max==probality_pos):
        print("The result is positiv",probality_pos,probality_neutral,probality_neg)
        result=4
    elif(probality_max==probality_neutral):
        print("The result is neutral",probality_pos,probality_neutral,probality_neg )
        result=2
    elif (probality_max == probality_neg):
        print("The result is negativ",probality_pos,probality_neutral,probality_neg )
        result=0
    print(validation[i][1].decode('utf-8'),validation[i][0].decode('utf-8'))
    print(split_validation)
    if(result==int(validation[i][0].decode('utf-8'))):
        num_matches+=1


print("ACCURACY %",accuracy(num_matches,num_validation))
    #dict = dict.fromkeys(seq)

    #print(split_validation)