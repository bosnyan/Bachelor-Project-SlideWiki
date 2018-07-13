from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import glob
import os
import pickle
import time

#keep track of the script
start_time = time.time()


NO_TOPICS = 50
MAX_ITER = 2500
NO_TOP_WORDS = 20

def display_topics(model, feature_names, NO_TOP_WORDS):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                    for i in topic.argsort()[:-NO_TOP_WORDS - 1:-1]]))

#add the contents of the dataset in a single list
documents = []
for i in glob.glob("decks/ham_bayes/*.txt"):
    text = open(i, 'r+', encoding="utf-16")
    read_it = text.read()
    process = read_it.replace('\n', '')
    documents.append(process)
    text.close()

#run the TF vectorizer to be used in the LDA topic modelling classifier
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

#run the LDA classifier
lda = LatentDirichletAllocation(n_components=NO_TOPICS, max_iter=MAX_ITER, evaluate_every=1, learning_method='online', learning_offset=10, batch_size=512, random_state=0).fit(tf)

display_topics(lda, tf_feature_names, NO_TOP_WORDS)

#save the variables to be used by the scores builder
file_name = 'TF_vectors_final'
out_test = open(file_name, 'wb')
pickle.dump(tf_vectorizer, out_test)
file_name = 'LDA_model_final'
out_test = open(file_name, 'wb')
pickle.dump(lda, out_test)

#display the duration the the script
elapsed_time = time.time() - start_time
print('duration: ' + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))