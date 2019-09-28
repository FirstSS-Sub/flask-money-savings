from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///money.db'
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
    income = db.Column(db.Integer)#追加
    expense = db.Column(db.Integer)#追加

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

    return redirect(url_for('.index'))

@app.route('/new')
def new_post():
    
    return render_template("new.html")


@app.route('/create', methods=["POST"])
def create_post():
    
    new_post = Post()
    new_post.title = request.form["title"]
    #金額入力を追加
    #合計計算の際にint + None とならないよう0を代入
    
    ### request.form.get を使わないでrequest.form[""]を使うとなぜかstr型になる
    if not isinstance(request.form.get('income', type=int), int):
        new_post.income = 0
    else:
        new_post.income = request.form.get('income', type=int)

    if not isinstance(request.form.get('expense', type=int), int):
        new_post.expense = 0
    else:
        new_post.expense = request.form.get('expense', type=int)
    #

    """
    new_post.income = 0
    new_post.expense = 0
    """

    """
    new_post.income = request.form["income"]
    new_post.expense = request.form["expense"]
    """

    new_post.content = request.form["content"]
    new_post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    new_post.commit = 0

    #app.logger.info(new_post.income)
    #app.logger.info(new_post.expense)

    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('.index'))


@app.route('/edit/<int:id>')
def edit_post(id):
    
    post = Post.query.get(id)

    return render_template("edit.html", post = post)

@app.route('/update/<int:id>', methods=["POST"])
def update_post(id):

    post = Post.query.get(id)
    post.title = request.form["title"]
    #金額入力を追加
    #合計計算の際にint + None とならないよう0を代入
    
    ### request.form.get を使わないでrequest.form[""]を使うとなぜかstr型になる
    if not isinstance(request.form.get('income', type=int), int):
        post.income = 0
    else:
        post.income = request.form.get('income', type=int)

    if not isinstance(request.form.get('expense', type=int), int):
        post.expense = 0
    else:
        post.expense = request.form.get('expense', type=int)
    #
    post.content = request.form["content"]
    post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    db.session.commit()

    return redirect(url_for('.index'))

@app.route('/done/<int:id>')
def done_post(id):

    post = Post.query.get(id)
    post.commit = 1
    post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    db.session.commit()
    posts = Post.query.all()

    return redirect(url_for('.index'))

@app.route('/undone/<int:id>')
def undone_post(id):

    post = Post.query.get(id)
    post.commit = 0
    post.date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
    db.session.commit()
    posts = Post.query.all()

    return redirect(url_for('.index'))