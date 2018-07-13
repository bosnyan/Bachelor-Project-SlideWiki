import requests
from lxml import html
import regex

headers = {
    'Accept': 'application/json',
}

params = (
    ('countOnly', 'false'),
)
#loop through a range of numbers to try it as a deck ID
for deck_id in range(0,999999):
    print(deck_id)
    response = requests.get('https://deckservice.slidewiki.org/deck/'+str(deck_id)+'/slides', headers=headers, params=params)
    #try the deck ID with the number deck_id, if it returns a status code 200, scrape its contents
    if response.status_code == 200:
        print("yes!")
        print(response)

        #retrieve the plain text of the response, filtering out any HTML tags
        tree = html.document_fromstring(response.text)
        full_text = tree.text_content()
        pattern = '"title":"\s?(.+?)\s?"' #search for text within this JSON response
        titles = regex.findall(pattern, full_text)
        pattern_2 = '"content":"\s?(.+?)\s?"' #search for text within this JSON response
        contents = regex.findall(pattern_2,full_text)

        # save as UTF-16, since many decks contain characters that cannot be processed with UTF-8
        text = open("decks/initial/"+str(deck_id)+".txt", 'w+', encoding="utf-16")
        #write the first index of the title list, as that is the title of the deck itself
        text.write(titles[0]+'\n')
        del titles[0] #remove the deck title, to keep the slide titles only

        #loop through the number of slides
        for i in range(0,len(contents)):
            text.write(titles[i]+'\n') #print the title of the slide
            text.write(contents[i] + '\n') #print the contents of the slide

        text.close()