from flask import Flask
from flask import request as abhishek_request
from flask import jsonify
from naive_bayes_classifier import NaiveBayesClassifier
import urllib.request
import json
import glob
import re
import random
from collections import Counter

PATH = "./dataset/"
app = Flask(__name__)
check_var = 0 
classifier = "" 

def split_data(data, prob):
    random.shuffle(data)
    data_len = len(data)
    split = int(prob * data_len)
    train_data = data[:split]
    test_data = data[split:]
    return train_data, test_data

@app.route('/checkSpamFilter', methods=['POST'])
def spamFilterChecker():
      print ('Received the JAVA Request!')
      # Get the text data from the JAVA Program.
      req_data = abhishek_request.get_json() 
      text_to_be_classified = req_data['text_to_be_classified']
      print (text_to_be_classified) 

      # ----------------------------------------------------------------------------
      # Make a POST request to the plino Spam API. 
      # ----------------------------------------------------------------------------
      data = []
      for verdict in ['spam', 'not_spam']:
            for files in glob.glob(PATH + verdict + "/*")[:500]:
                  is_spam = True if verdict == 'spam' else False
                  with open(files, "r", encoding='utf-8', errors='ignore') as f:
                        for line in f:
                              if line.startswith("Subject:"):
                                    subject = re.sub("^Subject: ", "", line).strip()
                                    data.append((subject, is_spam))

      random.seed(0)
      train_data, test_data = split_data(data, 0.80)
      classifier = NaiveBayesClassifier()
      classifier.train(train_data)
      
      json_response = ""
      value = classifier.classify(text_to_be_classified) 
      if value < 0.9: 
            json_response = "{'email_class' : 'spam'}"
      else:
            json_response = "{'email_class' : 'ham'}"
      print ("====================================================")
      print ("POSSIBILITY OF HAM : ", value) 
      print(json_response) 
      print ("====================================================")
      return json_response 
        

if __name__ =="__main__":
    app.run(debug=True)