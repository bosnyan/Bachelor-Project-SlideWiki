from __future__ import print_function, division
import os
from collections import Counter
from nltk import word_tokenize, WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier, classify
import pickle
import time

#keep track of the script
start_time = time.time()

stoplist = stopwords.words('english')

#import the trained classifier
in_test = open('NB_classifier', 'rb')
classifier = pickle.load(in_test)
in_test.close()
print('test')

def init_lists(folder):
    a_list = []
    file_list = os.listdir(folder)
    for a_file in file_list:
        f = open(folder + a_file, 'r', encoding="utf-16")
        a_list.append(f.read())
    f.close()
    return a_list

def preprocess(sentence):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(sentence)]

def get_features(text, setting):
    if setting=='bow':
        return {word: count for word, count in Counter(preprocess(text)).items() if not word in stoplist}
    else:
        return {word: True for word in preprocess(text) if not word in stoplist}

#import the dataset and create a feautreset of it
full_dir = "decks/english_only/"
full = init_lists(full_dir)
full_features = [get_features(test, 'bow') for test in full]
full_list = os.listdir(full_dir)
print('testt')

#loop through the featureset
for i in range(0, len(full_features)):
    deck_i = classifier.classify(full_features[i])
    if deck_i == 'spam': #if the deck is classified as spam..
        print(full_list[i] + " is spam!")
        #save the deck in the spam folder
        text = open(full_dir+full_list[i], 'r+', encoding="utf-16")
        result = open("decks/spam_bayes/" + full_list[i], 'w+', encoding="utf-16")
        process = text.readlines()
        for sent in process:
            words = word_tokenize(sent)
            for r in words:
                nieuw = lemmatizer.lemmatize(r.lower())
                result.write(nieuw + ' ')
            result.write('\n')
        text.close()
        result.close()
    if deck_i == 'ham': #if the deck is classified as ham..
        print(full_list[i] + " is ham!")
        #save the deck in the ham folder
        text = open(full_dir+full_list[i], 'r+', encoding="utf-16")
        result = open("decks/ham_bayes/" + full_list[i], 'w+', encoding="utf-16")
        process = text.readlines()
        for sent in process:
            words = word_tokenize(sent)
            for r in words:
                nieuw = lemmatizer.lemmatize(r.lower())
                result.write(nieuw + ' ')
            result.write('\n')
        text.close()
        result.close()

#display the duration the the script
elapsed_time = time.time() - start_time
print('duration: ' + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))