from flask import Flask, jsonify, render_template, request

from wrappers import TwitterApiWrapper

app = Flask(__name__)

@app.route('/')
def index():
    wrapper = TwitterApiWrapper(
        app.config['TWITTER_CONSUMER_KEY'],
        app.config['TWITTER_CONSUMER_SECRET'],
        app.config['TWITTER_ACCESS_TOKEN'],
        app.config['TWITTER_ACCESS_TOKEN_SECRET'])
    return render_template('index.html', twits=wrapper.favorites())

@app.route('/unfavorite')
def unfavorite():
    return jsonify(result='ok')

if __name__ == '__main__':
    app.debug = True
    app.config.from_object('config.twitter.TwitterConfig')
    app.run()
