from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.create_all()

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    content = db.Column(db.Text())

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
    db.commit()
    posts = Post.query.all()
    return render_template("index.html", posts = posts)

