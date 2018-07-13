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

#load the dictionaries
deck_dir = "decks/english_only/*.txt"

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
    file_name = path[19:].replace('.txt', '')  # strip the path and .txt from the filename
    deck_scores[file_name] = {} #create an empty dict key based on deck ID i
    a_copy = deck_scores[file_name]

    #load the topic scores for deck i
    scores = lda.transform(tf_vectorizer.transform(documents))[i]
    print(file_name)
    count = 0
    for j in range(0, len(scores)): #for deck i, loop through the topic and retrieve the scores
        current_topic = "topic_" + str(j)
        total_copy = topic_total[current_topic] #create a dict key named after topic j
        if scores[j] > REQ: #if the topic score j is > REQ, proceed
            count += 1
            a_copy[current_topic] = scores[j] #for the dict key deck ID i, save the score of topic j as a dict key topic j
            total_copy[file_name] = scores[j] #for the dict key topic j, save the deck ID i as a dict key with its score for topic j
    if count >= 1:
        # add deck ID i to the list of processable decks if it has a match with 1 or more topics
        deck_list.append(file_name)
        print(deck_scores[file_name])

#save the variables for the recommendation system
file_name = 'deck_list'
out_test = open(file_name, 'wb')
pickle.dump(deck_list, out_test)
out_test.close()
file_name = 'topic_total'
out_test = open(file_name, 'wb')
pickle.dump(topic_total, out_test)
out_test.close()
file_name = 'deck_scores'
out_test = open(file_name, 'wb')
pickle.dump(deck_scores, out_test)
out_test.close()

#display the duration the the script
elapsed_time = time.time() - start_time
print('duration: ' + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))