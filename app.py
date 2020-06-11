from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import os
app = Flask(__name__)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def index():
        render_template('results.html')
        try:
            r = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
            soup = BeautifulSoup(r.content, 'html.parser')  # To make it beautiful
            movies_class = soup.find_all('td', class_='titleColumn')
            review = []
            for movie in movies_class:
                try:
                    moviename = movie.find('a').get_text()
                    # Get the Release Years
                except:
                    moviename=None
                try:
                    year = movie.find('span').get_text()
                except:
                    year=None
                mov_and_year = {"Movie Title": moviename, "Year Of Release": year}
                review.append(mov_and_year)
            return render_template('results.html', review=review[0:(len(review) - 1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=8001, debug=True)