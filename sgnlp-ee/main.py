from flask import Flask, render_template, request, url_for, redirect, flash
from funcs import checkdata
from reddit_scraper_2 import *
from plagarism_checker import *
import string
#import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt 
#from tqdm import tqdm
#import re
#import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
#from nltk.stem.porter import PorterStemmer
#from wordcloud import WordCloud


app = Flask(__name__) #creating the Flask class object   
app.secret_key = "thisisasecret"


@app.route('/', methods = ["POST","GET"])
def root():
    return render_template("home.html")


@app.route('/plag_check', methods = ["POST","GET"])
def plag_check():
    if request.method == "POST":
        content_category = request.form["content_category"]
        content_title = request.form["content_title"]
        content = request.form["content"]
        search_query = content_category + ' ' + content_title
        main_plagarism_checker(search_query,content)
        flash('Plagarism check complete! View your results in the tab to the right.', 'green')
        return redirect(url_for('plag_check'))
    return render_template("plagarism.html")
    
    
@app.route('/cb', methods = ["POST","GET"]) 
def cb():
    if request.method == "POST":
        data = []
        qtype = request.form["qtype"]
        if qtype == "url":
            url = request.form["url"]
            post_data, comment_data = reddit_scraper_via_url(url)
        #elif qtype == "category":
            #categroy = request.form["categroy"]
            #limit = request.form["limit"]
            #post_data, comment_data = reddit_scraper_via_category(categroy, limit)
        else:
            subreddit_lst = list(request.form["subreddit_lst"].translate({ord(c): None for c in string.whitespace}).split(','))
            query_lst = list(request.form["query_lst"].translate({ord(c): None for c in string.whitespace}).split(','))
            limit = int(request.form["limit"])
            sort = request.form["sort"]
            #post_data, comment_data = reddit_scraper_via_query(subreddit_lst, query_lst, sort, limit)
            print((subreddit_lst, query_lst, sort, limit))
            try:
                post_data, comment_data = reddit_scraper_via_query(subreddit_lst, query_lst, sort, limit)
            except:
                flash('Error: Bad query, results not found. Possible spelling mistakes.', 'red')
                flash('To resolve, the following default values were used; sub = AskReddit, query = Coding, sort = Top, limit = 1', 'yellow')
                post_data, comment_data = reddit_scraper_via_query()
        
        issues = checkdata(post_data, comment_data)
        for i in range(len(post_data)): #for every post
            post = post_data[i]
            post_issues = issues[post['id'][0]]
            if len(post_issues) > 0:
                dataelement = []
                dataelement.append(post['title'][0])
                dataelement.append(post['url'][0])
                theseissues = []
                for issue in post_issues:
                    theseissues.append((issue.comment_author, issue.comment_body, issue.comment_link_id))
                dataelement.append(theseissues)
                data.append(dataelement)
        return render_template("cb_results.html",data = data)

    return render_template("index.html")

@app.route('/fake_news_detector', methods = ["POST","GET"]) 
def fake_news_detector():
    return render_template("coming_soon.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ =='__main__':  
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True, use_reloader=False)  

