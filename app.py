from flask import Flask
from flask import render_template, request, redirect, session
from pymongo import MongoClient
from flask_mail import Mail
import time
from bs4 import BeautifulSoup

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['HoundHunt']
collection = db['webscraped']




@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        paragraphs= []
        # data_present = False
        data = request.form.get("data")
        collection.create_index([('html', 'text')])

        search_term = data
        start_time = time.time()
        results = collection.find(
            {'$text': {'$search': search_term}},
            {'score': {'$meta': 'textScore'}, 'url': 1,'title':1,'html':1}
        ).sort([('score', {'$meta': 'textScore'})])
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time = "{:.5f}".format(elapsed_time)
        # print(results)

        # print(paragraphs)
        # if results == 0:
        #     data_present=False
        # else:
        #     data_present=True

        # for result in results:
        #     print(result['url'], result['score'])
        
        return render_template('result.html',BeautifulSoup=BeautifulSoup,results = results,data=data,total_time=elapsed_time)


    #     # print(data)
    return render_template('index.html')


app.run(debug=True)
