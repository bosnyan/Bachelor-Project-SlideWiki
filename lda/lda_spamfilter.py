from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import glob
import pickle
import time

#keep track of the script
start_time = time.time()

#initialize the constants
NO_TOPICS = 50
REQ = 0.05
SPAM_REQ = 0.7
SPAM_TOPICS = [0, 2, 4, 5, 8, 9, 14, 18, 23, 29, 31, 33, 34, 39, 41, 43, 46, 47, 48] #list of indices that correspond to spam topics 50 topics 2500 iter

#load the dictionaries
deck_dir = "decks/english_only/*.txt"
spam_dir = "decks/spam_lda/*.txt"
ham_dir = "decks/ham_lda/*.txt"

#load the dictionaries
in_test = open('TF_vectors', 'rb')
tf_vectorizer = pickle.load(in_test)
in_test.close()
in_test = open('LDA_model', 'rb')
lda = pickle.load(in_test)
in_test.close()

#create the list of documents
documents = []
for i in glob.glob(deck_dir):
    text = open(i, 'r+', encoding="utf-16")
    read_it = text.read()
    process = read_it.replace('\n', '')
    documents.append(process)
    text.close()
# create the dict objects
deck_list = []
deck_scores = {}
topic_total = {}
for i in range(0, NO_TOPICS):
    dict_item = 'topic_'+str(i)
    topic_total[dict_item] = {}

#loop through all decks in the directory
for i in range(0, len(glob.glob(deck_dir))):
    spam_score = 0.0 #start with a spam score of 0.0 for deck i
    path = glob.glob(deck_dir)[i]
    file_name = path[19:].replace('.txt', '') #strip the path and .txt from the filename
    deck_scores[file_name] = {} #create an empty dict key based on deck ID i
    a_copy = deck_scores[file_name]

    #load the topic scores for deck i
    scores = lda.transform(tf_vectorizer.transform(documents))[i]
    print(file_name)
    for spam in SPAM_TOPICS: #loop through the spam topic first
        if scores[spam] > REQ:
            # if the topic score is higher than REQ, add the score to the spam score
            spam_score += scores[spam]
    if spam_score > SPAM_REQ:
        #if the sum spam score is > SPAM_REQ, do not process it through the scores builder
        text = open(path, 'r+', encoding="utf-16")
        read_it = text.read()
        result = open(spam_dir.replace('*.txt', '') + file_name + '.txt', 'w+', encoding="utf-16")
        result.write(read_it)
        text.close()
        result.close()
    else: #if the sum spam score is < SPAM_REQ, proceed
        deck_list.append(file_name)
        text = open(path, 'r+', encoding="utf-16")
        read_it = text.read()
        result = open(ham_dir.replace('*.txt', '') + file_name + '.txt', 'w+', encoding="utf-16")
        result.write(read_it)
        text.close()
        result.close()
        print(deck_scores[file_name])

#display the duration the the script
elapsed_time = time.time() - start_time
print('duration: ' + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))