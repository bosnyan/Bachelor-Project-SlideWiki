import pickle
from numpy import array

#load the necessary variables
in_test = open('deck_list', 'rb')
deck_list = pickle.load(in_test)
in_test.close()
in_test = open('deck_scores', 'rb')
deck_scores = pickle.load(in_test)
in_test.close()
in_test = open('topic_total', 'rb')
topic_total = pickle.load(in_test)
in_test.close()

file_entry = input("Enter deck ID: ")

check = False #keep looping as long as there is no valid file entry
while check is False:
    if file_entry in deck_list:
        check = True
        deck_score = deck_scores.get(file_entry)
        #create some empty dict objects
        process = {}
        process_part2 = {}
        similar_decks = {}

        #retrieve the topics of the deck and loop through them
        deck_topics = list(deck_score.keys())
        topic_nr = 0
        for topic_i in deck_topics:
            deck_topic_score = list(deck_score.values())[topic_nr] #get the topic score of the current topic
            inv_weight = 1 - deck_topic_score #this is used as a weight to calculate a weighted score
            topic_nr += 1
            current_scores = topic_total.get(topic_i) #get the decks with their scores that are related to the current topic
            scores_array = array(list(current_scores.values())) #retrieve only the scores and turn the list into an array
            decks_4_topic = list(current_scores.keys()) #retrieve only the deck IDs from current_scores
            #calculate the difference between the scores in scores_array and the score of the input file
            for i in range(0, len(scores_array)):
                if scores_array[i] > deck_topic_score:
                    scores_array[i] = scores_array[i] - deck_topic_score
                else:
                    scores_array[i] = deck_topic_score - scores_array[i]
            scores_array = scores_array * inv_weight #calculte the weighed scores
            smallest = list(scores_array.argsort()[10:200]) #retrieve the indices of the 100 smallest values

            #loop through the smallest list
            for i in list(smallest):
                similar_deck = decks_4_topic[i] #get the deck ID that corresponds to index i
                similar_deck_score = scores_array[i] #get the score of the deck ID that corresponds to index i
                if similar_deck in process:
                    similar_deck_dict = process[similar_deck]
                #if the keys already exist, add the respective variables to the respective keys
                    similar_deck_dict['count'] += 1
                    similar_deck_dict['sum'] += similar_deck_score
                    similar_deck_dict['sum'] = similar_deck_dict['sum'] / similar_deck_dict['count']
                else: #otherwise create the keys
                    process[similar_deck] = {}  # create an empty dict key named after the deck ID from similar_deck
                    similar_deck_dict = process[similar_deck]
                    similar_deck_dict['sum'] = similar_deck_score
                    similar_deck_dict['count'] = 1
                #calculate the average confidence interval
                similar_deck_dict['average'] = (similar_deck_dict['sum'] / (similar_deck_dict['count']**similar_deck_dict['count']))*(1+len(deck_topics)-similar_deck_dict['count'])
                #only save the average confidence interval as value and the current deck as key
                process_part2[similar_deck] = similar_deck_dict['average']

        final_scores = array(list(process_part2.values())) #retrieve only the scores and turn the list into an array
        decks_4_deck = list(process_part2.keys()) #get the decks with their scores that are related to the input deck
        best_matches = list(final_scores.argsort()[5:200]) #retrieve the indices of the 100 smallest values
        print('Deck IDs recommended for deck ID ' + file_entry + ':')
        deck_score['similar decks'] = {} #create an empty key that will contain the 10 most similar decks to the input deck
        similar_decks_2 = deck_score['similar decks']
        no_matches = 0
        #loop through the best_matches array
        final_score = -1
        listy = []
        for i in list(best_matches):
            print(no_matches)
            print(final_scores[i])
            if no_matches >= 10:
                pass #stop adding any more recommendations after 10 recommendations
            else:
                matching_deck = decks_4_deck[i]
                if final_scores[i] == 0.0: #skip over duplicate decks
                    pass
                elif final_scores[i] == final_score:
                        pass
                else:
                    final_score = final_scores[i]
                    listy.append(matching_deck)
                    no_matches += 1
                    #get the deck and confidence interval that correspond to index i
                    ci_score = final_scores[i]
                    similar_decks[matching_deck] = ci_score
                    similar_decks_2[matching_deck] = ci_score
                    print('Deck ' + matching_deck + ' with confidence interval: ' + str(ci_score))
        print(deck_score)
        test = ', '.join(listy)
        print(test)
    else: #if no valid file name is provided
        file_entry = input("Deck not found. Try a different deck ID: ")
