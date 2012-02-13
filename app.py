from flask import Flask, jsonify, render_template, request, redirect, url_for, session, g, flash

from flaskext.oauth import OAuth

from wrappers import TwitterApiWrapper

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# configuration
DATABASE_URI = 'sqlite:////tmp/flask-oauth.db'
SECRET_KEY = '3d0d40c0-3b00-11e1-a1e5-00264a1c552e'

app = Flask(__name__)
app.secret_key = SECRET_KEY
oauth = OAuth()

#twitter = oauth.remote_app('twitter',
#        base_url='http://api.twitter.com/1/',
#        request_token_url='http://api.twitter.com/oauth/request_token',
#        access_token_url='http://api.twitter.com/oauth/access_token',
#        authorize_url='http://api.twitter.com/oauth/authenticate',
#        consumer_key='zYZS8rzUAxhPFRcKBenhPQ',
#        consumer_secret='AgXBoAjx3QuBtUQ60bEWFupNYGLITa1dTY3ljWw'
#    )

twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authorize',
    # the consumer keys from the twitter application registry.
    consumer_key='bCNMPo60kdOe1kMQ6Bpk5g',
    consumer_secret='MlUmEsYDmW9Pd8DqJNQK5lptEYGGOmBZnQGWNpQpjI'
)

# setup sqlalchemy
engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
#    models = (InstanceInfo, InstanceSegment)
#    engine = get_engine()
#    for model in models:
#        model.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True)
    name = Column(String(60))
    oauth_token = Column(String(200))
    oauth_secret = Column(String(200))

    def __init__(self, name):
        self.name = name


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db_session.remove()
    return response

@twitter.tokengetter
def get_twitter_token():
    """This is used by the API to look for the auth token and secret
    it should use for API calls.  During the authorization handshake
    a temporary set of token and secret is used, but afterwards this
    function has to return the token and secret.  If you don't want
    to store this in the database, consider putting it into the
    session instead.
    """

    user = g.user
    if user is not None:
        return user.oauth_token, user.oauth_secret

@app.route('/')
def index():
    if not g.user:
        return redirect('/login')
    wrapper = TwitterApiWrapper()
    tweets = []
    if g.user is not None:
        resp = twitter.get('favorites.json')
        if resp.status == 200:
            tweets = wrapper.favorites(resp.data)
    return render_template('index.html', twits=tweets)
    #return render_template('index.html', twits=wrapper.favorites())

@app.route('/unfavorite')
def unfavorite():
    wrapper = TwitterApiWrapper(
            app.config['TWITTER_CONSUMER_KEY'],
            app.config['TWITTER_CONSUMER_SECRET'],
            app.config['TWITTER_ACCESS_TOKEN'],
            app.config['TWITTER_ACCESS_TOKEN_SECRET'])
    id = request.args.get('id', '')
    if id:
        wrapper.unfavorite(id)
    return jsonify(result='ok')

@app.route('/retweet')
def retweet():
    wrapper = TwitterApiWrapper(
            app.config['TWITTER_CONSUMER_KEY'],
            app.config['TWITTER_CONSUMER_SECRET'],
            app.config['TWITTER_ACCESS_TOKEN'],
            app.config['TWITTER_ACCESS_TOKEN_SECRET'])
    id = request.args.get('id', '')
    if id:
        wrapper.retweet(id)
    return jsonify(result='ok')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/twitter')
def twitter_login():
    return twitter.authorize(callback=url_for('oauth_authorized',
            next=request.args.get('next') or '/'))

@app.route('/logout/twitter')
def twitter_logout():
    session.pop('user_id', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    """Called after authorization.  After this function finished handling,
    the OAuth information is removed from the session again.  When this
    happened, the tokengetter from above is used to retrieve the oauth
    token and secret.

    Because the remote application could have re-authorized the application
    it is necessary to update the values in the database.

    If the application redirected back after denying, the response passed
    to the function will be `None`.  Otherwise a dictionary with the values
    the application submitted.  Note that Twitter itself does not really
    redirect back unless the user clicks on the application name.
    """
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    user = User.query.filter_by(name=resp['screen_name']).first()

    # user never signed on
    if user is None:
        user = User(resp['screen_name'])
        db_session.add(user)

    # in any case we update the authenciation token in the db
    # In case the user temporarily revoked access we will have
    # new tokens here.
    user.oauth_token = resp['oauth_token']
    user.oauth_secret = resp['oauth_token_secret']
    db_session.commit()

    session['user_id'] = user.id
    flash('You were signed in')
    return redirect(next_url)

if __name__ == '__main__':
    app.debug = True
    app.config.from_object('config.twitter.TwitterConfig')
    init_db()
    app.run()
