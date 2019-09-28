# 家計簿アプリを作成 以下のURLを参考にした。
https://github.com/TaroNoguchi/flask-app-practice
# app.pyとhtmlファイル、DBを変更。
- app.py
    - タイトル等必要箇所を変更。
    - charge = db.Column(db.Integer) を追加。
- index.html
    - {{ posts | sum(attribute='') }} で、金額の合計が表示できるということが分かるまで相当苦労した。
    - request.form[""]だとナゼかstr型になってしまう。request.form.get()にしなければいけないと気付いた。
- DB(SQLite)
    - DB Browser for SQLite をダウンロード。
    - テーブル "posts" に 項目 "income", "expense" を追加。

# これから
- 年月ごとにページを分けられるようにする
- ログイン機能をつける
- herokuにデプロイして誰でも使えるように