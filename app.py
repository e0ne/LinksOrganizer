from flask import Flask, render_template

import twits

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', twits=twits.favorite_twits())


if __name__ == '__main__':
    app.debug = True
    app.run()
