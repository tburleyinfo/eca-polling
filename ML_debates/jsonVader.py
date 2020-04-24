import csv 
import json
import pprint 
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer

# import SentimentIntensityAnalyzer class 
# from vaderSentiment.vaderSentiment module. 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# function to print sentiments 
# of the sentence. 
def sentiment_scores(sentence):

        # Create a SentimentIntensityAnalyzer object. 
        sid_obj = SentimentIntensityAnalyzer()

        # polarity_scores method of SentimentIntensityAnalyzer 
        # oject gives a sentiment dictionary. 
        # which contains pos, neg, neu, and compound scores. 
        sentiment_dict = sid_obj.polarity_scores(sentence)

        print("Overall sentiment dictionary is : ", sentiment_dict)
        #print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
        #print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
        #print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
        print("Sentence Overall Rated As", end = " ")

        # decide sentiment as positive, negative and neutral 
        if sentiment_dict['compound'] >= 0.05 :
                print("Positive")
        elif sentiment_dict['compound'] <= - 0.05 :
                print("Negative")
        else :
                print("Neutral")
        return [sentiment_dict['neg']*100, sentiment_dict['pos']*100] 

#Load Data from transcripts
debates = {}

with open('transcripts.csv', 'r') as csvfile:
    next(csvfile)
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        if str(row[0]) in debates: 
            if str(row[1]) in debates[str(row[0])]: 
                debates[row[0]][row[1]].append(row[2])
            else: 
                debates[str(row[0])][str(row[1])] = []
                debates[str(row[0])][str(row[1])].append(str(row[2]))
        else:
            debates[str(row[0])] = {}
            debates[str(row[0])][str(row[1])] = []
            debates[str(row[0])][str(row[1])].append(str(row[2]))

#write to file
sample = open('debates.json', 'w') 
print(json.dumps(debates, indent=4, sort_keys=True), file = sample) 
sample.close() 


#Load Data from Polls
performance = {}
with open('data/A++.csv', 'r') as file:
    next(file)
    pollreader = csv.reader(file)
    for row in pollreader:
        if str(row[0]) in performance:
            if str(row[1]) in performance[str(row[0])]:
                continue #performance[row[0]][row[1]].append(row[2])
            else:
                performance[str(row[0])][str(row[1])] = []
                performance[str(row[0])][str(row[1])].append(str(row[2]))
                performance[str(row[0])][str(row[1])].append(str(row[3]))
        else:
            performance[str(row[0])] = {}
            performance[str(row[0])][str(row[1])] = []
            performance[str(row[0])][str(row[1])].append(str(row[2]))
            performance[str(row[0])][str(row[1])].append(str(row[3]))


#Write to file
sample = open('performance.json', 'w') 
print(json.dumps(performance, indent=4, sort_keys=True), file = sample)

# Driver code 
if __name__ == "__main__" :
        records = {}
        for date in debates.keys(): 
            #print("Debate Date: ", date)
            for speaker in debates[date].keys(): 
                 #print(date, speaker)
                speech = TreebankWordDetokenizer().detokenize(debates[date][speaker])
                #print(speech)
                #print("\nSpeaker Name: " + speaker)
                sentence = speech #"Geeks For Geeks is the best portal for the computer science engineering students."

                # function calling 
                score = sentiment_scores(sentence)
                data = [date, speaker, score] 
                #print("Date, Speaker, Negative, posiitve", data)

                if date in records:
                    if speaker in records: 
                        records[date][speaker] = score
                    else:
                        records[date][speaker] = {}
                        records[date][speaker] = score
                else: 
                    records[date] = {}
                    records[date][speaker] = {}
                    records[date][speaker] = score

        #print(records) 
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(records)

        #Write to file 
        sample = open('records.json', 'w')
        print(json.dumps(records, indent=4, sort_keys=True), file = sample)
        sample.close()

        print("There were ", len(records), " debates.")
        print("There are ", len(performance), " recorded polling days.")
              









