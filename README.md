# Bachelor-Project-SlideWiki
This is the implementation of the recommendation system used, along with the different models that were applied for spam classification on the dataset which is based of SlideWiki.org. Everything that is needed to reproduce the results in the thesis is present. 

There are some files that are zipped in .7z files. These are optional, but it's strongly recommended to download and to unpack the files if you wish to see a quick demonstration of the different scripts, such as the recommendation system.

This document will further explain the inidividual files present in this project.


# Scraping and preprocessing: scrapings.py and processing.py 
This is the first step to the implementation: gathering the data and preprocessing it. The decks.7z file in the root is the result of scraping SlideWiki and preprocessing of the data. Run scrapings.py first and then proceed to run processing.py.


# Score building and recommendation system: lda_modelling.py, scores_builder.py and recommend_system.py 
The implementations of the score builder and recommendaiton system can be found in any of the control, bayes, lda and ensemble folders. The difference in the models lies in the dataset is has been trained on. The control model has no spam classification performd on its dataset, the Bayes model used Naïve Bayes classification for spam filtering, the LDA model used LDA for spam filtering and the ensemble model combined Naïve Bayes classification and LDA for spam filtering. In any case, all four models have already been trained and score building has already been run. If you wish to immediately retrieve recommendations for a deck ID, just extract the contents in the respective pickles.7z files of the folders. 
Every folder also contains a deck.7z file, if you wish to run the score building yourself. Do make sure to first train the LDA model by running lda_modelling with the correct folder containing the training set, since score_builder.py is the LDA model that performs classification. 


# Naïve Bayes spam classification: naive_bayes_trainer.py and naive_bayes_spamfilter.py
The implementations of the Naïve Bayes classifier can be found in the bayes and ensemble folders. Both models have already been trained and they have already performed classification on the English-only dataset of SlideWiki's decks. The settings of the trained NB models can be found in the pickles.7z files, which are present in both the bayes and ensemble folders. Keep in mind however that the pickles.7z in the ensemble folder also contains the files for the trained LDA model. Furthermore, if you wish to train the Naïve Bayes classifier, you're required to unpack decks.7z in the bayes folder. Run naive_bayes_trainer.py first to train the classifier and then run the classifier naive_bayes_spamfilter.py. The output of the classifier is also present in decks.7z.


# LDA spam filtering: lda_modelling.py and lda_spamfilter.py
It should be noted that the classifier in the score builder and the alternative spam filtering method using LDA train exactly the same and use the same file to train their LDA models. Do make sure to train the LDA model again after performing LDA spam filtering to make sure that the score builder is trained on the filtered subset. Furthermore, the LDA spamfilter can be found in both the LDA and the ensemble folder. All the files associated with the trained LDA models can be found in the pickles.7z files in the respective folders. If you wish to perform classification, make sure to unpack the contents of deck.7z in the folder of a LDA model to make sure that it has a dataset to train on/to classify. After training the LDA model with lda_modelling.py, spam filtering can be performed with lda_spamfilter.py. The output of the classifier is also present in decks.7z.


# Ensemble: LDA spam filtering + Naïve Bayes spam classification
Simply follow the steps documented in the section about the Naïve Bayes spam classifier and then continue with the steps noted in the section about LDA spam filtering. The complete set of the two classifiers can be found in the ensemble folder. The files of the trained models can be found in pickles.7z and the output can be found in decks.7z.


# Scraping and preprocessing: the how and why
The recommendation system or any classifier in fact needs a dataset to train on. In this case the dataset consists of SlideWiki’s decks in plain text. The entire collection of SlideWiki’s decks was scraped on the 28th of May 2018 and 27012 decks were retrieved. The getDeckId function on SlideWiki’s own deckservice (https://deckservice.slidewiki.org/documentation#!/deck/getDeckId) was repurposed in Python to scrape all the decks that were available on SlideWiki at that time. Since SlideWiki uses simple integer value for their deck IDs, a for loop of 0 to 999999 was used to check for every value whether it was an existing deck ID. A response code of 200 meant that the deck with the given deck ID i exists and it could thus be scraped. As the deck is formatted in HTML, the first step was to only get the text from the response. LXML proved to be very helpful with that. The last step was retrieve the plain text content of the deck by searching for text that fell within a defined regex pattern. 

While plain text is a good start regarding data to process, the dataset could still use some pre-processing. The initial dataset consists of decks written in various languages (i.e. Hindi, Russian, Greek et cetera) and there is also a rather large proportion of very short decks. These shorter decks were first of all mostly decks that were made for testing purposes and furthermore, other non-test decks that are of such small size will not be informative anyway. The first course of action on the initial dataset was filter-ing out any decks where its plain text content was smaller than 1kB. This resulted in a dataset of 20460 decks 
After removing the small decks, the contents still require further processing. Non-Latin symbols, punctuation marks and stopwords were removed. Furthermore, all content was turned into lowercase text and lemmatization from NLTK’s lemmatiza-tion library was applied to the decks as the final step. Lemmatization is particularly useful for this use case, as it tries to unify all inflicted forms of a term into a single word. This prevents information loss and it also prevents the likelihood of the inflict-ed forms of a term (car, cars, …) to be split over multiple classes in the model space of our classifiers. 

Trying to keep the scope of this project somewhat narrow, non-English decks were removed as well. Non-English decks were filtered out using a Python library, called langdetect. This library is a port of  a Google library and it has the function of esti-mating the possible language(s) of a given input string. Filtering non-English decks with the help of langdetect resulted in a total of 16723 likely English slides. One should however keep in mind of that of course that the filtering process was auto-mated process where the program merely estimates the likelihood that a deck i is either English or not. Given that this is not a perfect world and despite all optimiza-tions made, the "English-only" classifier is not perfect either. This does mean that errors did occur where non-English decks were overlooked by the classifier and actual English decks were unjustly filtered out as being considered non-English by the classi-fier. Regarding the classifier’s efficacy, precision and recall was measured. 200 ran-dom samples were retrieved, 100 from the resulting English set of decks and 100 from the resulting non-English set of decks. The classifier has a recall of 0.81 and precision of 0.92. The fact that the dataset is imperfect (i.e. not completely “English-only”) should be kept in mind when commenting on the efficacy of both the spam filters and the recommendation systems.

After pre-processing the data is in principle ready to be processed through the LDA topic modelling classifier. However from the set of 16723 decks, there is still a large prevalence of spam present in the dataset. Three different models have been consid-ered for this project and they will later on be compared in terms of performance in one of the experiments. Regarding the final sets, there are four of them. 
- Naïve Bayes spam filtering resulted in 4476 decks, 
- LDA spam filtering resulted in 3948 decks
- Spam filtering by the ensemble resulted in 3781 decks.


# Score building: the how and why
As mentioned in the previous section, the recommendation system is split in two parts. This part will discuss the preparations which are performed by the score builder. The LDA model is from the scikit-learn package for Python. The Medium article from Aneesha Bakharia on Topic Modeling with Scikit Learn has been used as a starting point of which the training implementation is based on. (https://medium.com/mlreview/topic-modeling-with-scikit-learn-e80d33668730) 
The article shows how a LDA model can be trained when providing it a dataset and how the LDA model returns topics with labels for each topic after it has been trained. Everything in the implementation beyond training the LDA model has been built from scratch.
The first step is thus to train the LDA classifier by providing a training set. In the case of this project, the training set is the target as well. In other words, the target dataset trains the classifier so that the classifier can classify the documents in the target set. Before training running the training there are some parameters that have to be considered relative to the target set. In the case of this project the following pa-rameters have been set:
- Number of topics has been set to 50
- The model will run 2500 iterations
- Learning offset has been set to 10 
- Batch size has been set to 1024
These parameters were optimized for the 17K decks dataset where no spam filter-ing has been applied. This means that the LDA spam filter and the baseline recom-mendation system (no spam filtering applied) run optimally. The LDA spam filter in the ensemble and the recommendation systems where spam filtering have been ap-plied do not run optimally under these parameters, since they have smaller target sets that differ from the 17K dataset (due to spam filtering). Parameters have been kept constant across all models for the sake of enforcing consistency during experimenta-tion. After training, the LDA model is able to classify documents in the target set by assigning it scores for each topic. An example of how a topic can look like is the fol-lowing: Topic 3: data clustering cluster object set method point feature attribute analysis value distance similarity using algorithm measure number matrix hierar-chical graph.
 
It is rather clear that topic 3 is trained to have high associations with documents that are about clustering, since it contains labels that are typical to clustering.  It would make sense for a documents that has absolutely nothing to do with clustering to have an association of 0 with topic 3. However, the LDA classifier from scikit-learn will always return a score higher than 0 for every single topic given a document. Some of these scores can get as low as 8.43881857e-04, which translates to a match of roughly 0.09%. Such matches are clearly irrelevant and thus a threshold has been set that a topic has to meet in order for the topic to be considered to have a meaning-ful association with the target document. The threshold has to be set relative to the number of topics, since a higher number of topics allows for the likelihood of a doc-ument’s association to be split over a high number of topics. In this case where the number of topics has been set to 50, the threshold has been set to 0.05. 
Should for a given document the association with a topic be higher than the threshold then the topic is saved in a set of topics that are associated with the docu-ment and the document is saved in a set of documents that are associated with the topic. After classification has been finished (all the documents in the set are pro-cessed), there are two collections of sets that will be used for cross searching related documents in the recommendation model. There are n-number of sets of topics that have associations with a document i in n and k-number of sets of documents that have associations with a topic j in k. When classifying a set of SlideWiki’s decks the output for a deck ID 101888 and topic 6 look as follows. '101888':{'topic_6': 0.40411581834506022, 'topic_10': 0.10530399922914256, 'topic_11': 0.42686432288928561}. Here can be seen that the set of deck ID 101888 contains three topics. In other words, the deck is associated with three different topics. 'top-ic_6': {'101661': 0.10342629284133516, '101685': 0.32628935596278791, '101864': 0.39136141755081905, '101888': 0.40411581834506022, …}. The set of topic 6 contains among other deck 101888, but also several other decks that have an association with topic 6. Aside from the deck ID, every deck also contains the score that expresses its association with topic 6.  
Thus in the case of SlideWiki’s decks, there are n-number of sets of topics that have associations with a deck ID i in n and k-number of sets of deck IDs that have associations with a topic j in k.  


# Recommendation system: the how and why
After the score builder has finished, the recommendation system can provide recommendations based on similarities in topic associations between documents. Due to the fact that the heavy lifting has been done beforehand with the score builder, the relatively easy computations performed by the recommendation system allow it to return recommendations in an instant. 
Given a document ID i, the recommendation system looks at which topics are associated with the document and what the respective scores are for each topic. The system will then loop through each topic associated with the document. For every associated topic it will do the following: 
- Take the association score of the topic with document ID i and use it as a target value
- In the set of decks associated with the current topic:
  - Perform a confidence interval 
	- Sort to lowest scores first
	- Discard first 10 results (to avoid duplicates)
 - Save this order of documents as potential candidates to be recommended to the target document ID i
	- Check whether a document has been detected before in the loop (thus association with more than one topic)
	- If yes, sum the old total score of the document with current topic score of the document and divide it with the current count (e.g. 2)
  
After looping through every topic associated with document i, there is a list of potential candidates that could be recommended to document i as being related. These candidates have an intermediate confidence interval score of which the final score still has to be computed. The calculation for the final score heavily favors matching over the most number topics that are associated with the target document i. For example, imagine if a document i has associations with 5 different topics and a potentially recommended document has associations with 2 just of the same topics, while another document has associations with all 5 of the same topics. The latter will much more likely be selected as a recommendation for document i due to its match over all 5 topics. This approach has been chosen, since selecting on the lowest confidence interval alone does not yield the best recommendation. Assuming matching the number of topics to be of equal importance as the confidence interval can lead to situations where an irrelevant document is recommended over other relevant documents due to it having an extremely low confidence interval on a single topic. 
	In order to negate these irrelevant recommendations, the emphasis has thus been set on heavily favoring documents that match over the most number of topics to the target document. The final score is computed as follows:

A = # of associated topics of a target deck
B = # of associated topics shared

final score = (intermediate score /B^B)(A - B + 1)

The intermediate confidence interval is thus divided by the number of topics that a potentially recommendation j shares with document i to the power of this same number. Should this number be equal to 1, then the intermediate score will be divided by 1. The final score is then finally calculated by multiplying the aforementioned calculation by the number of topics document i is associated with, minus number of topics that a potentially recommendation j shares with document i, plus 1. The nice thing about this calculation is that it does not harm target documents that are associated with a low number of topics (such as 1). The final calculation will then simply be the intermediate score divided by 1, times 1. This is equal to the intermediate score itself. 
After the final confidence intervals have been determined, the list is once again sorted from lowest to highest. Due to a large abundance of duplicates in SlideWiki, the first 5 results are discarded as an attempt to avoid them. Forking is among other a key feature in SlideWiki that allows users to create duplicates for themselves. Thus there is a large presence of duplicates that are either (almost) identical to the target document or (almost) identical to one of the recommendations that were already determined. Simply deleting duplicates from the dataset or omitting them from the recommendation system is not a suitable solution in the use case of SlideWiki where forking is a key feature. Given that document retrieval using LDA is not Boolean retrieval (due to determining matches through scores between 0 and 1, instead of a Boolean value), it means that a target document can always have recommendations. The extent of how related a recommended document then is to a target document i is  dependent on the score/confidence interval. It is thus assumed that discarding the first 5 lowest results does not hurt relevance feedback, since there should be plenty of documents that can be related to the target document i anyway. 
After discarding the 5 lowest results, the system loops through the final list with the goal to find 10 document recommendations for document i. If the confidence interval of a document j is not equal to the confidence interval of the previously recommended document, save document j as a recommendation for document i. In other words, save document j as a recommended document k, only if document j is not a duplicate of recommended document k-1 (confidence intervals are different/not equal). The recommendation system will keep searching for documents to recommend until it has found 10 recommendations for document i or until it has exhausted its options for potential recommendations for document i. 
Going back to deck 101888, these are the recommendations returned for this particular deck: {'106477': 0.0013723926992843102, '99262': 0.0019579153229656266, '108790': 0.0019626365690208654, '97809': 0.0020098828243271488, '358': 0.0038274020059378393, '3201': 0.0048214531486790845, '2754': 0.0048214531489461981, '99587': 0.0049867929403360524}. According to the recommendation system; these should all be decks that are similar in content to 101888. These are all deck IDs that correspond to actual decks on SlideWiki. The link to for example deck 3201 can be found here: https://slidewiki.org/deck/3201.   


# Naïve Bayes spam classification: the how and why
The initial idea was to just tackle the spam head-on and build a Naïve Bayes spam filter. Naïve Bayes classification was the first solution that came to mind when faced with the large presence of spam in the SlideWiki dataset, since the textbook example of Naïve Bayes being applied is it being trained and implemented as spam filter. The implementation of the Naïve Bayes spam filter is largely based on an example that can be found on Cambridge Spark. (https://cambridgespark.com/content/tutorials/implementing-your-own-spam-filter/index.html) The article by Ekaterina Kochmar shows how a spam filter based on Naïve Bayes classification can be built using Python’s NLTK package. 
Aside from its associations as being a spam filter, Naïve Bayes has some other characteristics that make it interesting in this particular problem.	A Naïve Bayes spam classifier is relatively easy to train. Give it a set of labelled examples of both classes “ham” and “spam.” Train the model on this labelled training set such that it learns what documents should be considered spam and which documents should not be considered as spam based on the examples provided in the training set. In this case, the resulting labelled set consisted of 1151 “ham” labelled examples and 3808 “spam” labelled examples. 85% of this set is used for training, while the remaining 15% was set aside as a test set to evaluate the Naïve Bayes spam filter. This resulted in the following sets:
-	978 ham training
-	173 ham test
-	3236 spam training
-	571 spam test

Another upside to using Naïve Bayes classification is the relatively high speed when performing classification. The spam filter is able to process the 17K set of  Eng-lish decks in 11 minutes and 5 seconds. 
A downside with Naïve Bayes however is the performance of the spam filter itself. The classifier has an accuracy of 85% on the test set. This is by no means bad, but it is far from perfect. Furthermore, the evaluation on the test set only returned the accu-racy. Its precision and recall on the test set is unknown. A high recall is of course de-sirable, since it would mean that the classifier is sensitive enough to filter out a large proportion of spam, however precision is arguably much more important. When evaluation a spam classifier’s efficacy in terms of costs of the resulting errors, it be-comes clear why precision is much more important than recall. In the case of a false negative, the worst what can happen is that a spam document is given as a recom-mendation by the recommendation system. This would be mildly infuriating at most, while a false positive results in losing a non-spam document, as it was incorrectly classified as spam. With a non-spam SlideWiki deck it would mean that for example someone’s lecture on Artificial Intelligence got filtered away. That is valuable infor-mation that is lost due to an incorrect classification. 
 Furthermore, Naïve-Bayes uses supervised learning. The spam filter is constructed by providing labelled examples that are spam and not spam. Unless the sample sets are constantly updated as new decks are uploaded, the spam filter risks to become worse as the website grows in more and more distinct content. Especially when con-sidering that SlideWiki aspires to be a platform to create and share decks about any subject, worse performance of this spam filter over time seems inevitable.


# LDA spam filtering: the how and why
An alternative to Naïve-Bayes spam filtering could be spam filtering using the same LDA classifier that was used for the score builder. However, instead of identifying with which topics a document i is associated with, the classifier will determine whether a document i is spam by evaluating its associations with a set of preidentified “spam topics.” These spam topics are topics that contain labels that are typical vocabulary present in spam documents. An example of a spam topic is the following: Topic 2: gmail password recovery forgot warehouse passwordcall way help instant reliable passworddial effective entire operational helpusa wayusa helpuse helpget solu-tionusa analytical. Evaluating the labels present in topic 2, it becomes rather clear that this topic is likely associated with spam documents. 

There are several reasons to use LDA spam classification, the first one being the ease of implementation in the case of this project. The recommendation system which is based on LDA was already developed for this project. Adapting this imple-mentation to work as a spam filter requires minor tweaks. As seen in section 3.1, the LDA classifier returns a document’s associations with topics expressed as a decimal value. Given a set of spam topics, the spam filter will look into what a document i’s associations are with the set of spam topics and take the sum of these values. If this sum association exceeds a certain threshold (in this case it has been set to 0.7), the document will be classified as spam. If this sum value is below the threshold, the document will not be classified as spam and it will remain in the final dataset. 
The set of spam topics are determined beforehand and their indices are contained in a list (e.g. topic 0 sits at index 0 etc.) through which the spam filter will loop to evaluate a document’s association with a spam topic i in the set of spam topics. The final implementation of LDA spam classification contained 19 spam topics after training on the 17K dataset. 
Manually determining which topics should be seen as spam topics has its merits, but there are also some issues. One of the issues being that the LDA spam filter will require constant human intervention to again determine what the spam topics are every time the LDA model has updated. The upside to this approach and LDA in general is that there is much more possibility for finetuning the model to either preci-sion or recall. If recall needs to be maximized, just set the threshold lower and be rather liberate with the selection of spam topics. Precision will of course suffer under this, but that can again be prioritized by raising the threshold and being more con-servative with the selection of spam topics. Further optimization can be done by find-ing the optimal number of topics, iterations, learning offset, batch size etc. relative to the target dataset. 
The biggest downside with using LDA for spam classification however is its relatively slow performance. It took the LDA classifier roughly more than 16 hours to process the 17K unfiltered set of English decks. This is considerably slower to Naïve Bayes’ performance, which was able to process the same dataset in just beyond 11 minutes. 


# Ensemble: the how and why
When considering the strengths and weaknesses of both models, an ensemble consist-ing of LDA on top of Naïve Bayes classification seems to be a solution where both models will play to each other’s strengths. LDA is a slow classification technique, especially when compared to Naïve Bayes classification which is considerably faster. Naïve Bayes does not have many options regarding tuning, while LDA is much more flexible and it can be prioritized towards either precision or recall. Furthermore, a Naïve Bayes model runs the risk of becoming outdated in an ever-updating and growing database. A LDA model can just train on the new database again, such that it is updated on the newest contents of the database. 
Regarding the use cases of the respective spam classifiers, Naïve Bayes classifica-tion can be best seen as a classifier that is ran once to perform a rough, but quick cleanup of a large dataset. LDA on the other hand is best suitable for handling small-er datasets due to its slower performance, but high flexibility regarding tuning. Such small datasets are for example intermediate datasets that are returned by the Naïve Bayes classifier where some spam still may be present, or even batches of new up-loads that have to be evaluated on being spam or not. In the long run, the LDA mod-el seems as a more sustainable solution however, since it has the possibility to be constantly updated and tweaked such that it remains able to effectively classify spam. Furthermore, the LDA classifier is perhaps rather slow, but its implementation will likely just handle small batches of newly uploaded decks at a time. This makes the slow performance rather negligible. 
All in all, the Naïve Bayes classifier does the rough filtering and returns an inter-mediate dataset where most of the spam has been filtered out. The LDA classifier trains on the intermediate dataset and tries to pick out the remaining spam.
