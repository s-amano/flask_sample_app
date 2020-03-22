from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object('flaskr.config')

db = SQLAlchemy(app)

# インデックスページ
import flaskr.views

# ログイン機能の追加
import flaskr.auth
app.register_blueprint(auth.bp)

# 書籍管理機能の追加
import flaskr.book
app.register_blueprint(book.bp)
