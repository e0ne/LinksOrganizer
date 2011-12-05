from flask import Flask, jsonify, render_template, request

import twits

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', twits=twits.favorite_twits())

@app.route('/unfavorite')
def unfavorite():
    return jsonify(result='ok')

if __name__ == '__main__':
    app.debug = True
    app.run()
