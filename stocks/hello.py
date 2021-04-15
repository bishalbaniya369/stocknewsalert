from flask import Flask
from flask import Flask, jsonify, request, session, send_file, redirect, render_template, flash
import requests
#from twilio.rest import Client

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route('/action_page', methods=['GET', 'POST'])
def stock():
    phone_number = request.form.get('phone_number')
    ticker = request.form.get('ticker')
    print("Your phone number: ", phone_number)
    print("Ticker selected: ", ticker)   

    #for testing using Tesla as example
    STOCK_NAME = ticker
   ##maybe pull company name from the ticker if possible COMPANY_NAME = "Tesla Inc"

    STOCK_ENDPOINT = "https://www.alphavantage.co/query"
    NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
    STOCK_API_KEY = "K9K5ADN99GWI7SE8"
    NEWS_API_KEY = "b0b52657236b4df284fedab693b18476"
    TWILIO_id ="ACed7ead9b981ea39266dde7f1fb0decd9"
    TWILIO_auth="4c4f07875af969dea52cd68b8bfdea50"
        ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
    # When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

    #TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": STOCK_API_KEY
                    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    #checking what kind of data is returned by the API
    #print(response.json())
    data = response.json()["Time Series (Daily)"]
    data_list =[value for (key, value) in data.items()]
    #list comprehention,, I am pulling out yesterday's price
    yesterday_data = data_list[0]
    yesterday_close = yesterday_data["4. close"]
    #same thing for the day before yesterday
    daybefore_yesterday_data = data_list[1]
    daybefore_yesterday_close = daybefore_yesterday_data["4. close"]
    print(yesterday_close)
    print(daybefore_yesterday_close)
    diff = abs(float(daybefore_yesterday_close)-float(yesterday_close))
    #now working on NEWS_API 
    #declaring news params
    news_params={"apikey":NEWS_API_KEY,
                 "qInTitle": ticker}
    news_response =requests.get(NEWS_ENDPOINT,params=news_params)
    #checking news response in json
    #print(news_response.json())
    articles = news_response.json()["articles"]
    #slicing for the top three article using python slice opereator
    three_articles = articles[:3]
    # making the news readable by slicing article headline , description and source
    # ready_article = [f"Headline: {article['title']}. Url:{article['url']} " for article in three_articles]
    # news1= ready_article[0]
    #creating a twilio client class

   # client= Client(TWILIO_id,TWILIO_auth)
    #sending the message
   #/ for article in ready_article:
    #    message = client.messages.create(
    #        body =article,
    #        from_="+122244429844",
    #       to="+14692628335"
    #   ) 
    #return render_template("main.html", price=diff)

    return render_template("news.html", articles=three_articles)
