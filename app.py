from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.create_all()


class Post(db.Model):
   
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Text())
    title = db.Column(db.Text())
    content = db.Column(db.Text())
    commit = db.Column(db.Integer)


@app.route('/')
def index():
    
    posts = Post.query.all()
    return render_template("index.html", posts = posts)


@app.route('/show/<int:id>')
def show(id):
    
    post = Post.query.get(id)
    return render_template("show.html", post = post)


@app.route('/destroy/<int:id>')
def destroy(id):
   
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    posts = Post.query.all()
    return render_template("index.html", posts = posts)


@app.route('/new')
def new_post():
    
    return render_template("new.html")

@app.route('/create', methods=["POST"])
def create_post():
    
    new_post = Post()
    new_post.title = request.form["title"]
    new_post.content = request.form["content"]
    new_post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    new_post.commit = 0
    db.session.add(new_post)
    db.session.commit()

    posts = Post.query.all()

    return render_template("index.html", posts = posts)


@app.route('/edit/<int:id>')
def edit_post(id):
    
    post = Post.query.get(id)

    return render_template("edit.html", post = post)

@app.route('/update/<int:id>', methods=["POST"])
def update_post(id):

    post = Post.query.get(id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    db.session.commit()

    return render_template("show.html", post = post)

@app.route('/done/<int:id>')
def done_post(id):

    post = Post.query.get(id)
    post.commit = 1
    db.session.commit()
    posts = Post.query.all()

    return render_template("index.html", posts = posts)

@app.route('/undone/<int:id>')
def undone_post(id):

    post = Post.query.get(id)
    post.commit = 0
    db.session.commit()
    posts = Post.query.all()

    return render_template("index.html", posts = posts)