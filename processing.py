from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import glob
import os
from langdetect import detect_langs
import unicodedata as ud

latin_letters= {}
def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))
def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha()) # isalpha suggested by John Machin

stop_words = set(stopwords.words('english'))

counts = 0

#loop through all documents in the directory
for i in glob.glob("decks/initial/*.txt"):
    statinfo = os.stat(i)
    #only further process and save the deck if it is larger than 1kB
    if statinfo.st_size >= 1024:
        counts += 1
        text = open(i, 'r+', encoding="utf-16")
        file_name = i[14:]
        result = open("decks/processed/" + file_name, 'w+', encoding="utf-16")
        process = text.readlines()
        for sent in process:
            #do some processing on the sentences
            sent_2 = sent.replace("\n", '')
            words = word_tokenize(sent_2)
            for r in words:
                if len(r) > 1: #filter out any single character strings
                    if r.isalpha() == True: #filter out any non-alphanumeric characters
                        if not r in stop_words: #filter out stopwords
                            lemma = lemmatizer.lemmatize(r.lower()) #lemmatize the remaining text
                            result.write(lemma + ' ')

            result.write('\n')

        text.close()
        result.close()
    print(counts)

counts = 0

#loop through the processed decks in the dictionary
for i in glob.glob("decks/processed/*.txt"):
    counts += 1
    print(counts)
    text = open(i, 'r+', encoding="utf-16")
    file_name = i[16:]
    print(file_name)
    result = open("decks/english_only/" + file_name, 'w+', encoding="utf-16")
    process = text.readlines()
    slides = 0
    score = 0.0
    for sent in process:
        sent = sent.strip()
        slides += 1

        if sent != '\n' and len(sent.split()) > 1:

            #copy the file in a new dictionary, namely english_only
            result.write(sent)
            result.write('\n')
            langs = detect_langs(sent)
            print(langs, [sent])
            main_lang = langs[0]
            print(len(sent.split()))
            #if the string is identified as mainly english, add the main_lang.prob to the score
            if main_lang.lang == 'en' and only_roman_chars(sent) is True:
                print(str(score)+" + "+str(main_lang.prob))
                score += main_lang.prob
                print(score)
            # if the string is identified as mainly non-english, subtract the main_lang.prob from the score
            elif main_lang.lang != 'en':
                score -= main_lang.prob
                print(score)

    text.close()
    result.close()
    print(score)
    print(slides)
    final_score = 0.0
    if score != 0:
        final_score = score / (slides/2)
    print(final_score)
    if final_score < 0.2: #if the score is below 0.2, remove the file from the dictionary
        print('removing ' + file_name)
        os.remove("decks/english_only/" + file_name)
    else:
        print('keeping ' + file_name)
print(counts)