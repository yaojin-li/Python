from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def index():
    user = {'username': 'lxj'}
    posts = [
        {
            "author": {'username': '一一'},
            "body": "我是一一"
        },{
            "author": {'username': "二二"},
            "body": "我是二二"
        }
    ]
    return render_template("index.html",
                           # title = '标题',
                           user = user,
                           posts = posts)

@app.route("/index_base")
def index_base():
    user = {'username': 'lxj'}
    posts = [
        {
            "author": {'username': '一一'},
            "body": "我是一一"
        },{
            "author": {'username': "二二"},
            "body": "我是二二"
        }
    ]
    return render_template("index_base.html",
                           # title = '标题',
                           user = user,
                           posts = posts)

if __name__ == '__main__':
    app.run()
