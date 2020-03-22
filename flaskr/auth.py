
"""
ログイン処理などを行う
"""

from flaskr import app, db
from flaskr.models import Book, User
from functools import wraps


from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')




def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            flash('ログインをしてからにして', category='alert alert-info')
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_view

@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # print(session['user_id'])
        # print(session)
        g.user = User.query.get(session['user_id'])
        print(g.user)


@bp.route('/users/create', methods=('GET', 'POST'))
def create_user():
    """
    GET ：ユーザー登録画面に遷移
    POST：ユーザー登録処理を実施
    """

    if request.method == 'POST':  # 2.ユーザがフォームの値を返した場合
        username = request.form['username']  # 3.ユーザが入力したusernameとpasswordの値
        password = request.form['password']

        error = None

        if not username:  # 4.usernameが空でないか
            error = 'Username is required.'
        elif not password:  # 4.passwordが空でないか
            error = 'Password is required.'
        elif User.query.filter(User.user_name == username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:  # 6.インプットの値が妥当であった場合
            user = User(user_name=request.form['username'],
                        password=request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('ユーザー登録が完了しました。登録した内容でログインしてください', category='alert alert-info')
            return redirect(url_for('auth.login'))  # 7.ログインページにリダイレクト

        flash(error)  # 8.インプットの値が妥当でない場合

    return render_template('auth/create_user.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
        GET ：ログイン画面に遷移
        POST：ログイン処理を実施
        """
    if request.method == 'POST':
        # ログインフォームから送られてきた、ユーザー名とパスワードを取得
        username = request.form['username']
        password = request.form['password']

        error = None

        user = User.query.filter(User.user_name == username).first()

        # app.logger.debug("*****************:")
        # app.logger.debug(password)
        # app.logger.debug("------------:")
        # app.logger.debug(type(user))
        # app.logger.debug(user.password)
        # app.logger.debug("*****************:")
        if user is None:
            error = 'Incorrect username.'
        # elif not check_password_hash(user.password, password):  # 2.パスワードをハッシュ値の比較で照合
        elif user.password != password:  # 2.パスワードをハッシュ値の比較で照合
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id  # 3.sessionにユーザのidを保存
            flash('{}さんとしてログインしました'.format(username), category='alert alert-info')
            return redirect(url_for('home'))
        else:
            flash(error, category='alert alert-danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')



@bp.route('/logout')
def logout():
    """ログアウトする"""
    session.clear()
    flash('ログアウトしました', category='alert alert-info')
    return redirect(url_for('home'))